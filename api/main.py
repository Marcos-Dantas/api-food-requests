from fastapi import FastAPI, Depends
from api.routers import secure
from api.auth import check_api_key
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    secure.router,
    prefix="/api/v1/secure",
    dependencies=[Depends(check_api_key)]
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )