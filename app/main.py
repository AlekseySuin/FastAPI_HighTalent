import os

from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.v1 import reservations, tables

app = FastAPI()

app.include_router(reservations.router)
app.include_router(tables.router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

host = os.getenv("UVICORN_HOST", "0.0.0.0")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=host, port=8000)