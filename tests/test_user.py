from app.auth import hash_password
from app.models import User, Url

def test_get_user_urls_returns_401_without_auth(client):
    response = client.get("/user/urls")
    assert response.status_code == 401


    
def test_get_user_urls_returns_only_own_urls(client, db):
    user = User(
        email="jose@yahoo.com",
        pass_hash = hash_password("jose-the-great")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    login_response = client.post("/auth/login", json={
        "email": "jose@yahoo.com",
        "password": "jose-the-great"
    })
    token1 = login_response.json()["access_token"]

    payload = {"long_url": "https://example.com", "custom_key": "dup-key"}
    client.post("/shorten", json=payload, headers={"Authorization": f"Bearer {token1}"})

    user2 = User(
        email="jose02@yahoo.com",
        pass_hash = hash_password("jose-the-greatest")
    )
    db.add(user2)
    db.commit()
    db.refresh(user2)
    login_response2 = client.post("/auth/login", json={
        "email": "jose02@yahoo.com",
        "password": "jose-the-greatest"
    })
    token2 = login_response2.json()["access_token"]

    payload = {"long_url": "https://example-jose.com", "custom_key": "jose-key"}
    client.post("/shorten", json=payload, headers={"Authorization": f"Bearer {token2}"})

    response = client.get("/user/urls", headers={"Authorization": f"Bearer {token1}"})
    assert response.status_code == 200
    body = response.json()

    assert len(body) == 1
    assert body[0]["short_key"] == "dup-key"

def test_get_url_analytics_returns_correct_data(client, db):
    user = User(
        email="jose@yahoo.com",
        pass_hash = hash_password("jose-the-great")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    login_response = client.post("/auth/login", json={
        "email": "jose@yahoo.com",
        "password": "jose-the-great"
    })
    token = login_response.json()["access_token"]

    payload = {"long_url": "https://example.com", "custom_key": "dup-key"}
    client.post("/shorten", json=payload, headers={"Authorization": f"Bearer {token}"})
    client.get("/dup-key")
    client.get("/dup-key")
    client.get("/dup-key")
    query = db.query(Url.short_key, Url.id).filter(Url.short_key == "dup-key").first()
    response = client.get(f"/urls/{query.id}/analytics", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert body["total_clicks"] == 3
    assert len(body["daily_breakdown"]) == 1
    assert body["daily_breakdown"][0]["count"] == 3