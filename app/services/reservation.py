from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.reservation import ReservationBase
from app.models.table import Table
from app.models.reservation import Reservation
from datetime import datetime, timezone
from datetime import timedelta
from sqlalchemy.sql import func
from sqlalchemy import or_, and_
from pytz import UTC


class ReservationService:
    @staticmethod
    def validate_reservation_data(db: Session, data: ReservationBase):
        if data.duration_minutes <= 0:
            raise HTTPException(
                status_code=422,
                detail="Длительность бронирования должна быть положительной"
            )
        current_time = datetime.now(timezone.utc)
        if data.reservation_time < current_time:
            raise HTTPException(
                status_code=422,
                detail="Невозможно забронировать стол в прошлом"
            )
        if not db.query(Table).filter(Table.id == data.table_id).first():
            raise HTTPException(
                status_code=404,
                detail=f"Столик {data.table_id} не существует"
            )
        if ReservationService.is_table_reserved(db, data):
            raise HTTPException(
                status_code=404,
                detail=f"Столик {data.table_id} уже занят в это время. Выберите другой стол или время"
            )

    @staticmethod
    def is_reserved_exists(db: Session, reservation_id: int):
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if not reservation:
            raise HTTPException(
                status_code=404,
                detail="Бронь не найдена"
            )
        return reservation

    @staticmethod
    def is_table_reserved(db: Session, current_reservation: ReservationBase) -> bool:
        # Приводим время к UTC (aware datetime)
        start_time = current_reservation.reservation_time
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)

        end_time = start_time + timedelta(minutes=current_reservation.duration_minutes)

        # Создаем подзапрос для проверки пересечений временных интервалов
        conflicting_reservations = db.query(Reservation).filter(
            Reservation.table_id == current_reservation.table_id,
            func.date(func.timezone('UTC', Reservation.reservation_time)) == func.date(start_time),
            func.timezone('UTC', Reservation.reservation_time) < end_time,
            func.timezone('UTC', Reservation.reservation_time) +
            func.make_interval(0, 0, 0, 0, 0, Reservation.duration_minutes, 0) > start_time
        )

        # Проверяем существование конфликтующих бронирований
        return db.query(conflicting_reservations.exists()).scalar()

    @staticmethod
    def get_all_reservations(db: Session):
        return db.query(Reservation).all()

    @staticmethod
    def delete_reservation(db: Session, reservation_id: int):
        reservation = ReservationService.is_reserved_exists(db, reservation_id)
        db.delete(reservation)
        db.commit()
        return True

    @classmethod
    def create_reservation(cls, db: Session, data: ReservationBase):
        cls.validate_reservation_data(db, data)

        new_reservation = Reservation(
            customer_name=data.customer_name,
            table_id=data.table_id,
            reservation_time=data.reservation_time,
            duration_minutes=data.duration_minutes
        )
        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)
        return new_reservation