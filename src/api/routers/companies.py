from fastapi import APIRouter

router = APIRouter(
    tags=["Companies"]
)

@router.get("/companies")
def companies():
    return {
        "message": "Companies endpoint"
    }