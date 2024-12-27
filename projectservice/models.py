from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, UUID, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from datetime import datetime, date
from projectservice.database import Base


class BusinessEntities(Base):
    __tablename__ = 'businessentities'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    key = Column(Integer, autoincrement=True, unique=True)
    value = Column(String(255), nullable=False)
    description = Column(String)


class Rules(Base):
    __tablename__ = 'rules'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    key = Column(Integer, autoincrement=True, unique=True)
    value = Column(String(255), nullable=False)
    description = Column(String)


class Scripts(Base):
    __tablename__ = 'scripts'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    key = Column(Integer, autoincrement=True, unique=True)
    value = Column(String(255), nullable=False)
    description = Column(String)


class Process(Base):
    __tablename__ = 'process'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    key = Column(Integer, autoincrement=True, unique=True)
    value = Column(String(255), nullable=False)
    description = Column(String)


class DataTypes(Base):
    __tablename__ = 'datatypes'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    key = Column(Integer, autoincrement=True, unique=True)
    value = Column(String(255), nullable=False)
    description = Column(String)


class ModellingTools(Base):
    __tablename__ = 'modellingtools'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    key = Column(Integer, autoincrement=True, unique=True)
    value = Column(String(255), nullable=False)
    description = Column(String)


class Softwares(Base):
    __tablename__ = 'softwares'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    key = Column(Integer, autoincrement=True, unique=True)
    value = Column(String(255), nullable=False)
    description = Column(String)


class Methodologies(Base):
    __tablename__ = 'methodologies'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    key = Column(Integer, autoincrement=True, unique=True)
    value = Column(String(255), nullable=False)
    description = Column(String)


class ProjectStatus(Base):
    __tablename__ = 'projectstatus'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    key = Column(Integer, autoincrement=True, unique=True)
    value = Column(String(255), nullable=False)
    description = Column(String)


class DataTransferStatus(Base):
    __tablename__ = 'datatransferstatus'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    key = Column(Integer, autoincrement=True, unique=True)
    value = Column(String(255), nullable=False)
    description = Column(String)


class SourceLocationType(Base):
    __tablename__ = 'sourcelocationtype'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    key = Column(Integer, autoincrement=True, unique=True)
    value = Column(String(255), nullable=False)
    description = Column(String)


class DestinationLocationType(Base):
    __tablename__ = 'destinationlocationtype'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    key = Column(Integer, autoincrement=True, unique=True)
    value = Column(String(255), nullable=False)
    description = Column(String)


class RulesProcessStatus(Base):
    __tablename__ = 'rulesprocessstatus'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    key = Column(Integer, autoincrement=True, unique=True)
    value = Column(String(255), nullable=False)
    description = Column(String)


class Users(Base):
    __tablename__ = 'users'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    short_id = Column(String(255), nullable=False)
    created_date = Column(Date, nullable=False, default=date.today)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_date = Column(Date, nullable=True)
    last_login_date_time = Column(DateTime, nullable=True)
    business_entity = Column(PG_UUID(as_uuid=True), ForeignKey("businessentities.id"), nullable=False)
    # Relationship to BusinessEntities
    business_entity_relationship = relationship("BusinessEntities")
    roles = relationship("UserRole", back_populates="user")


class Projects(Base):
    __tablename__ = "projects"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    project_id = Column(String(255), nullable=False)
    project_name = Column(String(255), nullable=False)
    project_code = Column(String(255), nullable=False)
    erf_number = Column(String(255), nullable=False)
    project_manager = Column(String(255))
    land_owner = Column(String(255))
    crediting_start_year = Column(Integer)
    crediting_end_year = Column(Integer)
    state = Column(String(255))
    country = Column(String(255))
    projection_system_utm = Column(Integer)
    created_date = Column(Date, nullable=False)
    updated_date = Column(Date, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_date = Column(Date)
    business_entity = Column(PG_UUID(as_uuid=True), ForeignKey("businessentities.id"), nullable=False)
    methodology = Column(PG_UUID(as_uuid=True), ForeignKey("methodologies.id"), nullable=False)
    status = Column(PG_UUID(as_uuid=True), ForeignKey("projectstatus.id"), nullable=False)
    modeling_tools = Column(PG_UUID(as_uuid=True), ForeignKey("modellingtools.id"), nullable=False)
    data_transfer_status = Column(PG_UUID(as_uuid=True), ForeignKey("datatransferstatus.id"), nullable=False)
    rule_process_status = Column(PG_UUID(as_uuid=True), ForeignKey("rulesprocessstatus.id"), nullable=False)
    created_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    modified_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    deleted_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    # Relationship to Foreign Key Tables
    business_entity_relationship = relationship("BusinessEntities", foreign_keys=[business_entity])
    methodology_relationship = relationship("Methodologies", foreign_keys=[methodology])
    status_relationship = relationship("ProjectStatus", foreign_keys=[status])
    modeling_tools_relationship = relationship("ModellingTools", foreign_keys=[modeling_tools])
    data_transfer_status_relationship = relationship("DataTransferStatus", foreign_keys=[data_transfer_status])
    rule_process_status_relationship = relationship("RulesProcessStatus", foreign_keys=[rule_process_status])
    created_by_relationship = relationship("Users", foreign_keys=[created_by])
    modified_by_relationship = relationship("Users", foreign_keys=[modified_by])
    deleted_by_relationship = relationship("Users", foreign_keys=[deleted_by])

    
class Files(Base):
    __tablename__ = "files"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    project_id = Column(PG_UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    category = Column(String(255))
    custodian = Column(String(255))
    generic_file_name = Column(String(255))
    file_name = Column(String(255))
    desired_file_output = Column(String(255), nullable=False)
    source_location = Column(String, nullable=False)
    site = Column(String)
    version = Column(Float)
    comment = Column(String)
    process = Column(PG_UUID(as_uuid=True), ForeignKey("process.id"))
    process_script = Column(PG_UUID(as_uuid=True), ForeignKey("scripts.id"))
    data_type = Column(PG_UUID(as_uuid=True), ForeignKey("datatypes.id"))
    year = Column(Integer)
    software = Column(PG_UUID(as_uuid=True), ForeignKey("softwares.id"))
    source_location_type = Column(PG_UUID(as_uuid=True), ForeignKey("sourcelocationtype.id"))
    destination_location = Column(String)
    destination_location_type = Column(PG_UUID(as_uuid=True), ForeignKey("destinationlocationtype.id"))
    state = Column(String(255))
    country = Column(String(255))
    projection_system_utm = Column(Integer)
    data_transfer_status = Column(PG_UUID(as_uuid=True), ForeignKey("datatransferstatus.id"), nullable=False)
    created_date = Column(Date, nullable=False)
    updated_date = Column(Date, nullable=False)
    created_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    modified_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_date = Column(Date)
    deleted_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    # Relationship to Foreign Key Tables
    project_id_relationship = relationship("Projects", foreign_keys=[project_id])
    process_relationship = relationship("Process", foreign_keys=[process])
    process_script_relationship = relationship("Scripts", foreign_keys=[process_script])
    data_type_relationship = relationship("DataTypes", foreign_keys=[data_type])
    software_relationship = relationship("Softwares", foreign_keys=[software])
    source_location_type_relationship = relationship("SourceLocationType", foreign_keys=[source_location_type])
    destination_location_type_relationship = relationship("DestinationLocationType", foreign_keys=[destination_location_type])
    data_transfer_status_relationship = relationship("DataTransferStatus", foreign_keys=[data_transfer_status])
    created_by_relationship = relationship("Users", foreign_keys=[created_by])
    modified_by_relationship = relationship("Users", foreign_keys=[modified_by])
    deleted_by_relationship = relationship("Users", foreign_keys=[deleted_by])


class Roles(Base):
    __tablename__ = 'roles'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    # Relationship
    users = relationship("UserRole", back_populates="role")
    permissions = relationship("RolePermission", back_populates="role")


class Permissions(Base):
    __tablename__ = 'permissions'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    # Relationship
    roles = relationship("RolePermission", back_populates="permission")


class RolePermission(Base):
    __tablename__ = 'role_permission'

    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)

    # Composite Primary Key
    __table_args__ = (PrimaryKeyConstraint('role_id', 'permission_id'),)

    # Relationships
    role = relationship("Roles", back_populates="permissions")
    permission = relationship("Permissions", back_populates="roles")


class UserRole(Base):
    __tablename__ = 'user_roles'

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)

    # Composite Primary Key
    __table_args__ = (PrimaryKeyConstraint('user_id', 'role_id'),)

    # Relationships
    user = relationship("Users", back_populates="roles")
    role = relationship("Roles", back_populates="users")


class Project(Base):
    __tablename__ = "project"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, nullable=False)
    project_name = Column(String, nullable=False)
    state = Column(String)
    country = Column(String)
    data_transfer_status = Column(PG_UUID(as_uuid=True), ForeignKey("datatransferstatus.id"), nullable=False)
    rule_process_status = Column(PG_UUID(as_uuid=True), ForeignKey("rulesprocessstatus.id"), nullable=False)
    created_date = Column(Date, nullable=False)
    updated_date = Column(Date, nullable=False)
    is_deleted = Column(Boolean, default=False)
    deleted_date = Column(Date)
    created_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    modified_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    deleted_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    # Relationship to Foreign Key Tables
    data_transfer_status_relationship = relationship("DataTransferStatus", foreign_keys=[data_transfer_status])
    rule_process_status_relationship = relationship("RulesProcessStatus", foreign_keys=[rule_process_status])
    created_by_relationship = relationship("Users", foreign_keys=[created_by])
    modified_by_relationship = relationship("Users", foreign_keys=[modified_by])
    deleted_by_relationship = relationship("Users", foreign_keys=[deleted_by])
    project_properties = relationship("ProjectProperties", back_populates="project")


class ProjectProperties(Base):
    __tablename__ = "projectproperties"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(PG_UUID(as_uuid=True), ForeignKey("project.id"), nullable=False)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)
    business_entity = Column(PG_UUID(as_uuid=True), ForeignKey("businessentities.id"), nullable=False)
    # Relationship to Foreign Key Tables
    business_entity_relationship = relationship("BusinessEntities", foreign_keys=[business_entity])
    project = relationship("Project", back_populates="project_properties")


class File(Base):
    __tablename__ = "file"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    project_id = Column(PG_UUID(as_uuid=True), ForeignKey("project.id"), nullable=False)
    file_name = Column(String)
    desired_file_output = Column(String(255), nullable=False)
    source_location = Column(String, nullable=False)
    version = Column(Float)
    comment = Column(String)
    data_type = Column(String)
    source_location_type = Column(String)
    destination_location = Column(String)
    destination_location_type = Column(String)
    state = Column(String)
    country = Column(String)
    data_transfer_status = Column(PG_UUID(as_uuid=True), ForeignKey("datatransferstatus.id"), nullable=False)
    created_date = Column(Date, nullable=False)
    updated_date = Column(Date, nullable=False)
    is_deleted = Column(Boolean, default=False)
    deleted_date = Column(Date)
    created_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    modified_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    deleted_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    # Relationship to Foreign Key Tables
    project_id_relationship = relationship("Project", foreign_keys=[project_id])
    data_transfer_status_relationship = relationship("DataTransferStatus", foreign_keys=[data_transfer_status])
    created_by_relationship = relationship("Users", foreign_keys=[created_by])
    modified_by_relationship = relationship("Users", foreign_keys=[modified_by])
    deleted_by_relationship = relationship("Users", foreign_keys=[deleted_by])
    file_properties = relationship("FileProperties", back_populates="file")


class FileProperties(Base):
    __tablename__ = "fileproperties"

    id = Column(String, primary_key=True, index=True)
    file_id = Column(PG_UUID(as_uuid=True), ForeignKey("file.id"), nullable=False)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)
    business_entity = Column(PG_UUID(as_uuid=True), ForeignKey("businessentities.id"), nullable=False)
    # Relationship to Foreign Key Tables
    business_entity_relationship = relationship("BusinessEntities", foreign_keys=[business_entity])
    file = relationship("File", back_populates="file_properties")


