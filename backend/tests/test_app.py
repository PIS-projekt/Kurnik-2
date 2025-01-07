from fastapi.testclient import TestClient

from src.psi_backend.app import app

client = TestClient(app)


# Test root endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


# Test join room failure
def test_join_room_failure(monkeypatch):
    def mock_check_room_exists(_):
        return False

    monkeypatch.setattr(
        "src.psi_backend.websocket_chat.room_assignment.check_room_exists",
        mock_check_room_exists,
    )

    response = client.get("/join-room", params={"room_code": "ABC123", "user_id": 1234})

    assert response.status_code == 404
    assert response.json() == {"detail": "Room not found."}
