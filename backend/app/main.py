from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, monitor


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(monitor.router)


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Backend Running Successfully"}
