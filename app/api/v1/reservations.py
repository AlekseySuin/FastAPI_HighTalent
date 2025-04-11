from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.reservation import ReservationBase
from app.services.reservation import ReservationService
from app.core.database import get_db

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.get("/", response_model=list[ReservationBase])
def get_reservations(db: Session = Depends(get_db)):
    reservations = ReservationService.get_all_reservations(db)
    return reservations


@router.post("/", status_code=201)
def create_reservation(reservation_data: ReservationBase,
                       db: Session = Depends(get_db)
                       ):
    try:
        new_reservation = ReservationService.create_reservation(db, reservation_data)
        # return new_reservation
        return {"message": "Бронь успешно создана",
                "reservation_id": new_reservation.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=str(e))


@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    ReservationService.delete_reservation(db, reservation_id)
    return True
