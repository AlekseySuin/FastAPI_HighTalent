from datetime import datetime, timedelta
import pytest


def test_create_reservation(client, db):
    test_data = {
        "customer_name": "Иван Тестов",
        "table_id": 1,
        "reservation_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "duration_minutes": 60
    }

    response = client.post("/reservations/", json=test_data)
    assert response.status_code == 201
    data = response.json()
    assert "reservation_id" in data
    assert data["customer_name"] == test_data["customer_name"]


def test_get_reservations(client, db):
    response = client.get("/reservations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_conflicting_reservation(client, db):
    time = (datetime.now() + timedelta(days=1)).isoformat()

    # Первая бронь
    client.post("/reservations/", json={
        "customer_name": "Первый Клиент",
        "table_id": 1,
        "reservation_time": time,
        "duration_minutes": 60
    })

    # Конфликтующая бронь
    response = client.post("/reservations/", json={
        "customer_name": "Второй Клиент",
        "table_id": 1,
        "reservation_time": time,
        "duration_minutes": 30
    })

    assert response.status_code == 409
    assert "уже занят" in response.json()["detail"]