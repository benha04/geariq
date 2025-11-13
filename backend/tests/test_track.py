from app.services.track import track_rule, list_rules


def test_track_inmemory():
    # Ensure that in absence of DB (or if DB not running in test), we at least store the rule
    r = track_rule({"q": "test helmet", "budget": 100, "contact": "me@example.com"})
    assert r.get("id") is not None
    rules = list_rules()
    assert any(rr.get("q") == "test helmet" for rr in rules)
