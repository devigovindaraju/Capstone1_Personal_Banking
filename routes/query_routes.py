from fastapi import APIRouter

from services.query_services import process_query

router = APIRouter()


@router.post("/query")
def query(request: dict):
    return process_query(request)
