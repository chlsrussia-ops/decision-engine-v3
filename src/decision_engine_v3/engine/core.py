"""DecisionEngineV3 — core orchestration. No transport. Returns Decision."""
from __future__ import annotations
from ..models.data import *
from ..models.enums import Action, DecisionMode, HumanRuleStatus, ReasonCode
from ..flags.config import FeatureFlags
from .safe_executor import safe_execute
from .signal_cleaning import clean_signals
from .intent import compute_intent
from .evidence import compute_evidence
from .antiviral import compute_antiviral
from .viability import compute_viability
from .confidence import compute_confidence
from .marketplace import compute_marketplace
from .economics import compute_economics
from .caps import build_caps, apply_cap
from .neutral_builders import *
from .reasoning import build_red_flags


class DecisionEngineV3:
    def __init__(self, flags: FeatureFlags | None = None):
        self.flags = flags or FeatureFlags()

    def decide_explore(self, content: ContentMetrics, marketplace_raw: MarketplaceMetrics | None = None, economics_raw: EconomicsPreview | None = None, reviewer: ReviewerContext | None = None) -> Decision:
        decision = Decision(mode=DecisionMode.EXPLORE)
        degraded: list[str] = []
        errors: list[str] = []

        # 1. Signal cleaning
        cleaning = neutral_cleaning()
        if self.flags.enable_signal_cleaning:
            r = safe_execute("signal_cleaning", lambda: clean_signals(content.comments), neutral_cleaning())
            cleaning = r.value
            if not r.success: degraded.append(r.module_name); errors.append(r.error_message)
        decision.trace.signal_cleaning = {"clean_count": cleaning.clean_comment_count, "dup_ratio": cleaning.duplicate_ratio, "spam_ratio": cleaning.spam_ratio, "uniqueness": cleaning.uniqueness_score, "removed_duplicates": cleaning.removed_duplicates, "removed_spam": cleaning.removed_spam, "removed_noise": cleaning.removed_noise, "degraded": "signal_cleaning" in degraded}

        comments = cleaning.clean_comments if self.flags.enable_signal_cleaning else content.comments

        # 2. Intent
        r = safe_execute("intent", lambda: compute_intent(comments, cleaning if self.flags.enable_signal_cleaning else None), neutral_intent())
        intent = r.value
        if not r.success: degraded.append(r.module_name); errors.append(r.error_message)
        decision.intent_score = intent.qualified_intent if self.flags.enable_qualified_intent else intent.raw_intent
        decision.trace.intent_engine = {"qualified": intent.qualified_intent, "raw": intent.raw_intent, "density": intent.intent_density, "negative_rate": intent.negative_rate, "strong_share": intent.strong_intent_share, "penalties": intent.penalties, "high_hits": intent.high_intent_hits, "negative_hits": intent.negative_hits, "degraded": "intent" in degraded}

        # 3. Evidence
        r = safe_execute("evidence", lambda: compute_evidence(content, marketplace_raw, cleaning if self.flags.enable_signal_cleaning else None), neutral_evidence())
        evidence = r.value
        if not r.success: degraded.append(r.module_name); errors.append(r.error_message)
        decision.trace.evidence_engine = {"score": evidence.evidence_score, "comment": evidence.comment_confidence, "volume": evidence.volume_confidence, "click": evidence.click_confidence, "marketplace": evidence.marketplace_confidence, "gates_triggered": ["evidence_hold"] if evidence.evidence_score < 0.35 else [], "degraded": "evidence" in degraded}

        # 4. Anti-viral
        antiviral = neutral_antiviral()
        if self.flags.enable_antiviral_v3:
            r = safe_execute("antiviral", lambda: compute_antiviral(content, intent), neutral_antiviral())
            antiviral = r.value
            if not r.success: degraded.append(r.module_name); errors.append(r.error_message)
        decision.trace.anti_viral = {"score": antiviral.antiviral_score, "status": antiviral.status, "empty_viral": antiviral.empty_viral_score, "curiosity_bait": antiviral.curiosity_bait_score, "rage": antiviral.rage_score, "entertainment": antiviral.entertainment_score, "misleading_cta": antiviral.misleading_cta_score, "false_viral": antiviral.false_viral_score, "gates_triggered": ["antiviral_block"] if antiviral.antiviral_score >= 0.6 else [], "degraded": "antiviral" in degraded}

        # 5. Marketplace
        mkt = neutral_marketplace()
        if self.flags.enable_marketplace_modifier_v3:
            r = safe_execute("marketplace", lambda: compute_marketplace(marketplace_raw), neutral_marketplace())
            mkt = r.value
            if not r.success: degraded.append(r.module_name); errors.append(r.error_message)
        decision.trace.marketplace_modifier = {"pressure": mkt.pressure_score, "saturation": mkt.saturation_state, "demand_proof": mkt.demand_proof_score, "fake_opp": mkt.fake_opportunity}

        # 6. Economics
        r = safe_execute("economics", lambda: compute_economics(economics_raw), neutral_economics())
        econ = r.value
        if not r.success: degraded.append(r.module_name); errors.append(r.error_message)
        decision.trace.economics = {"margin": econ.estimated_margin_pct, "status": econ.status, "landed_above": econ.landed_above_market_min, "margin_ok": econ.margin_ok, "gates_triggered": ["economics_fail"] if econ.status == "fail" else [], "degraded": "economics" in degraded}

        # 7. Viability
        r = safe_execute("viability", lambda: compute_viability(content, intent, evidence, antiviral, mkt), neutral_viability())
        viability = r.value
        if not r.success: degraded.append(r.module_name); errors.append(r.error_message)
        decision.viability = viability.viability
        decision.trace.viability_engine = {"score": viability.viability, "components": viability.components, "caps_applied": viability.caps_applied, "degraded": "viability" in degraded}

        # 8. Confidence
        conf = neutral_confidence()
        if self.flags.enable_confidence_engine:
            r = safe_execute("confidence", lambda: compute_confidence(evidence, cleaning, mkt), neutral_confidence())
            conf = r.value
            if not r.success: degraded.append(r.module_name); errors.append(r.error_message)
        decision.confidence = conf.confidence
        decision.trace.confidence_engine = {"score": conf.confidence, "components": conf.components, "penalties": conf.penalties, "gates_triggered": ["confidence_cap"] if conf.confidence < 0.30 else [], "degraded": "confidence" in degraded}

        # 9. Policy
        from ..policies.explore import decide_explore_action
        policy_action, reasons, reason_codes = decide_explore_action(content, intent, evidence, viability, self.flags)
        decision.reasons = reasons
        decision.reason_codes = reason_codes

        # 10. Human rule
        from ..policies.reviewer_rules import evaluate_human_rule
        decision.human_rule = evaluate_human_rule(intent, evidence, conf, viability, antiviral)

        # 11. Caps
        caps = build_caps(evidence, antiviral, conf, econ, mkt, decision.human_rule)
        decision.caps = caps
        decision.action = apply_cap(policy_action, caps)
        decision.trace.policy_engine = {"raw_action": policy_action.value, "capped_action": decision.action.value, "cap_reasons": [c.value for c in caps.reasons], "downgraded": policy_action.value != decision.action.value, "human_rule": decision.human_rule.value}

        # 12. Red flags
        decision.red_flags = build_red_flags(content, intent, evidence, antiviral, conf, econ, mkt, viability)
        decision.red_flag_codes = [f.code for f in decision.red_flags]

        # 13. CAUTION override
        if self.flags.enable_caution_status and decision.action == Action.TEST_PRODUCT:
            hard = [f for f in decision.red_flags if f.severity == "hard"]
            if hard:
                decision.action = Action.CAUTION

        # 14. Degradation metadata
        decision.degraded = bool(degraded)
        decision.degraded_modules = degraded
        decision.module_errors = errors
        decision.fallback_used = bool(degraded)
        return decision

    def decide_sell(self, sell: SellMetrics) -> Decision:
        decision = Decision(mode=DecisionMode.SELL)
        from ..policies.sell import decide_sell_action
        action, reasons, codes = decide_sell_action(sell)
        decision.action = action
        decision.reasons = reasons
        decision.reason_codes = codes
        return decision
