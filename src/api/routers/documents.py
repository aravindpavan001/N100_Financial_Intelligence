from fastapi import (
    APIRouter,
    HTTPException
)

router = APIRouter(
    tags=["Documents"]
)


@router.get("/companies/{ticker}/documents")
def get_documents(
    ticker: str
):

    raise HTTPException(

        status_code=501,

        detail="Documents dataset is not available in the current database."

    )