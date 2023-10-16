"""
This file stores enumeration classes needed through the optimization frameworks.
"""

# -------------------------------------------------------------------------------------------------------------------- #
# Standard Library
from enum import Enum

# Third Party


# Private Party


# -------------------------------------------------------------------------------------------------------------------- #


class OptimizationType(str, Enum):
    """Enum for specifying the type of optimization."""

    MINIMIZE = "minimize"
    MAXIMIZE = "maximize"


class InequalityType(str, Enum):
    """Enum for specifying the type of inequality constraint."""

    LESS_THAN = "<"
    LESS_THAN_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_THAN_EQUAL = ">="
    EQUAL = "="
