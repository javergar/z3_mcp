from typing import cast

from returns.result import Failure, Result, Success
from z3 import (
    BoolRef,
    BoolSort,
    Const,
    ForAll,
    Function,
    Implies,
    Not,
    Solver,
    StringSort,
    unsat,
)

from z3_poc.models.relationships import (
    Entity,
    Relation,
    Relationship,
    RelationshipQuery,
    RelationshipResult,
)


def create_entity(name: str) -> Result[Entity, str]:
    """Create a Z3 constant for an entity.
    
    Args:
        name: The entity name
        
    Returns:
        Result containing an Entity or an error message
    """
    try:
        return Success(Entity(
            name=name,
            z3_const=Const(name, StringSort())
        ))
    except Exception as e:
        return Failure(f"Error creating entity {name}: {e!s}")


def create_entities(relationships: list[Relationship]) -> Result[dict[str, Entity], str]:
    """Create Z3 constants for all entities in the relationships.
    
    Args:
        relationships: List of relationships
        
    Returns:
        Result containing a dictionary of entity names to Entity objects or an error message
    """
    entities_dict = {}
    
    # Extract unique entity names from relationships
    entity_names = set()
    for rel in relationships:
        entity_names.add(rel.person1)
        entity_names.add(rel.person2)
    
    # Create Z3 constants for each entity
    for name in entity_names:
        result = create_entity(name)
        match result:
            case Success(entity):
                entities_dict[name] = entity
            case Failure(_):
                return result
    
    return Success(entities_dict)


def create_relation(name: str) -> Result[Relation, str]:
    """Create a Z3 function for a relation.
    
    Args:
        name: The relation name
        
    Returns:
        Result containing a Relation or an error message
    """
    try:
        return Success(Relation(
            name=name,
            z3_func=Function(name, StringSort(), StringSort(), BoolSort())
        ))
    except Exception as e:
        return Failure(f"Error creating relation {name}: {e!s}")


def create_relations(relationships: list[Relationship]) -> Result[dict[str, Relation], str]:
    """Create Z3 functions for all relations in the relationships.
    
    Args:
        relationships: List of relationships
        
    Returns:
        Result containing a dictionary of relation names to Relation objects or an error message
    """
    relations_dict = {}
    
    # Extract unique relation names from relationships
    relation_names = set(rel.relation for rel in relationships)
    
    # Create Z3 functions for each relation
    for name in relation_names:
        result = create_relation(name)
        match result:
            case Success(relation):
                relations_dict[name] = relation
            case Failure(_):
                return result
    
    return Success(relations_dict)


def add_relationship_assertions(
    solver: Solver,
    relationships: list[Relationship],
    entities: dict[str, Entity],
    relations: dict[str, Relation]
) -> Result[None, str]:
    """Add relationship assertions to the solver.
    
    Args:
        solver: The Z3 solver
        relationships: List of relationships
        entities: Dictionary of entity names to Entity objects
        relations: Dictionary of relation names to Relation objects
        
    Returns:
        Result containing None or an error message
    """
    try:
        for rel in relationships:
            relation = relations[rel.relation]
            entity1 = entities[rel.person1]
            entity2 = entities[rel.person2]
            
            # Use pattern matching to check for None values
            match (relation.z3_func, entity1.z3_const, entity2.z3_const):
                case (None, _, _):
                    return Failure(f"Relation {rel.relation} has no Z3 function")
                case (_, None, _):
                    return Failure(f"Entity {rel.person1} has no Z3 constant")
                case (_, _, None):
                    return Failure(f"Entity {rel.person2} has no Z3 constant")
                case (z3_func, e1_const, e2_const):
                    # All values are not None, proceed with adding constraints
                    if rel.value:
                        solver.add(z3_func(e1_const, e2_const))
                    else:
                        solver.add(Not(z3_func(e1_const, e2_const)))
        
        # Add symmetry axioms for sibling relation if it exists
        if "sibling" in relations:
            x = Const("x", StringSort())
            y = Const("y", StringSort())
            sibling_relation = relations["sibling"]
            
            # Use pattern matching to check for None value
            match sibling_relation.z3_func:
                case None:
                    return Failure("Sibling relation has no Z3 function")
                case z3_func:
                    solver.add(ForAll([x, y], Implies(z3_func(x, y), z3_func(y, x))))
        
        return Success(None)
    except Exception as e:
        return Failure(f"Error adding relationship assertions: {e!s}")


def parse_query(
    query: str,
    entities: dict[str, Entity],
    relations: dict[str, Relation]
) -> Result[BoolRef, str]:
    """Parse a relationship query into a Z3 expression.
    
    Args:
        query: The query string
        entities: Dictionary of entity names to Entity objects
        relations: Dictionary of relation names to Relation objects
        
    Returns:
        Result containing a Z3 expression or an error message
    """
    try:
        # Simple parsing for queries like "relation(entity1, entity2)"
        parts = query.split("(")
        if len(parts) != 2 or ")" not in parts[1]:
            return Failure(f"Invalid query format: {query}")
        
        relation_name = parts[0].strip()
        entities_part = parts[1].split(")")[0].strip()
        entity_names = [e.strip() for e in entities_part.split(",")]
        
        if len(entity_names) != 2:
            return Failure(f"Query must involve exactly two entities: {query}")
        
        if relation_name not in relations:
            return Failure(f"Unknown relation: {relation_name}")
        
        for entity_name in entity_names:
            if entity_name not in entities:
                return Failure(f"Unknown entity: {entity_name}")
        
        relation = relations[relation_name]
        entity1 = entities[entity_names[0]]
        entity2 = entities[entity_names[1]]
        
        # Use pattern matching to check for None values
        match (relation.z3_func, entity1.z3_const, entity2.z3_const):
            case (None, _, _):
                return Failure(f"Relation {relation_name} has no Z3 function")
            case (_, None, _):
                return Failure(f"Entity {entity_names[0]} has no Z3 constant")
            case (_, _, None):
                return Failure(f"Entity {entity_names[1]} has no Z3 constant")
            case (z3_func, e1_const, e2_const):
                # Cast the result to BoolRef to satisfy the return type
                result = z3_func(e1_const, e2_const)
                return Success(cast(BoolRef, result))
    except Exception as e:
        return Failure(f"Error parsing query '{query}': {e!s}")


def evaluate_query(
    solver: Solver,
    query_expr: BoolRef
) -> Result[tuple[bool, str, bool], str]:
    """Evaluate a query expression using the solver.
    
    Args:
        solver: The Z3 solver
        query_expr: The Z3 query expression
        
    Returns:
        Result containing a tuple of (result, explanation, is_satisfiable) or an error message
    """
    try:
        # Check if the model implies the query
        solver.push()
        solver.add(Not(query_expr))
        neg_result = solver.check()
        solver.pop()
        
        # If the negation is unsatisfiable, the query is implied
        if neg_result == unsat:
            return Success((True, "The relationship is confirmed by the given facts.", True))
        
        # Check if the model implies the negation of the query
        solver.push()
        solver.add(query_expr)
        pos_result = solver.check()
        solver.pop()
        
        # If the query is unsatisfiable, its negation is implied
        if pos_result == unsat:
            return Success((False, "The relationship is contradicted by the given facts.", True))
        
        # If both are satisfiable, the query is neither implied nor contradicted
        return Success((False, "The relationship is possible but not confirmed by the given facts.", True))
    except Exception as e:
        return Failure(f"Error evaluating query: {e!s}")


def analyze_relationships(query: RelationshipQuery) -> Result[RelationshipResult, str]:
    """Analyze relationships and evaluate a query.
    
    Args:
        query: The relationship query
        
    Returns:
        Result containing a RelationshipResult or an error message
    """
    try:
        solver = Solver()
        
        # Create entities and relations
        entities_result = create_entities(query.relationships)
        match entities_result:
            case Failure(error):
                return Failure(error)
            case Success(entities):
                relations_result = create_relations(query.relationships)
                match relations_result:
                    case Failure(error):
                        return Failure(error)
                    case Success(relations):
                        # Add relationship assertions
                        assertions_result = add_relationship_assertions(solver, query.relationships, entities, relations)
                        match assertions_result:
                            case Failure(error):
                                return Failure(error)
                            case Success(_):
                                # Parse the query
                                query_expr_result = parse_query(query.query, entities, relations)
                                match query_expr_result:
                                    case Failure(error):
                                        return Failure(error)
                                    case Success(query_expr):
                                        # Check if the model is satisfiable
                                        if solver.check() == unsat:
                                            return Success(RelationshipResult(
                                                result=False,
                                                explanation="The relationships are contradictory.",
                                                is_satisfiable=False
                                            ))
                                        
                                        # Evaluate the query
                                        eval_result = evaluate_query(solver, query_expr)
                                        match eval_result:
                                            case Failure(error):
                                                return Failure(error)
                                            case Success((result, explanation, is_satisfiable)):
                                                return Success(RelationshipResult(
                                                    result=result,
                                                    explanation=explanation,
                                                    is_satisfiable=is_satisfiable
                                                ))
    except Exception as e:
        return Failure(f"Error analyzing relationships: {e!s}")
    
    # This should never be reached, but adding for type safety
    return Failure("Unexpected error in analyze_relationships")
