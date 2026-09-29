"""
Exam, Result, Attendance, Timetable, and UserAccount domain entities.
Entities 10, 11, 12, 13, 14 in 3NF Schema.
"""

import hashlib
from typing import Optional, Tuple
from datetime import date, time
from classes.base import BaseEntity


class Exam(BaseEntity):
    """
    Represents an examination or assessment conducted for a course offering.
    Entity 10 in 3NF Schema.
    """
    VALID_TYPES = ["Midterm", "Final", "Quiz", "Assignment", "Project"]

    def __init__(
        self,
        offering_id: int,
        exam_type: str,
        exam_date: str | date,
        total_marks: float,
        exam_id: Optional[int] = None
    ):
        self.exam_id = exam_id
        self.offering_id = int(offering_id)
        self.exam_type = exam_type.strip()
        self.exam_date = str(exam_date)
        self.total_marks = float(total_marks)


class Result(BaseEntity):
    """
    Connects student with exam, storing marks, letter grade, and grade points.
    Entity 11 in 3NF Schema.
    """
    def __init__(
        self,
        student_id: int,
        exam_id: int,
        obtained_marks: float,
        grade: Optional[str] = None,
        grade_point: Optional[float] = None,
        result_id: Optional[int] = None,
        total_marks: float = 100.0
    ):
        self.result_id = result_id
        self.student_id = int(student_id)
        self.exam_id = int(exam_id)
        self.obtained_marks = float(obtained_marks)

        if grade is None or grade_point is None:
            g, gp = self.compute_grade(self.obtained_marks, total_marks)
            self.grade = g
            self.grade_point = gp
        else:
            self.grade = grade.strip()
            self.grade_point = float(grade_point)

    @staticmethod
    def compute_grade(obtained: float, total: float) -> Tuple[str, float]:
        """
        Computes standard university letter grade and 4.0 scale grade points.
        """
        if total <= 0:
            return ("F", 0.0)
        percentage = (obtained / total) * 100.0

        if percentage >= 85:
            return ("A+", 4.00)
        elif percentage >= 80:
            return ("A", 4.00)
        elif percentage >= 75:
            return ("B+", 3.33)
        elif percentage >= 70:
            return ("B", 3.00)
        elif percentage >= 65:
            return ("C+", 2.33)
        elif percentage >= 60:
            return ("C", 2.00)
        elif percentage >= 50:
            return ("D", 1.00)
        else:
            return ("F", 0.00)


class Attendance(BaseEntity):
    """
    Represents student class attendance per session.
    Entity 12 in 3NF Schema.
    """
    VALID_STATUSES = ["Present", "Absent", "Late", "Excused"]

    def __init__(
        self,
        student_id: int,
        offering_id: int,
        attendance_date: str | date,
        status: str = "Present",
        attendance_id: Optional[int] = None
    ):
        self.attendance_id = attendance_id
        self.student_id = int(student_id)
        self.offering_id = int(offering_id)
        self.attendance_date = str(attendance_date)
        self.status = status.strip().capitalize()


class Timetable(BaseEntity):
    """
    Represents weekly timetable schedule for lectures in assigned classrooms.
    Entity 13 in 3NF Schema.
    """
    DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    def __init__(
        self,
        offering_id: int,
        room_id: int,
        day: str,
        start_time: str,
        end_time: str,
        timetable_id: Optional[int] = None
    ):
        self.timetable_id = timetable_id
        self.offering_id = int(offering_id)
        self.room_id = int(room_id)
        self.day = day.strip().capitalize()
        self.start_time = str(start_time)
        self.end_time = str(end_time)

    def conflicts_with(self, other: "Timetable") -> bool:
        """Check if this timetable slot overlaps with another in the same room on the same day."""
        if self.day != other.day or self.room_id != other.room_id:
            return False
        # If slots overlap
        return not (self.end_time <= other.start_time or self.start_time >= other.end_time)


class UserAccount(BaseEntity):
    """
    Represents user authentication credentials and role authorization.
    Entity 14 in 3NF Schema.
    """
    ROLES = ["Administrator", "Teacher", "Student"]

    def __init__(
        self,
        username: str,
        password: str,
        role: str,
        student_id: Optional[int] = None,
        teacher_id: Optional[int] = None,
        user_id: Optional[int] = None,
        is_already_hashed: bool = False
    ):
        self.user_id = user_id
        self.username = username.strip()
        self.password = password if is_already_hashed else self.hash_password(password)
        self.role = role.strip()
        self.student_id = student_id
        self.teacher_id = teacher_id

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def verify_password(self, plain_password: str) -> bool:
        """Verify plain password against stored hash."""
        return self.password == self.hash_password(plain_password)
