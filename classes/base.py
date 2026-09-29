"""
Base entity class for University Management System domain models.
Provides common methods for serialization, validation, and string representation.
"""

from typing import Any, Dict
from datetime import datetime, date


class BaseEntity:
    """Base class for all domain model entities in the University Management System."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert the model instance into a dictionary representation."""
        result = {}
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            if isinstance(value, (datetime, date)):
                result[key] = value.isoformat()
            elif hasattr(value, "to_dict"):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result

    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith("_"))
        return f"{self.__class__.__name__}({attrs})"
