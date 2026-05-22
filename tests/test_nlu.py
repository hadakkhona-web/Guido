# tests/test_nlu.py
from unittest.mock import patch
from PC.brain.nlu import NLU
from PC.brain.person_lookup import PersonLookup

nlu = NLU()


# ── NLU tests (mocked — no Ollama call, instant) ──────────────────────────

def test_destination_intent():
    fake_response = '{"intent": "GUIDE_TO", "destination": "youssef\'s office"}'
    with patch.object(nlu, '_ask_model', return_value=fake_response):
        intent, entities = nlu.process("guide me to youssef's office")
        assert intent == "GUIDE_TO"
        assert entities["destination"] == "youssef"


def test_unknown_input():
    fake_response = '{"intent": "UNKNOWN", "destination": null}'
    with patch.object(nlu, '_ask_model', return_value=fake_response):
        intent, entities = nlu.process("bla bla random")
        assert intent == "UNKNOWN"
        assert entities == {}


def test_invalid_intent_fallback():
    """Model hallucinating a bad intent → should fall back to UNKNOWN."""
    fake_response = '{"intent": "DANCE", "destination": null}'
    with patch.object(nlu, '_ask_model', return_value=fake_response):
        intent, _ = nlu.process("do a backflip")
        assert intent == "UNKNOWN"


def test_broken_json_fallback():
    """Model returning garbage → should not crash, returns UNKNOWN."""
    with patch.object(nlu, '_ask_model', return_value="not json at all %%%"):
        intent, entities = nlu.process("whatever")
        assert intent == "UNKNOWN"
        assert entities == {}


# ── PersonLookup tests (no API, instant) ─────────────────────────────────

def test_known_person_resolves():
    result = PersonLookup().find_person("youssef")
    assert result is not None
    assert "1.38" in result["name"]


def test_unknown_person_returns_none():
    """This is what was missing — unknown person must NOT resolve."""
    result = PersonLookup().find_person("boogieman")
    assert result is None


def test_partial_name_match():
    """'abder' should still resolve to abderrahmane's office."""
    result = PersonLookup().find_person("abder")
    assert result is not None