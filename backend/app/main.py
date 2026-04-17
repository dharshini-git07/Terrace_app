from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, monitor

# ✅ create app (VERY IMPORTANT)
app = FastAPI()

# ✅ allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ include routes
app.include_router(auth.router)
app.include_router(monitor.router)

# ✅ test route
@app.get("/")
def home():
    return {"message": "Backend Running Successfully"}
