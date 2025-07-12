from fastapi import APIRouter
from . import (
    province_router,
    hotel_router,
    ticket_router,
    # booking_router,
    # user_router,
)

router = APIRouter(prefix="/v1")
router.include_router(province_router.router)
router.include_router(hotel_router.router)
router.include_router(ticket_router.router)
# router.include_router(booking_router.router)
# router.include_router(user_router.router)
