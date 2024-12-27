from pydantic import BaseModel, Field, UUID4
from datetime import date, datetime
from uuid import UUID
from typing import Optional, List


# Files schema for responses
class FilesSchema(BaseModel):
    id: UUID
    category: Optional[str] = None
    custodian: Optional[str] = None
    generic_file_name: Optional[str] = None
    file_name: Optional[str] = None
    desired_file_output: str
    source_location: str
    site: Optional[str] = None
    version: Optional[float] = None
    comment: Optional[str] = None
    year: Optional[int] = Field(None, ge=1900)
    destination_location: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    projection_system_utm: Optional[int]
    created_date: date
    updated_date: date
    is_deleted: bool
    deleted_date: Optional[date] = None
    # Back reference to Parent
    process: Optional[UUID4]
    process_script: Optional[UUID4] = None
    data_type: Optional[UUID4]
    software: Optional[UUID4] = None
    source_location_type: Optional[UUID4] = None
    destination_location_type: Optional[UUID4]
    data_transfer_status: UUID4
    created_by: UUID4
    modified_by: UUID4
    deleted_by: Optional[UUID4] = None

    class Config: 
        orm_mode = True


# File Pagination Schema
class FilePaginationSchema(BaseModel):
    total: int
    limit: int
    offset: int
    files: List[FilesSchema]

    class Config:
        orm_mode = True