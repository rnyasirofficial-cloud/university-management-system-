"""
Student and Teacher domain entities for the University Management System.
"""

from typing import Optional, List, Dict, Any
from datetime import date
from classes.base import BaseEntity


class Student(BaseEntity):
    """
    Represents a student enrolled in a university academic program.
    Entity 3 in 3NF Schema.
    """
    def __init__(
        self,
        registration_no: str,
        student_name: str,
        email: str,
        phone: str,
        admission_date: str | date,
        program_id: int,
        student_id: Optional[int] = None
    ):
        self.student_id = student_id
        self.registration_no = registration_no.strip().upper()
        self.student_name = student_name.strip()
        self.email = email.strip().lower()
        self.phone = phone.strip()
        self.admission_date = str(admission_date)
        self.program_id = program_id

    def validate(self) -> bool:
        """Validate student properties."""
        if not self.registration_no:
            raise ValueError("Registration number cannot be empty.")
        if not self.student_name:
            raise ValueError("Student name cannot be empty.")
        if "@" not in self.email:
            raise ValueError("Invalid student email address.")
        if not self.program_id:
            raise ValueError("Program ID is required.")
        return True

    @staticmethod
    def calculate_gpa(results: List[Dict[str, Any]]) -> float:
        """
        Calculate Cumulative GPA based on grade points and course credit hours.
        CGPA = Sum(Grade_Point * Credit_Hours) / Sum(Credit_Hours)
        """
        if not results:
            return 0.0
        total_quality_points = 0.0
        total_credits = 0.0
        for r in results:
            credits = float(r.get("Credit_Hours", 3.0))
            gp = float(r.get("Grade_Point", 0.0))
            total_quality_points += (gp * credits)
            total_credits += credits

        return round(total_quality_points / total_credits, 2) if total_credits > 0 else 0.0

    @staticmethod
    def calculate_attendance_percentage(attendance_records: List[Dict[str, Any]]) -> float:
        """Calculate overall attendance percentage for a student."""
        if not attendance_records:
            return 0.0
        present_count = sum(
            1 for rec in attendance_records if rec.get("Status") in ("Present", "Late")
        )
        return round((present_count / len(attendance_records)) * 100.0, 1)


class Teacher(BaseEntity):
    """
    Represents a faculty teacher / instructor in the university.
    Entity 4 in 3NF Schema.
    """
    VALID_DESIGNATIONS = [
        "Professor",
        "Associate Professor",
        "Assistant Professor",
        "Senior Lecturer",
        "Lecturer",
        "Visiting Faculty"
    ]

    def __init__(
        self,
        teacher_name: str,
        email: str,
        phone: str,
        designation: str,
        department_id: int,
        teacher_id: Optional[int] = None
    ):
        self.teacher_id = teacher_id
        self.teacher_name = teacher_name.strip()
        self.email = email.strip().lower()
        self.phone = phone.strip()
        self.designation = designation.strip()
        self.department_id = department_id

    def validate(self) -> bool:
        """Validate teacher properties."""
        if not self.teacher_name:
            raise ValueError("Teacher name cannot be empty.")
        if "@" not in self.email:
            raise ValueError("Invalid teacher email address.")
        if not self.department_id:
            raise ValueError("Department ID is required.")
        return True
