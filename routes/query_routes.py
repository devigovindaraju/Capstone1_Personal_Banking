from fastapi import APIRouter

from services.query_services import process_query

router = APIRouter(prefix="/api/v1/advisor")


@router.post("/")
def query(request: dict):
    return process_query(request)
