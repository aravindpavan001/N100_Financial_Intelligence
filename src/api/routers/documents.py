from fastapi import APIRouter

router = APIRouter(
    tags=["Documents"]
)

@router.get("/documents")
def documents():
    return {
        "message": "Documents endpoint"
    }