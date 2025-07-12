from fastapi import FastAPI
from contextlib import asynccontextmanager

from . import routers
from . import models


app = FastAPI(title="TraveloThai API", version="1.0.0")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database
    await models.init_db()
    yield
    # Close the database connection
    await models.close_db()


app = FastAPI(title="TraveloThai API", version="1.0.0", lifespan=lifespan)
app.include_router(routers.router)
