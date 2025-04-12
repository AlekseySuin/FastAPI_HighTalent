from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from app.schemas.table import TableBase
from app.services.table import TableService

router = APIRouter(prefix="/tables", tags=["tables"])

@router.get("/")
def get_tables(db: Session = Depends(get_db)):
    tables = TableService.get_all_tables(db)
    return tables


@router.post("/")
def create_table(table_data: TableBase, db: Session = Depends(get_db)):
    try:
        new_table = TableService.create_table(db, table_data)
        #return new_table
        return {"message": "Новый стол успешно создан",
                "table_id": new_table.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=str(e))


@router.delete("/{table_id}")
def delete_table(table_id: int, db: Session = Depends(get_db)):
    TableService.delete_table(db, table_id)
    return True
