from fastapi import FastAPI
from app.database import Base, engine
from app.routes.auth_routes import router

app = FastAPI(title="Auth Backend with Redis")

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Auth Backend Running"}
