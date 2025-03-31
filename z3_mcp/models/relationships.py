from dataclasses import dataclass

from pydantic import BaseModel
from z3 import FuncDeclRef


class Relationship(BaseModel):
    """Model representing a relationship between two entities."""
    person1: str
    person2: str
    relation: str
    value: bool = True


class RelationshipQuery(BaseModel):
    """Model representing a query about relationships."""
    relationships: list[Relationship]
    query: str


class RelationshipResult(BaseModel):
    """Model representing the result of a relationship query."""
    result: bool
    explanation: str
    is_satisfiable: bool


@dataclass
class Entity:
    """Dataclass representing an entity in a relationship."""
    name: str
    z3_const: object | None = None  # Z3 constant


@dataclass
class Relation:
    """Dataclass representing a relation between entities."""
    name: str
    z3_func: FuncDeclRef | None = None  # Z3 function declaration
