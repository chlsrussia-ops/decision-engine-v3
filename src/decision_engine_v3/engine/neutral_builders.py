"""Conservative neutral builders for disabled/failed modules. No permissive defaults."""
from ..models.data import (
    SignalCleaningResult, IntentResult, EvidenceResult, AntiViralResult,
    ViabilityResult, ConfidenceResult, MarketplaceModifierResult, EconomicsResult,
)


def neutral_cleaning() -> SignalCleaningResult:
    return SignalCleaningResult(uniqueness_score=0.5)


def neutral_intent() -> IntentResult:
    return IntentResult()


def neutral_evidence() -> EvidenceResult:
    return EvidenceResult(evidence_score=0.0)


def neutral_antiviral() -> AntiViralResult:
    return AntiViralResult(status="unknown")


def neutral_viability() -> ViabilityResult:
    return ViabilityResult()


def neutral_confidence() -> ConfidenceResult:
    return ConfidenceResult()


def neutral_marketplace() -> MarketplaceModifierResult:
    return MarketplaceModifierResult(saturation_state="unknown", review_maturity="unknown")


def neutral_economics() -> EconomicsResult:
    return EconomicsResult(status="unknown")
