"""SafeExecutor — fail-safe module execution with structured degradation."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Callable, Any
import logging

T = TypeVar("T")
logger = logging.getLogger("decision_engine.safe")


@dataclass
class SafeResult(Generic[T]):
    value: T
    success: bool = True
    module_name: str = ""
    fallback_used: bool = False
    error_message: str = ""


def safe_execute(module_name: str, fn: Callable[[], T], fallback: T) -> SafeResult[T]:
    """Execute fn safely. On failure, return fallback and log."""
    try:
        result = fn()
        return SafeResult(value=result, success=True, module_name=module_name)
    except Exception as e:
        logger.error(f"[{module_name}] FAILED: {e}", exc_info=True)
        return SafeResult(
            value=fallback, success=False, module_name=module_name,
            fallback_used=True, error_message=str(e),
        )
