from typing import List
from projectservice.schemas.project import ProjectPaginationSchema, ProjectSchema
from projectservice.schemas.file import FilePaginationSchema, FileSchema


def paginateprojects(data: List[ProjectSchema], total: int, limit: int, offset: int) -> ProjectPaginationSchema: 
    return ProjectPaginationSchema(
        total= total,
        limit= limit,
        offset= offset,
        data= data
    )


def paginatefiles(data: List[FileSchema], total: int, limit: int, offset: int) -> FilePaginationSchema: 
    return FilePaginationSchema(
        total= total,
        limit= limit,
        offset= offset,
        data= data
    )