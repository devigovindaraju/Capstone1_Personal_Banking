from fastapi import FastAPI

from routes.upload_routes import router as upload_router
from routes.query_routes import router as query_router

app = FastAPI(title="Customer 360 Financial Advisor API")


@app.get("/")
def root():
    return "Hello World"


app.include_router(upload_router)
app.include_router(query_router)
