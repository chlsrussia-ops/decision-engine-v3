from decision_engine_v3.engine.safe_executor import safe_execute

def test_success():
    r = safe_execute("test", lambda: 42, 0)
    assert r.value == 42
    assert r.success is True
    assert r.fallback_used is False

def test_failure_returns_fallback():
    def broken(): raise ValueError("boom")
    r = safe_execute("test", broken, -1)
    assert r.value == -1
    assert r.success is False
    assert r.fallback_used is True
    assert "boom" in r.error_message
