"""
Course, Semester, Classroom, CourseOffering, and Enrollment domain entities.
Entities 5, 6, 7, 8, 9 in 3NF Schema.
"""

from typing import Optional
from datetime import date
from classes.base import BaseEntity


class Course(BaseEntity):
    """
    Represents an academic course offered in curriculum.
    Entity 5 in 3NF Schema.
    """
    def __init__(
        self,
        course_code: str,
        course_name: str,
        credit_hours: int,
        department_id: int,
        course_description: str = "",
        course_id: Optional[int] = None
    ):
        self.course_id = course_id
        self.course_code = course_code.strip().upper()
        self.course_name = course_name.strip()
        self.credit_hours = int(credit_hours)
        self.department_id = int(department_id)
        self.course_description = course_description.strip()

    def validate(self) -> bool:
        if not self.course_code:
            raise ValueError("Course code cannot be empty.")
        if not (1 <= self.credit_hours <= 6):
            raise ValueError("Credit hours must be between 1 and 6.")
        return True


class Semester(BaseEntity):
    """
    Represents an academic semester session (e.g., Fall 2026).
    Entity 6 in 3NF Schema.
    """
    def __init__(
        self,
        semester_name: str,
        year: int,
        start_date: str | date,
        end_date: str | date,
        semester_id: Optional[int] = None
    ):
        self.semester_id = semester_id
        self.semester_name = semester_name.strip()
        self.year = int(year)
        self.start_date = str(start_date)
        self.end_date = str(end_date)

    @property
    def full_name(self) -> str:
        return f"{self.semester_name} {self.year}"


class Classroom(BaseEntity):
    """
    Represents a physical classroom or laboratory hall.
    Entity 7 in 3NF Schema.
    """
    def __init__(
        self,
        building_name: str,
        room_number: str,
        capacity: int,
        room_id: Optional[int] = None
    ):
        self.room_id = room_id
        self.building_name = building_name.strip()
        self.room_number = room_number.strip()
        self.capacity = int(capacity)

    @property
    def display_name(self) -> str:
        return f"{self.building_name} - {self.room_number} (Cap: {self.capacity})"


class CourseOffering(BaseEntity):
    """
    Represents an active course section offered during a semester.
    Entity 8 in 3NF Schema.
    """
    def __init__(
        self,
        course_id: int,
        semester_id: int,
        teacher_id: int,
        room_id: int,
        section: str = "A",
        offering_id: Optional[int] = None
    ):
        self.offering_id = offering_id
        self.course_id = int(course_id)
        self.semester_id = int(semester_id)
        self.teacher_id = int(teacher_id)
        self.room_id = int(room_id)
        self.section = section.strip().upper()


class Enrollment(BaseEntity):
    """
    Resolves the M:N relationship between Student and CourseOffering.
    Entity 9 in 3NF Schema.
    """
    STATUS_OPTIONS = ["Enrolled", "Dropped", "Completed", "Withdrawn"]

    def __init__(
        self,
        student_id: int,
        offering_id: int,
        enrollment_date: str | date,
        status: str = "Enrolled",
        enrollment_id: Optional[int] = None
    ):
        self.enrollment_id = enrollment_id
        self.student_id = int(student_id)
        self.offering_id = int(offering_id)
        self.enrollment_date = str(enrollment_date)
        self.status = status.strip().capitalize()

    def drop(self) -> None:
        """Mark student course status as Dropped."""
        self.status = "Dropped"

    def complete(self) -> None:
        """Mark student course status as Completed."""
        self.status = "Completed"
