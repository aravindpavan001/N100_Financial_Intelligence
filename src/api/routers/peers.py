from fastapi import APIRouter

router = APIRouter(
    tags=["Peers"]
)

@router.get("/peers")
def peers():
    return {
        "message": "Peers endpoint"
    }