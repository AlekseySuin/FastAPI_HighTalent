from fastapi import HTTPException, status
from datetime import datetime
from sqlalchemy.orm import Session
from app.schemas.table import TableBase
from app.models.table import Table
import datetime
from datetime import timedelta
from sqlalchemy.sql import func
from sqlalchemy import or_, and_

class TableService:
    @staticmethod
    def get_all_tables(db: Session):
        return db.query(Table).all()

    @staticmethod
    def validate_table_data(db: Session, data: TableBase):
        # Написано для примера и/или для будущего расширения
        if data.seats > 50:
            raise HTTPException(
                status_code=422,
                detail="Указано слишком много мест, измените"
            )


    def is_table_exists(db: Session, table_id: int):
        table = db.query(Table).filter(Table.id == table_id).first()
        if not table:
            raise HTTPException(
                status_code=404,
                detail="Стол не найден"
            )
        return table

    @staticmethod
    def delete_table(db: Session, table_id: int):
        table = TableService.is_table_exists(db, table_id)
        db.delete(table)
        db.commit()
        return True

    @classmethod
    def create_table(cls, db: Session, data: TableBase):
        cls.validate_table_data(db, data)

        new_table = Table(
            name=data.name,
            seats=data.seats,
            location=data.location
        )
        db.add(new_table)
        db.commit()
        db.refresh(new_table)
        return new_table
