from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, aliased
from typing import Optional, List
from uuid import UUID
import logging
from projectservice.schemas.project import ProjectSchema, ProjectPaginationSchema
from projectservice.models import Project, ProjectProperties
from projectservice.database import get_db
from projectservice.utils.pagination import paginateprojects
from projectservice.utils.rbac import has_permissions

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/project',
    tags=['Project'],
    dependencies=[Depends(has_permissions("read_projects"))]
    )


@router.get('/', response_model=ProjectPaginationSchema)
def read_projects(
        db: Session = Depends(get_db),
        limit: int = Query(10, ge=1, description="Number of projects to return"),
        offset: int = Query(0, ge=0, description="Starting position to fetch projects"),
        search: Optional[str] = Query(None, description="Search term for filtering projects by project_name or project_code"),
        status: Optional[List[str]] = Query(None, description="Filter by multiple status (values)"),
        methodology: Optional[List[str]] = Query(None, description="Filter by multiple methodology (values)"),
        project_manager: Optional[List[str]] = Query(None, description="Filter by multiple project managers"),
        project_id: Optional[List[str]] = Query(None, description="Filter by multiple project ids"),
        country: Optional[List[str]] = Query(None, description="Filter by multiple countries"),
        state: Optional[List[str]] = Query(None, description="Filter by multiple states"),
        sort_by: Optional[str] = Query("project_name", description="Field to sort by (default: project_name)"),
        sort_order: Optional[str] = Query("asc", description="Sort order: asc or desc (default: asc)"),
):
    logger.info(f"Received query params: search={search}, status={status}, methodology={methodology}, project_manager={project_manager}, project_id: {project_id}, state: {state}, country: {country}")
    query = db.query(Project)

    # Aliases for ProjectProperties table
    StatusAlias = aliased(ProjectProperties)
    MethodologyAlias = aliased(ProjectProperties)
    ProjectManagerAlias = aliased(ProjectProperties)
    ProjectCodeAlias = aliased(ProjectProperties)

    # Search functionality
    if search:
        query = query.outerjoin(ProjectCodeAlias, Project.id == ProjectCodeAlias.project_id)
        query = query.filter(
            (Project.project_id.ilike(f"%{search}%")) |
            (Project.project_name.ilike(f"%{search}%")) |
            ((ProjectCodeAlias.name == "project_code") & (ProjectCodeAlias.value.ilike(f"%{search}%")))
        )

    # Project id filter


    # Filter by status (stored in ProjectProperties)
    if status:
        query = query.join(StatusAlias, Project.id == StatusAlias.project_id)
        query = query.filter((StatusAlias.name == "Status") & 
                             (StatusAlias.value.in_(status)))
    
    # Filter by methodology (stored in ProjectProperties)
    if methodology:
        query = query.join(MethodologyAlias, Project.id == MethodologyAlias.project_id)
        query = query.filter((MethodologyAlias.name == "Methodology") & 
                             (MethodologyAlias.value.in_(methodology)))

    # Filter by project manager (stored in ProjectProperties)
    if project_manager:
        query = query.join(ProjectManagerAlias, Project.id == ProjectManagerAlias.project_id)
        query = query.filter((ProjectManagerAlias.name == "Project Manager") & 
                             (ProjectManagerAlias.value.in_(project_manager)))
        
    # Filter by project id
    if project_id:
        query = query.filter(Project.project_id.in_(project_id))

    # Filter by country
    if country:
        query = query.filter(Project.country.in_(country))

    # Filter by state
    if state:
        query = query.filter(Project.state.in_(state))

    # Sorting functionality
    sort_column = getattr(Project, sort_by, None)

    if sort_column is not None:
        if sort_order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

    # Count total items for pagination
    total  = query.count()

    # Fetch paginated items
    projects = query.offset(offset).limit(limit).all()

    # Convert SQLAlchemy objects to Pydantic models
    projects_data = [ProjectSchema.model_validate(project, from_attributes=True) for project in projects if project is not None]

    # Return paginated response
    return paginateprojects(data=projects_data, total=total, limit=limit, offset=offset)
