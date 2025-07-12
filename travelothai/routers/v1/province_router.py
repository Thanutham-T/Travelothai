from fastapi import APIRouter

router = APIRouter(prefix="/provinces", tags=["provinces"])


@router.get("/")
def read_provinces():
    return {"message": "List of provinces"}