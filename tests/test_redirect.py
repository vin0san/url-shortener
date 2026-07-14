from app.models import Url
from datetime import timedelta, datetime, timezone

def test_redirect_nonexistent_key_returns_404(client):
    response = client.get("/this-key-should-not-exist")
    assert response.status_code == 404

def test_redirect_expired_link_returns_410(client, db):
    url = Url(
        long_url="https://example.com",
        short_key="abc345",
        expires_at= datetime.now(timezone.utc) - timedelta(days=10)
    )
    db.add(url)
    db.commit()
    db.refresh(url)
    response = client.get("/abc345")
    assert response.status_code == 410

def test_redirect_active_link_returns_307(client, db):
    url = Url(
        long_url="https://example.com",
        short_key="abc456",
        expires_at= datetime.now(timezone.utc) + timedelta(days=10)
    )
    db.add(url)
    db.commit()
    db.refresh(url)
    response = client.get("/abc456")
    assert response.status_code == 307