from fastapi import APIRouter, Depends, Query
from sqlalchemy.sql import cast
from sqlalchemy.types import Integer
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased
from typing import Optional, List
from uuid import UUID
import logging
from projectservice.schemas.file import FileSchema, FilePaginationSchema
from projectservice.models import File, FileProperties
from projectservice.database import get_db
from projectservice.utils.pagination import paginatefiles
from projectservice.utils.rbac import has_permissions

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/file',
    tags=['File'],
    dependencies=[Depends(has_permissions("read_files"))]
    )


@router.get('/', response_model=FilePaginationSchema)
def read_files(
        db: Session = Depends(get_db),
        generic: Optional[str] = Query(None, description="Write 'generic' for file listing"),
        search: Optional[str] = Query(None, description="Search term for file_name or desired_file_output"),
        year_start: Optional[int] = Query(None, description="Start year for filtering"),
        year_end: Optional[int] = Query(None, description="End year for filtering"),
        latest_version: bool = Query(True, description="Filter by latest version"),
        limit: int = Query(10, ge=1, description="Number of files to return"),
        offset: int = Query(0, ge=0, description="Starting position to fetch files"),
):
    query = db.query(File)
    logger.info(f"Received query params: search:{search}, year_start: {year_start}, year_end: {year_end}, latest_version: {latest_version}")

    # Aliases for ProjectProperties table
    YearAlias = aliased(FileProperties)

    # Search functionality
    if search:
        query = query.filter(
            (File.desired_file_output.ilike(f"%{search}%")) |
            (File.file_name.ilike(f"%{search}%"))
        )

    # list all the generic files
    # if generic and generic.lower() == "generic":
    #     generic_files = db.query(FileProperties).filter(FileProperties.name == "Generic File Name or File Category").distinct().all()


    # Filter by year range
    if year_start and year_end:
        query = query.join(YearAlias, File.id == YearAlias.file_id)
        query = query.filter((YearAlias.name == "Year") & 
                             (cast(YearAlias.value, Integer).between(year_start, year_end)))
    elif year_start:
        query = query.join(YearAlias, File.id == YearAlias.file_id)
        query = query.filter((YearAlias.name == "Year") & 
                             (cast(YearAlias.value, Integer) >= year_start))
    elif year_end:
        query = query.join(YearAlias, File.id == YearAlias.file_id)
        query = query.filter((YearAlias.name == "Year") & 
                             (cast(YearAlias.value, Integer) <= year_end))
    
    # Filter by latest version
    if latest_version:
        subquery = (
            db.query(File.file_name, File.desired_file_output, func.max(File.version).label("latest_version"),)
            .group_by(File.file_name, File.desired_file_output)
            .subquery()
        )
        query = query.filter((File.file_name == subquery.c.file_name) & 
                             (File.desired_file_output == subquery.c.desired_file_output) & 
                             (File.version == subquery.c.latest_version))
        
    # Sorting (default by file_name ascending)
    query = query.order_by(File.file_name.asc())

    # Count total items for pagination
    total  = query.count()

    # Fetch paginated items
    files = query.offset(offset).limit(limit).all()

    # Convert SQLAlchemy objects to Pydantic models
    files_data = [FileSchema.model_validate(file, from_attributes=True) for file in files if file is not None]

    # Return paginated response
    return paginatefiles(data=files_data, total=total, limit=limit, offset=offset)