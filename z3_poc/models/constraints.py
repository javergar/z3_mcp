from enum import Enum
from typing import Union

from pydantic import BaseModel
from z3 import ArithRef, BoolRef, BoolSort, ExprRef, IntSort, RealSort, StringSort


class VariableType(str, Enum):
    """Enum for supported variable types in Z3."""
    INTEGER = "integer"
    REAL = "real"
    BOOLEAN = "boolean"
    STRING = "string"


class Variable(BaseModel):
    """Model representing a variable in a Z3 problem."""
    name: str
    type: VariableType


class Constraint(BaseModel):
    """Model representing a constraint in a Z3 problem."""
    expression: str  # Z3 expression as string
    description: str = ""


class Problem(BaseModel):
    """Model representing a complete Z3 constraint satisfaction problem."""
    variables: list[Variable]
    constraints: list[Constraint]
    description: str = ""


# Define Z3 value types
Z3Value = bool | int | float | str
Z3Ref = Union[BoolRef, ArithRef, ExprRef]  # Add ExprRef for more flexibility
Z3Sort = Union[BoolSort, IntSort, RealSort, StringSort]


class Solution(BaseModel):
    """Model representing a solution to a Z3 problem."""
    values: dict[str, Z3Value]
    is_satisfiable: bool
    status: str
