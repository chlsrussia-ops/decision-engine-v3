"""Intent Engine V3 — dictionary-driven intent scoring with penalties."""
from __future__ import annotations
import re
from ..models.data import IntentResult, SignalCleaningResult

HIGH_INTENT = {"где купить": 1.0, "сколько стоит": 1.0, "артикул": 1.0, "ссылка": 1.0, "цена": 1.0, "как заказать": 1.0, "купить": 0.9, "заказать": 0.9}
MEDIUM_INTENT = {"хочу": 0.5, "беру": 0.5, "нужно": 0.5, "доставка": 0.5, "заказал": 0.5, "взял": 0.5, "купил": 0.5, "куплю": 0.5}
LOW_INTENT = {"прикольно": 0.1, "вау": 0.1, "интересно": 0.1, "круто": 0.1, "класс": 0.1, "огонь": 0.1}
NEGATIVE_INTENT = {"фигня": -0.5, "развод": -1.0, "обман": -1.0, "не работает": -0.5, "сломалось": -0.5, "мусор": -0.7, "хлам": -0.7}


def compute_intent(comments: list[str], cleaning: SignalCleaningResult | None = None) -> IntentResult:
    if not comments:
        return IntentResult()

    high, med, low, neg, skep = 0, 0, 0, 0, 0
    total_weight = 0.0
    keywords: list[str] = []

    for comment in comments:
        c = comment.lower()
        matched = False
        for phrase, w in HIGH_INTENT.items():
            if phrase in c:
                high += 1; total_weight += w; keywords.append(phrase); matched = True; break
        if matched: continue
        for phrase, w in NEGATIVE_INTENT.items():
            if phrase in c:
                neg += 1; total_weight += w; keywords.append(phrase); matched = True; break
        if matched: continue
        for phrase, w in MEDIUM_INTENT.items():
            if phrase in c:
                med += 1; total_weight += w; keywords.append(phrase); matched = True; break
        if matched: continue
        for phrase, w in LOW_INTENT.items():
            if phrase in c:
                low += 1; total_weight += w; keywords.append(phrase); matched = True; break

    total = len(comments)
    raw = round(total_weight / total * 2.5, 4) if total else 0.0
    weighted = raw

    # Penalties
    penalties = {}
    if cleaning:
        if cleaning.spam_ratio > 0.3:
            penalties["spam"] = -0.15
            weighted *= 0.85
        if cleaning.duplicate_ratio > 0.4:
            penalties["duplicates"] = -0.10
            weighted *= 0.90
    if total < 10:
        penalties["small_sample"] = -0.05
        weighted *= 0.95
    negative_rate = neg / total if total else 0.0
    if negative_rate > 0.2:
        penalties["high_negative"] = -0.20
        weighted *= 0.80

    qualified = max(round(weighted, 4), 0.0)
    intent_density = (high + med) / total if total else 0.0
    strong_share = high / (high + med + low) if (high + med + low) > 0 else 0.0

    return IntentResult(
        raw_intent=raw, weighted_intent=round(weighted, 4), qualified_intent=qualified,
        high_intent_hits=high, medium_hits=med, low_hits=low, skeptical_hits=skep, negative_hits=neg,
        intent_density=round(intent_density, 4), strong_intent_share=round(strong_share, 4),
        negative_rate=round(negative_rate, 4),
        top_keywords=list(dict.fromkeys(keywords))[:10],
        penalties=penalties,
    )
