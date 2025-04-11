from pydantic import BaseModel

class TableBase(BaseModel):
    name: str
    seats: int
    location: str

    class Config:
        orm_mode = True # Для совместимости с SqlAlchemy