from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes import auth, monitor


app = FastAPI()
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
FRONTEND_FILE = FRONTEND_DIR / "AGRI.html"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(monitor.router)

app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


@app.get("/health")
def health() -> dict[str, str]:
    return {"message": "Backend Running Successfully"}


@app.get("/")
def frontend_home() -> FileResponse:
    return FileResponse(FRONTEND_FILE)


@app.get("/app")
def frontend_app() -> FileResponse:
    return FileResponse(FRONTEND_FILE)
