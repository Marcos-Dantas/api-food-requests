from fastapi import FastAPI, Depends
from routers import secure
from auth import check_api_key
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    secure.router,
    prefix="/api/v1/secure",
    dependencies=[Depends(check_api_key)]
)

# Configuração do CORS
origins = [
    "https://tech.redventures.com.br",
    # Adicione outras origens permitidas, se necessário
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
