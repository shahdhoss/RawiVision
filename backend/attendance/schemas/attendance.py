from pydantic import BaseModel
from uuid import uuid4
from uuid import UUID
from datetime import date, datetime

class AttendanceBase(BaseModel):
    employee_id: UUID

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceResponse(AttendanceBase):
    id: UUID
    day: date | None
    date_created: datetime | None