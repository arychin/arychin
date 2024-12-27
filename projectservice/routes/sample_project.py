from fastapi import APIRouter, Depends, HTTPException
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from projectservice.schemas.sample_project import (
    ProjectListResponse,
    ProjectData
)

router = APIRouter(
    prefix='/sample_project',
    tags=['Sample Projects'],
    responses={404: {"description": "Not found"}},
)

@router.get('/', response_model=ProjectListResponse)
def get_list_of_projects():
    
    project = ProjectData()
    project.project_name='P1'

    return {
        'status': 'Success',
        'error': None,
        'data': {
            'page': 1,
            'pageSize': 10,
            'totalRecords': 100,
            'result': [project],
        },
    }