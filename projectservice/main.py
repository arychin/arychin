import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from asgi_correlation_id import CorrelationIdMiddleware
from projectservice.config import settings
from projectservice.middleware.authorization import AuthorizationMiddleware
from projectservice.middleware.time_and_log import TimeAndLogItMiddleware
from projectservice.exceptions.exceptions import add_exceptions_handlers
from projectservice.routes.router import api_router


app = FastAPI(debug=settings.debug)

app.include_router(api_router)
app.add_middleware(
    AuthorizationMiddleware,
    exposed_paths=['/docs', '/redoc', '/openapi.json'],
)
app.add_middleware(TimeAndLogItMiddleware)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)
add_exceptions_handlers(app)


if __name__ in '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)