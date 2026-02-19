def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Eonix Backend is running"}

def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_execute_command(client, mocker):
    # Mock the orchestrator to avoid actual AI/Execution calls
    mocker.patch('api.routes.orchestrator.process_command', return_value={
        "response": "Executed",
        "intent": "test",
        "data": {}
    })
    
    response = client.post("/api/command", json={"command": "test command"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "response" in data["data"]
