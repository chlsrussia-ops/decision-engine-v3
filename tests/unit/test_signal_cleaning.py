from decision_engine_v3.engine.signal_cleaning import clean_signals

def test_dedup():
    r = clean_signals(["хочу", "хочу", "хочу", "беру"])
    assert r.removed_duplicates == 2
    assert r.clean_comment_count == 2

def test_spam():
    r = clean_signals(["https://spam.com купи", "хороший товар"])
    assert r.removed_spam == 1
    assert r.clean_comment_count == 1

def test_empty():
    r = clean_signals([])
    assert r.clean_comment_count == 0

def test_whitelist_short():
    r = clean_signals(["хочу", "беру", "ок"])
    assert r.clean_comment_count >= 2
