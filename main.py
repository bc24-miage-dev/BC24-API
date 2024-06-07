from fastapi import FastAPI
from core.config import settings

from api.router import router

app = FastAPI(title=settings.title,
              version=settings.version,
              description=settings.description,
              docs_url=settings.docs_url,
              redoc_url=settings.redoc_url,
              openapi_url=settings.openapi_url,)

app.include_router(router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    return {"Say": "Hello!"}
