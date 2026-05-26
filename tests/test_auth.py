def test_register_duplicate_email(client):

    user_data = {
        "email": "duplicate@test.com",
        "password": "123456"
    }

    response_1 = client.post(
        "/auth/register",
        json=user_data
    )

    response_2 = client.post(
        "/auth/register",
        json=user_data
    )

    assert response_2.status_code == 400


def test_login_user(client):

    user_data = {
        "email": "login@test.com",
        "password": "123456"
    }

    # registrar usuario
    client.post(
        "/auth/register",
        json=user_data
    )

    login_data = {
        "username": "login@test.com",
        "password": "123456"
    }

    response = client.post(
        "/auth/login",
        data=login_data
    )

    assert response.status_code == 200

def test_get_current_user(client):

    user_data = {
        "email": "me@test.com",
        "password": "123456"
    }

    # registrar usuario
    client.post(
        "/auth/register",
        json=user_data
    )

    # login
    #Se usa username y no email porque es lo que nos pide OAuth2PasswordRequestForm
    login_data = {
        "username": "me@test.com",
        "password": "123456"
    }

    login_response = client.post(
        "/auth/login",
        data=login_data
    )

    token = login_response.json()["access_token"]

    # headers JWT
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # endpoint protegido
    response = client.get(
        "/auth/me",
        headers=headers
    )

    assert response.status_code == 200

def test_create_client(client):

    # ---------------- REGISTER ----------------

    user_data = {
        "email": "client@test.com",
        "password": "123456"
    }

    client.post(
        "/auth/register",
        json=user_data
    )

    # ---------------- LOGIN ----------------

    login_data = {
        "username": "client@test.com",
        "password": "123456"
    }

    login_response = client.post(
        "/auth/login",
        data=login_data
    )

    token = login_response.json()["access_token"]

    # ---------------- AUTH HEADERS ----------------

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # ---------------- CREATE CLIENT ----------------

    response = client.post(
        "/clients/",
        json={
            "name": "Genesis",
            "email": "genesis@test.com",
            "phone": "123456789"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Genesis"

from models.user import User


def test_create_service(client, session):

    # ---------------- REGISTER ----------------

    user_data = {
        "email": "service@test.com",
        "password": "123456"
    }

    client.post(
        "/auth/register",
        json=user_data
    )

    # ---------------- CONVERT USER TO ADMIN ----------------

    user = session.query(User).filter(
        User.email == "service@test.com"
    ).first()

    user.is_admin = True

    session.add(user)
    session.commit()

    # ---------------- LOGIN ----------------

    login_data = {
        "username": "service@test.com",
        "password": "123456"
    }

    login_response = client.post(
        "/auth/login",
        data=login_data
    )

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # ---------------- CREATE SERVICE ----------------

    response = client.post(
        "/services/",
        json={
            "name": "Maderoterapia",
            "price": 100,
            "duration_minutes": 60
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Maderoterapia"

from models.user import User


def test_create_appointment(client, session):

    # ---------------- REGISTER ----------------

    user_data = {
        "email": "appointment@test.com",
        "password": "123456"
    }

    client.post(
        "/auth/register",
        json=user_data
    )

    # ---------------- MAKE ADMIN ----------------

    user = session.query(User).filter(
        User.email == "appointment@test.com"
    ).first()

    user.is_admin = True

    session.add(user)
    session.commit()

    # ---------------- LOGIN ----------------

    login_data = {
        "username": "appointment@test.com",
        "password": "123456"
    }

    login_response = client.post(
        "/auth/login",
        data=login_data
    )

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # ---------------- CREATE CLIENT ----------------

    client_response = client.post(
        "/clients/",
        json={
            "name": "Genesis",
            "email": "genesis@test.com",
            "phone": "123456789"
        },
        headers=headers
    )

    client_id = client_response.json()["id"]

    # ---------------- CREATE SERVICE ----------------

    service_response = client.post(
        "/services/",
        json={
            "name": "Maderoterapia",
            "price": 100,
            "duration_minutes": 60
        },
        headers=headers
    )

    service_id = service_response.json()["id"]

    # ---------------- CREATE APPOINTMENT ----------------

    response = client.post(
        "/appointments/",
        json={
            "client_id": client_id,
            "appointment_date": "2027-05-25T15:00:00",
            "notes": "Primera cita",
            "service_ids": [service_id]
        },
        headers=headers
    )

    assert response.status_code == 200