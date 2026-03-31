"""Signal Cleaning — dedup, spam filter, noise filter, whitelist."""
from __future__ import annotations
import re
from collections import Counter
from ..models.data import SignalCleaningResult

# Strong short phrases that should NOT be filtered as noise
WHITELIST_SHORT = {
    "где купить", "сколько стоит", "хочу", "беру", "нужно", "ссылка",
    "артикул", "цена", "доставка", "заказал", "взял", "купил",
}

SPAM_PATTERNS = [
    re.compile(r"https?://", re.I),
    re.compile(r"@\w+\s", re.I),
    re.compile(r"подписк|subscribe|follow", re.I),
    re.compile(r"бесплатн|free|giveaway|розыгрыш", re.I),
]


def clean_signals(comments: list[str]) -> SignalCleaningResult:
    if not comments:
        return SignalCleaningResult()

    normalized = [c.strip().lower() for c in comments if c and c.strip()]
    if not normalized:
        return SignalCleaningResult()

    # Dedup
    seen: dict[str, int] = {}
    unique = []
    duplicates = 0
    for c in normalized:
        key = re.sub(r"\s+", " ", c)
        if key in seen:
            duplicates += 1
        else:
            seen[key] = 1
            unique.append(c)

    # Spam filter
    clean = []
    spam_count = 0
    for c in unique:
        if any(p.search(c) for p in SPAM_PATTERNS):
            spam_count += 1
        else:
            clean.append(c)

    # Noise filter (too short, not in whitelist)
    final = []
    noise_count = 0
    for c in clean:
        if len(c) < 3 and c not in WHITELIST_SHORT:
            noise_count += 1
        elif len(c) < 2:
            noise_count += 1
        else:
            final.append(c)

    total = len(normalized)
    return SignalCleaningResult(
        clean_comments=final,
        clean_comment_count=len(final),
        duplicate_ratio=round(duplicates / total, 4) if total else 0.0,
        uniqueness_score=round(len(unique) / total, 4) if total else 1.0,
        spam_ratio=round(spam_count / total, 4) if total else 0.0,
        removed_duplicates=duplicates,
        removed_spam=spam_count,
        removed_noise=noise_count,
    )
