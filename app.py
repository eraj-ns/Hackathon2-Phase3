from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.api.auth_router import router as auth_router
from src.api.tasks_router import router as tasks_router
from src.database import create_db_and_tables
from src.dependencies import get_current_user
from src.models.user import User
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_db_and_tables()
    yield

app = FastAPI(title="Todo API", version="1.0.0", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/test-auth")
def test_auth(current_user: User = Depends(get_current_user)):
    return {"user_id": current_user.id, "email": current_user.email}

# Register routers
app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# For Hugging Face Spaces, we need to use the PORT environment variable
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)