from fastapi import FastAPI
from core.config import settings
from starlette.middleware.base import BaseHTTPMiddleware

from api.router import router

app = FastAPI(title=settings.title,
              version=settings.version,
              description=settings.description,
              docs_url=settings.docs_url,
              redoc_url=settings.redoc_url,
              openapi_url=settings.openapi_url,)



class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers['Cache-Control'] = 'no-store'
        return response

app.add_middleware(NoCacheMiddleware)
app.include_router(router, prefix=settings.api_prefix)

@app.get("/")
async def root():
    return {"Say": "Hello!"}
