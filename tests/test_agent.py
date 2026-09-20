from unittest.mock import MagicMock, patch

from llm.agent import run_agent


def test_agent_requires_api_key():
    with patch("llm.agent.Client") as mock_client:
        with patch("llm.agent.os.getenv", return_value=None):
            with patch("llm.agent.config.GEMINI_API_KEY", None):

                try:
                    run_agent("What is the vision of GECBH?")
                    assert False, "Expected ValueError"
                except ValueError as exc:
                    assert "GEMINI_API_KEY" in str(exc)

                mock_client.assert_not_called()


def test_agent_returns_answer_from_gemini():
    fake_response = MagicMock()

    fake_response.function_calls = []

    fake_response.text = "GECBH aims to excel in higher learning."

    mock_client_instance = MagicMock()
    mock_client_instance.models.generate_content.return_value = fake_response

    with patch("llm.agent.Client", return_value=mock_client_instance):
        with patch(
            "llm.agent.os.getenv",
            return_value="fake-api-key",
        ):

            result = run_agent("What is the vision of GECBH?")

    assert result["answer"] == "GECBH aims to excel in higher learning."
    assert result["tool_name"] is None
    assert result["source_url"] is None
    
def test_agent_handles_empty_gemini_response():
    fake_response = MagicMock()

    fake_response.function_calls = []
    fake_response.text = ""

    mock_client_instance = MagicMock()
    mock_client_instance.models.generate_content.return_value = fake_response

    with patch("llm.agent.Client", return_value=mock_client_instance):
        with patch(
            "llm.agent.os.getenv",
            return_value="fake-api-key",
        ):

            result = run_agent("What is my current GPA?")

    assert "could not be found" in result["answer"].lower()
    assert result["tool_name"] is None
    assert result["source_url"] is None