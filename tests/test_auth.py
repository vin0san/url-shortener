from app.models import User
from app.auth import hash_password

def test_user_registration(client):
    response = client.post("/auth/register", json={
        "email": "jose@yahoo.com",
        "password": "jose-the-great"
    })
    assert response.status_code == 200

def test_alreadyregistred_user_re_registration(client, db):
    user = User(
        email="jose@yahoo.com",
        pass_hash = hash_password("jose-the-great")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    response = client.post("/auth/register", json={
        "email": "jose@yahoo.com",
        "password": "jose-the-great"
    })
    assert response.status_code == 400

def test_user_login_with_wrong_password(client, db):
    user = User(
        email="jose@yahoo.com",
        pass_hash = hash_password("jose-the-great")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    response = client.post("/auth/login", json={
        "email": "jose@yahoo.com",
        "password": "jose123"
    })
    assert response.status_code == 401

def test_user_login_with_wrong_email(client, db):
    user = User(
        email="jose@yahoo.com",
        pass_hash = hash_password("jose-the-great")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    response = client.post("/auth/login", json={
        "email": "jose@gmail.com",
        "password": "jose-the-great"
    })
    assert response.status_code == 401

def test_user_login_with_correct_credentials(client, db):
    user = User(
        email="jose@yahoo.com",
        pass_hash = hash_password("jose-the-great")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    response = client.post("/auth/login", json={
        "email": "jose@yahoo.com",
        "password": "jose-the-great"
    })
    assert response.status_code == 200

