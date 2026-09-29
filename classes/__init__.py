"""
University Management System - Domain Entity Classes Package.
All 14 3NF entities are defined with Object-Oriented Principles.
"""

from classes.base import BaseEntity
from classes.department_program import Department, Program
from classes.student_teacher import Student, Teacher
from classes.academic import Course, Semester, Classroom, CourseOffering, Enrollment
from classes.examination import Exam, Result, Attendance, Timetable, UserAccount

__all__ = [
    "BaseEntity",
    "Department",
    "Program",
    "Student",
    "Teacher",
    "Course",
    "Semester",
    "Classroom",
    "CourseOffering",
    "Enrollment",
    "Exam",
    "Result",
    "Attendance",
    "Timetable",
    "UserAccount",
]
