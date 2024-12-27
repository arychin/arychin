from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased
from typing import Optional, List
from uuid import UUID
import logging
from projectservice.schemas.files import FilesSchema, FilePaginationSchema
from projectservice.models import Files
from projectservice.database import get_db
from projectservice.utils.pagination import paginatefiles
from projectservice.utils.rbac import has_permissions

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix='/files',
    tags=['Files'],
    dependencies=[Depends(has_permissions("read_files"))]
    )


@router.get('/', response_model=FilePaginationSchema)
def read_files(
        db: Session = Depends(get_db),
        search: Optional[str] = Query(None, description="Search term for file_name or desired_file_output"),
        year_start: Optional[int] = Query(None, description="Start year for filtering"),
        year_end: Optional[int] = Query(None, description="End year for filtering"),
        latest_version: bool = Query(True, description="Filter by latest version"),
        limit: int = Query(10, ge=1, description="Number of files to return"),
        offset: int = Query(0, ge=0, description="Starting position to fetch files"),
):
    query = db.query(Files)
    logger.info(f"Received query: {query}")

    # Search functionality
    if search:
        query = query.filter(
            (Files.desired_file_output.ilike(f"%{search}%")) |
            (Files.file_name.ilike(f"%{search}%"))
        )

    # Filter by year range
    if year_start and year_end:
        query = query.filter(Files.year.between(year_start, year_end))
    elif year_start:
        query = query.filter(Files.year >= year_start)
    elif year_end:
        query = query.filter(Files.year <= year_end)
    
    # Filter by latest version
    if latest_version:
        subquery = (
            db.query(Files.file_name, Files.desired_file_output, func.max(Files.version).label("latest_version"),)
            .group_by(Files.file_name, Files.desired_file_output)
            .subquery()
        )
        query = query.filter((Files.file_name == subquery.c.file_name) & 
                             (Files.desired_file_output == subquery.c.desired_file_output) & 
                             (Files.version == subquery.c.latest_version))
        
    # Sorting (default by file_name ascending)
    query = query.order_by(Files.file_name.asc())

    # Count total items for pagination
    total  = query.count()

    # Fetch paginated items
    files = query.offset(offset).limit(limit).all()

    # Convert SQLAlchemy objects to Pydantic models
    files_data = [FilesSchema.model_validate(file, from_attributes=True) for file in files if file is not None]

    # Return paginated response
    return paginatefiles(files=files_data, total=total, limit=limit, offset=offset)