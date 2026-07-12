def test_root_returns_app_info(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["App"] == "Url Shortener"
    assert body["Version"] == "1.0"

def test_health_check_success(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["database"] == "connected"
    assert body["version"] == "1.0" 
