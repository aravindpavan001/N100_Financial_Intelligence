from fastapi import APIRouter

router = APIRouter(
    tags=["Portfolio"]
)

@router.get("/portfolio")
def portfolio():
    return {
        "message": "Portfolio endpoint"
    }