from pydantic import BaseModel, Field, UUID4
from datetime import date, datetime
from uuid import UUID
from typing import Optional, List


class FilePropertiesSchema(BaseModel):
    id: UUID
    file_id: UUID4
    name: str
    value: str
    business_entity: UUID4

    class Config: 
        orm_mode = True


# File schema for responses
class FileSchema(BaseModel):
    id: UUID
    file_name: Optional[str] = None
    desired_file_output: str
    source_location: str
    version: Optional[float] = None
    comment: Optional[str] = None
    data_type: Optional[str] = None
    source_location_type: Optional[str] = None
    destination_location: Optional[str] = None
    destination_location_type: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    created_date: date
    updated_date: date
    is_deleted: bool
    deleted_date: Optional[date] = None
    # Back reference to Parent
    project_id: Optional[UUID4]
    data_transfer_status: UUID4
    created_by: UUID4
    modified_by: UUID4
    deleted_by: Optional[UUID4] = None
    file_properties: List[FilePropertiesSchema]

    class Config: 
        orm_mode = True


# File Pagination Schema
class FilePaginationSchema(BaseModel):
    total: int
    limit: int
    offset: int
    data: List[FileSchema]

    class Config:
        orm_mode = True