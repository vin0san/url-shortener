from app.models import User, Url
from app.auth import hash_password, get_optional_user

def test_shorten_generates_key_when_no_custom_key(client):
    response = client.post("/shorten", json={"long_url": "https://example.com"})
    assert response.status_code == 200
    body = response.json()
    assert body["custom_key"]
    assert body["short_url"].endswith(body["custom_key"])
    assert body["expires_at"] is not None


def test_shorten_accepts_valid_custom_key(client):
    response = client.post("/shorten", json={
        "long_url": "https://example.com",
        "custom_key": "my-link"
    })
    assert response.status_code == 200
    assert response.json()["custom_key"] == "my-link"


def test_shorten_rejects_duplicate_custom_key(client):
    payload = {"long_url": "https://example.com", "custom_key": "dup-key"}
    first = client.post("/shorten", json=payload)
    assert first.status_code == 200

    second = client.post("/shorten", json=payload)
    assert second.status_code == 400


def test_shorten_rejects_reserved_key(client):
    response = client.post("/shorten", json={
        "long_url": "https://example.com",
        "custom_key": "admin"
    })
    assert response.status_code == 400


def test_shorten_rejects_invalid_custom_key_format(client):
    bad_payloads = [
        {"long_url": "https://example.com", "custom_key": "ab"},
        {"long_url": "https://example.com", "custom_key": "way-too-long-key"},
        {"long_url": "https://example.com", "custom_key": "has space"},
    ]
    for payload in bad_payloads:
        response = client.post("/shorten", json=payload)
        assert response.status_code == 422


def test_shorten_rejects_invalid_expiration_days(client):
    response = client.post("/shorten", json={
        "long_url": "https://example.com",
        "expiration_days": -10,
        "custom_key": "abc345"
    })
    assert response.status_code == 422
    response = client.post("/shorten", json={
        "long_url": "https://example.com",
        "expiration_days": 400,
        "custom_key": "def678"
    })
    assert response.status_code == 422


def test_shorten_rejects_malformed_long_url(client):
    response = client.post("/shorten", json={
        "long_url": "ht/tps:///example.com",
        "expiration_days": 40,
        "custom_key": "def678"
    })
    assert response.status_code == 422


def test_shorten_no_expiration_when_expiration_days_null(client):
    response = client.post("/shorten", json={
        "long_url": "https://example.com",
        "expiration_days": None,
        "custom_key": "def678"
    })
    assert response.status_code == 200
    body = response.json()
    assert body["expires_at"] is None

def test_shorten_sets_user_id_when_authenticated(client, db):
    user = User(email="jose@yahoo.com", pass_hash=hash_password("jose-the-great"))
    db.add(user)
    db.commit()
    db.refresh(user)

    login_response = client.post("/auth/login", json={
        "email": "jose@yahoo.com",
        "password": "jose-the-great"
    })
    token = login_response.json()["access_token"]

    response = client.post("/shorten", json={
        "long_url": "https://example.com",
        "expiration_days": None,
        "custom_key": "def678"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    url_query = db.query(Url.user_id).filter(Url.short_key == "def678").first()
    assert url_query.user_id == user.id