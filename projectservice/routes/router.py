from fastapi import APIRouter, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer

from projectservice.config import settings
from projectservice.routes import (
    project, projects, files, file, sample_project
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl=settings.auth_token_url,
    scheme_name=settings.auth_schema,
    authorizationUrl=settings.auth_url,
    )

api_router = APIRouter(
    tags=["all"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme),],
)

api_router.include_router(sample_project.router) # Not to be used. Obsolete and code will be removed soon
api_router.include_router(projects.router) # Not to be used. Obsolete and code will be removed soon
api_router.include_router(files.router) # Not to be used. Obsolete and code will be removed soon
api_router.include_router(file.router)
api_router.include_router(project.router)
