from fastapi import FastAPI
from app.api.v1.endpoints import auth, me
from app.db.session import engine
from app.db.base import Base

# Buat tabel-tabel di database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(me.router, prefix="/api/v1/me", tags=["me"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)