from fastapi import FastAPI
from src.api.auth_router import router as auth_router
from src.api.tasks_router import router as tasks_router
from src.dependencies import get_current_user
from src.models.user import User
from contextlib import asynccontextmanager
from src.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_db_and_tables()
    yield
    # Cleanup on shutdown (if needed)

app = FastAPI(title="Todo API", version="1.0.0", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

# Register routers
app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)