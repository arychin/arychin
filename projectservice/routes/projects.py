from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, aliased
from typing import Optional, List
from uuid import UUID
import logging
from projectservice.schemas.projects import ProjectsSchema, ProjectPaginationSchema
from projectservice.models import Projects, ProjectStatus, Methodologies
from projectservice.database import get_db
from projectservice.utils.pagination import paginateprojects
from projectservice.utils.rbac import has_permissions

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/projects',
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
        country: Optional[List[str]] = Query(None, description="Filter by multiple countries"),
        state: Optional[List[str]] = Query(None, description="Filter by multiple states"),
        sort_by: Optional[str] = Query("project_name", description="Field to sort by (default: project_name)"),
        sort_order: Optional[str] = Query("asc", description="Sort order: asc or desc (default: asc)"),
):
    logger.info(f"Received countries: {country}")
    query = db.query(Projects)

    # Aliases for Status table to filter by status value
    StatusAlias = aliased(ProjectStatus)
    MethodologyAlias = aliased(Methodologies)

    # Search functionality
    if search:
        query = query.filter(
            (Projects.project_id.ilike(f"%{search}%")) |
            (Projects.project_name.ilike(f"%{search}%")) |
            (Projects.project_code.ilike(f"%{search}%"))
        )

    # Join with Status table to filter by status value
    if status:
        query = query.join(StatusAlias, Projects.status == StatusAlias.id)
        query = query.filter(StatusAlias.value.in_(status))
    
    # Join with Methodology table to filter by methodology value
    if methodology:
        query = query.join(MethodologyAlias, Projects.methodology == MethodologyAlias.id)
        query = query.filter(MethodologyAlias.value.in_(methodology))

    # Filter functionality for other fields
    if project_manager:
        query = query.filter(Projects.project_manager.in_(project_manager))
    if country:
        query = query.filter(Projects.country.in_(country))
    if state:
        query = query.filter(Projects.state.in_(state))

    # Sorting functionality
    sort_column = getattr(Projects, sort_by, None)

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
    projects_data = [ProjectsSchema.model_validate(project, from_attributes=True) for project in projects if project is not None]

    # Return paginated response
    return paginateprojects(projects=projects_data, total=total, limit=limit, offset=offset)
