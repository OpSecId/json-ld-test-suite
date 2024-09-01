from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from config import settings
from app.routers import w3c_test_suites

app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)


api_router = APIRouter()

api_router.include_router(w3c_test_suites.router, tags=["W3C Test Suites"], prefix="/w3c")

@api_router.get("/server/status", tags=["Server"])
async def server_status(include_in_schema=False):
    return JSONResponse(status_code=200, content={"status": "ok"})


app.include_router(api_router)
