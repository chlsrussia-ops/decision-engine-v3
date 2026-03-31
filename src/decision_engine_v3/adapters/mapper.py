"""Generic mapping utilities for adapters."""

def safe_float(val, default: float = 0.0) -> float:
    try: return float(val) if val is not None else default
    except (ValueError, TypeError): return default

def safe_int(val, default: int = 0) -> int:
    try: return int(val) if val is not None else default
    except (ValueError, TypeError): return default

def safe_str_list(val) -> list[str]:
    if not val: return []
    if isinstance(val, list): return [str(v).strip() for v in val if v and str(v).strip()]
    return []

def clamp(val: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(val, hi))
