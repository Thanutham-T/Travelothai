from fastapi import FastAPI
from . import routers

app = FastAPI(title="TraveloThai API", version="1.0.0")
app.include_router(routers.router)
