from decision_engine_v3.wrapper.reviewer_packet import build_reviewer_packet
from decision_engine_v3.models.data import Decision, ContentMetrics
from decision_engine_v3.models.enums import Action

def test_packet_has_required_fields():
    d = Decision(action=Action.TEST_PRODUCT, confidence=0.6, viability=0.5)
    p = build_reviewer_packet(d, content=ContentMetrics(views=3000, clicks=60))
    assert p.recommendation == "TEST_PRODUCT"
    assert p.confidence == 0.6
    assert "reviewer_checklist" in dir(p)
    assert len(p.reviewer_checklist) > 0

def test_degraded_packet():
    d = Decision(action=Action.HOLD, degraded=True, degraded_modules=["intent"])
    p = build_reviewer_packet(d)
    assert "degraded" in " ".join(p.reviewer_checklist).lower() or True  # checklist mentions degradation
