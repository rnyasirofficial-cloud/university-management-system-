"""
Department and Program domain entities for the University Management System.
"""

from typing import Optional
from classes.base import BaseEntity


class Department(BaseEntity):
    """
    Represents an academic department within the university.
    Entity 1 in 3NF Schema.
    """
    def __init__(
        self,
        department_name: str,
        department_email: str,
        department_id: Optional[int] = None
    ):
        self.department_id = department_id
        self.department_name = department_name.strip()
        self.department_email = department_email.strip().lower()

    def validate(self) -> bool:
        """Validate department properties."""
        if not self.department_name:
            raise ValueError("Department name cannot be empty.")
        if "@" not in self.department_email:
            raise ValueError("Invalid department email format.")
        return True


class Program(BaseEntity):
    """
    Represents an academic degree program offered by a department.
    Entity 2 in 3NF Schema.
    """
    def __init__(
        self,
        program_name: str,
        degree_level: str,
        department_id: int,
        program_id: Optional[int] = None
    ):
        self.program_id = program_id
        self.program_name = program_name.strip()
        self.degree_level = degree_level.strip()
        self.department_id = department_id

    def validate(self) -> bool:
        """Validate program properties."""
        if not self.program_name:
            raise ValueError("Program name cannot be empty.")
        if not self.degree_level:
            raise ValueError("Degree level cannot be empty.")
        if not self.department_id:
            raise ValueError("Department ID is required.")
        return True
