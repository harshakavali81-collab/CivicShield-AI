"""Multilingual responses must remain curated and free of fabricated notices."""
import pytest
from civicshield.assistant.guidance import answer

@pytest.mark.parametrize("language", ["en", "te", "hi", "ta", "kn"])
def test_curated_guidance_for_all_languages(language):
    result = answer("flood", language)
    assert result["answer"]
    assert result["topic"] == "flood"
    assert result["language"] == language
    assert result["live_retrieval"] is False
    assert result["is_official_warning"] is False
    assert result["references"][0]["url"].startswith("https://")

def test_unknown_question_gets_general_preparedness():
    assert answer("help please", "en")["topic"] == "general"

def test_api_rejects_unsupported_language(client):
    response = client.post("/api/v1/assistant/ask", json={"question": "Flood advice", "language": "xx"})
    assert response.status_code == 422
