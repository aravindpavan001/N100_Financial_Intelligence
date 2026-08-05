import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import (
    companies,
    documents,
    health,
    peers,
    portfolio,
    screener,
    sectors,
    valuation,
)

app = FastAPI(title="N100 Financial Intelligence API", version="1.0.0")

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# REQUEST LOGGING
# ==========================================================


@app.middleware("http")
async def log_requests(request, call_next):

    start = time.time()

    response = await call_next(request)

    duration = round((time.time() - start) * 1000, 2)

    print(
        f"{request.method}"
        f" {request.url.path}"
        f" {response.status_code}"
        f" {duration} ms"
    )

    return response


# ==========================================================
# REGISTER ROUTERS
# ==========================================================

app.include_router(health.router, prefix="/api/v1")

app.include_router(companies.router, prefix="/api/v1")

app.include_router(screener.router, prefix="/api/v1")

app.include_router(sectors.router, prefix="/api/v1")

app.include_router(peers.router, prefix="/api/v1")

app.include_router(valuation.router, prefix="/api/v1")

app.include_router(portfolio.router, prefix="/api/v1")

app.include_router(documents.router, prefix="/api/v1")


@app.get("/")
def root():

    return {"message": "N100 Financial Intelligence API", "version": "1.0.0"}
