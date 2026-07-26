from fastapi import APIRouter

router = APIRouter(
    tags=["Sectors"]
)

@router.get("/sectors")
def sectors():
    return {
        "message": "Sectors endpoint"
    }