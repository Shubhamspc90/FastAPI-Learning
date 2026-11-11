
from datetime import date
from typing import Literal

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="Student Attendance API",
    description="A practice REST API for managing student attendance records",
    version="1.0.0",
)


AttendanceStatus = Literal["present", "absent"]


class AttendanceCreate(BaseModel):
    student_id: int = Field(gt=0)
    attendance_date: date
    attendance_status: AttendanceStatus


class AttendanceUpdate(BaseModel):
    student_id: int = Field(gt=0)
    attendance_date: date
    attendance_status: AttendanceStatus


class AttendanceResponse(AttendanceCreate):
    id: int


attendance_records: list[dict] = [
    {
        "id": 1,
        "student_id": 101,
        "attendance_date": date(2026, 11, 10),
        "attendance_status": "present",
    },
    {
        "id": 2,
        "student_id": 101,
        "attendance_date": date(2026, 11, 11),
        "attendance_status": "absent",
    },
    {
        "id": 3,
        "student_id": 102,
        "attendance_date": date(2026, 11, 10),
        "attendance_status": "present",
    },
]


@app.post(
    "/attendance",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
)
def mark_attendance(record: AttendanceCreate):
    # Prevent duplicate attendance for the same student on the same date.
    for existing in attendance_records:
        if (
            existing["student_id"] == record.student_id
            and existing["attendance_date"] == record.attendance_date
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Attendance already exists for this student on this date",
            )

    new_id = max(
        (record["id"] for record in attendance_records),
        default=0,
    ) + 1

    new_record = {
        "id": new_id,
        **record.model_dump(),
    }

    attendance_records.append(new_record)
    return new_record


@app.get("/attendance", response_model=list[AttendanceResponse])
def get_all_attendance(
    student_id: int | None = Query(default=None, gt=0),
    attendance_status: AttendanceStatus | None = Query(default=None),
):
    result = attendance_records

    if student_id is not None:
        result = [
            record for record in result
            if record["student_id"] == student_id
        ]

    if attendance_status is not None:
        result = [
            record for record in result
            if record["attendance_status"] == attendance_status
        ]

    return result


@app.get(
    "/attendance/date/{attendance_date}",
    response_model=list[AttendanceResponse],
)
def get_attendance_by_date(attendance_date: date):
    return [
        record for record in attendance_records
        if record["attendance_date"] == attendance_date
    ]


@app.get(
    "/attendance/{attendance_id}",
    response_model=AttendanceResponse,
)
def get_attendance_by_id(attendance_id: int):
    for record in attendance_records:
        if record["id"] == attendance_id:
            return record

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Attendance record not found",
    )


@app.get(
    "/students/{student_id}/attendance",
    response_model=list[AttendanceResponse],
)
def get_student_attendance(student_id: int):
    if student_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID must be greater than zero",
        )

    return [
        record for record in attendance_records
        if record["student_id"] == student_id
    ]


@app.get("/students/{student_id}/attendance/percentage")
def get_attendance_percentage(student_id: int):
    if student_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID must be greater than zero",
        )

    student_records = [
        record for record in attendance_records
        if record["student_id"] == student_id
    ]

    total_days = len(student_records)

    if total_days == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No attendance records found for this student",
        )

    present_days = sum(
        1 for record in student_records
        if record["attendance_status"] == "present"
    )

    percentage = (present_days / total_days) * 100

    return {
        "student_id": student_id,
        "total_days": total_days,
        "present_days": present_days,
        "absent_days": total_days - present_days,
        "attendance_percentage": round(percentage, 2),
    }


@app.put(
    "/attendance/{attendance_id}",
    response_model=AttendanceResponse,
)
def update_attendance(
    attendance_id: int,
    updated_record: AttendanceUpdate,
):
    for index, existing in enumerate(attendance_records):
        if existing["id"] == attendance_id:

            # Prevent duplicate records after updating.
            for other in attendance_records:
                if (
                    other["id"] != attendance_id
                    and other["student_id"] == updated_record.student_id
                    and other["attendance_date"] == updated_record.attendance_date
                ):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Attendance already exists for this student on this date",
                    )

            new_record = {
                "id": attendance_id,
                **updated_record.model_dump(),
            }

            attendance_records[index] = new_record
            return new_record

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Attendance record not found",
    )


@app.delete("/attendance/{attendance_id}")
def delete_attendance(attendance_id: int):
    for index, record in enumerate(attendance_records):
        if record["id"] == attendance_id:
            attendance_records.pop(index)

            return {
                "message": "Attendance record deleted successfully",
                "attendance_id": attendance_id,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Attendance record not found",
    )


# cd 10-practice-projects\05-student-attendance
# uvicorn main:app --reload