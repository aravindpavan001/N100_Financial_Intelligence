from fastapi import APIRouter

router = APIRouter(
    tags=["Screener"]
)

@router.get("/screener")
def screener():
    return {
        "message": "Screener endpoint"
    }