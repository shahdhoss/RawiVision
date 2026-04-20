from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.attendance import AttendanceCreate, AttendanceResponse
from ..models.attendance import Attendance
from uuid import UUID
from sqlalchemy import select

class AttendanceRepository:
    def __init__(self, db:AsyncSession):
        self.db = db
    
    async def create_attendance_record(self, attendance:AttendanceCreate):
        try:
            new_attendance_record = Attendance(employee_id=attendance.employee_id)
            self.db.add(new_attendance_record)
            await self.db.flush()
            return new_attendance_record
        except Exception as error:
            raise error
    
    async def read_all_attendance_records(self):
        result = await self.db.execute(select(Attendance))
        attendance_records = result.scalars().all()
        return attendance_records
    
    async def read_attendance_record_by_employee_id(self, employee_id: UUID):
        result = await self.db.execute(select(Attendance).where(Attendance.employee_id == employee_id))
        attendance_records = result.scalars().all()
        return attendance_records