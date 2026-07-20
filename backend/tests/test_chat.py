from unittest.mock import patch
from fastapi.testclient import TestClient

def test_agentic_chat_query_endpoint(client: TestClient):
    """
    Validates that incoming chat routing structures execute smoothly 
    by intercepting and mocking the internal LangGraph engine invocation layer.
    """
    # Define a static, deterministic mock payload to substitute for the Gemini network response
    mocked_graph_output = {
        "messages": [
            type('Message', (object,), {"content": "Mocked AI output response: Ceylon cinnamon is available."})()
        ]
    }

    # Intercept the agent graph invoke pipeline completely using unittest patch
    with patch("app.api.endpoints.chat.agent_graph.invoke", return_value=mocked_graph_output):
        chat_request = {
            "message": "Is Ceylon Cinnamon currently available in your catalog?",
            "session_id": None
        }
        
        response = client.post("/api/v1/chat/query", json=chat_request)
        
        assert response.status_code == 200
        response_data = response.json()
        assert "session_id" in response_data
        assert "Ceylon cinnamon is available" in response_data["response"]