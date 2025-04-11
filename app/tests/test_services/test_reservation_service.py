import pytest
from datetime import datetime, timedelta
from app.services.reservation import ReservationService
from app.schemas.reservation import ReservationBase
from app.models.reservation import Reservation


def test_is_table_reserved(db):
    """Тест проверки занятости столика"""
    now = datetime.utcnow()

    # Создаем тестовую бронь
    test_reservation = Reservation(
        customer_name="Тест",
        table_id=1,
        reservation_time=now + timedelta(hours=1),
        duration_minutes=60
    )
    db.add(test_reservation)
    db.commit()

    # Проверяем тот же столик в то же время
    test_data = ReservationBase(
        customer_name="Новый Клиент",
        table_id=1,
        reservation_time=now + timedelta(minutes=30),
        duration_minutes=30
    )

    assert ReservationService.is_table_reserved(db, test_data) is True


def test_create_reservation_service(db):
    """Тест создания брони через сервис"""
    now = datetime.utcnow()

    test_data = ReservationBase(
        customer_name="Сервис Тест",
        table_id=2,
        reservation_time=now + timedelta(minutes=30),
        duration_minutes=90
    )

    result = ReservationService.create_reservation(db, test_data)

    assert result.id is not None
    assert db.query(Reservation).filter(Reservation.id == result.id).first() is not None