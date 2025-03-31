#!/usr/bin/env python3
import json

from fastmcp import FastMCP
from mcp.types import TextContent
from returns.result import Failure, Success

from z3_mcp.core.relationships import analyze_relationships
from z3_mcp.core.solver import solve_problem
from z3_mcp.models.constraints import (
    Constraint,
    Problem,
    Variable,
    VariableType,
)
from z3_mcp.models.relationships import (
    Relationship,
    RelationshipQuery,
)

# Create the FastMCP application
app = FastMCP(
    name="z3-server",
    version="0.1.0",
    description="Z3 Theorem Prover MCP Server"
)


@app.tool("solve_constraint_problem")
async def solve_constraint_problem(problem: Problem) -> list[TextContent]:
    """Solve a constraint satisfaction problem using Z3.
    
    This tool takes a constraint satisfaction problem defined with variables and constraints,
    and returns a solution if one exists.
    
    Args:
        problem: The problem definition with variables and constraints
        
    Returns:
        A list of TextContent containing the solution or an error message
    """
    result = solve_problem(problem)
    
    match result:
        case Success(solution):
            return [TextContent(
                type="text",
                text=json.dumps({
                    "values": solution.values,
                    "is_satisfiable": solution.is_satisfiable,
                    "status": solution.status
                })
            )]
        case Failure(error):
            return [TextContent(
                type="text",
                text=f"Error solving problem: {error}"
            )]
        case _:
            # This should never happen, but adding for type safety
            return [TextContent(
                type="text",
                text="Unexpected error in solve_constraint_problem"
            )]


@app.tool("analyze_relationships")
async def analyze_relationships_tool(query: RelationshipQuery) -> list[TextContent]:
    """Analyze relationships between entities using Z3.
    
    This tool takes a set of relationships between entities and a query about 
    those relationships, and determines whether the query is implied by 
    the given relationships.
    
    Args:
        query: The relationship query with relationships and a query string
        
    Returns:
        A list of TextContent containing the analysis result or an error message
    """
    result = analyze_relationships(query)
    
    match result:
        case Success(rel_result):
            return [TextContent(
                type="text",
                text=json.dumps({
                    "result": rel_result.result,
                    "explanation": rel_result.explanation,
                    "is_satisfiable": rel_result.is_satisfiable
                })
            )]
        case Failure(error):
            return [TextContent(
                type="text",
                text=f"Error analyzing relationships: {error}"
            )]
        case _:
            # This should never happen, but adding for type safety
            return [TextContent(
                type="text",
                text="Unexpected error in analyze_relationships_tool"
            )]


@app.tool("simple_constraint_solver")
async def simple_constraint_solver(
    variables: list[dict[str, str]],
    constraints: list[str],
    description: str = ""
) -> list[TextContent]:
    """A simpler interface for solving constraint problems.
    
    This tool provides a more straightforward interface for simple constraint problems,
    without requiring the full Problem model structure.
    
    Args:
        variables: List of variable definitions, each with 'name' and 'type'
        constraints: List of constraint expressions as strings
        description: Optional description of the problem
        
    Returns:
        A list of TextContent containing the solution or an error message
    """
    try:
        # Convert to Problem model
        problem_variables = []
        for var in variables:
            if 'name' not in var or 'type' not in var:
                return [TextContent(
                    type="text",
                    text="Each variable must have 'name' and 'type' fields"
                )]
            
            try:
                var_type = VariableType(var['type'])
            except ValueError:
                return [TextContent(
                    type="text",
                    text=f"Invalid variable type: {var['type']}. Must be one of: {', '.join([t.value for t in VariableType])}"
                )]
            
            problem_variables.append(Variable(name=var['name'], type=var_type))
        
        problem_constraints = [Constraint(expression=expr) for expr in constraints]
        
        problem = Problem(
            variables=problem_variables,
            constraints=problem_constraints,
            description=description
        )
        
        # Solve the problem
        result = solve_problem(problem)
        
        match result:
            case Success(solution):
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "values": solution.values,
                        "is_satisfiable": solution.is_satisfiable,
                        "status": solution.status
                    })
                )]
            case Failure(error):
                return [TextContent(
                    type="text",
                    text=f"Error solving problem: {error}"
                )]
            case _:
                # This should never happen, but adding for type safety
                return [TextContent(
                    type="text",
                    text="Unexpected error in simple_constraint_solver"
                )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error in simple_constraint_solver: {e!s}"
        )]


@app.tool("simple_relationship_analyzer")
async def simple_relationship_analyzer(
    relationships: list[dict[str, str | bool]],
    query: str
) -> list[TextContent]:
    """A simpler interface for analyzing relationships.
    
    This tool provides a more straightforward interface for relationship analysis,
    without requiring the full RelationshipQuery model structure.
    
    Args:
        relationships: List of relationship definitions, each with 'person1', 
        'person2', 'relation', and optional 'value'
        query: A query string in the format "relation(entity1, entity2)"
        
    Returns:
        A list of TextContent containing the analysis result or an error message
    """
    try:
        # Convert to RelationshipQuery model
        query_relationships = []
        for rel in relationships:
            if 'person1' not in rel or 'person2' not in rel or 'relation' not in rel:
                return [TextContent(
                    type="text",
                    text="Each relationship must have 'person1', 'person2', and 'relation' fields"
                )]
            
            value = rel.get('value', True)
            if not isinstance(value, bool):
                return [TextContent(
                    type="text",
                    text=f"Relationship value must be a boolean, got: {value}"
                )]
            
            # Ensure person1, person2, and relation are strings
            person1 = str(rel['person1'])
            person2 = str(rel['person2'])
            relation = str(rel['relation'])
            
            query_relationships.append(Relationship(
                person1=person1,
                person2=person2,
                relation=relation,
                value=value
            ))
        
        relationship_query = RelationshipQuery(
            relationships=query_relationships,
            query=query
        )
        
        # Analyze the relationships
        result = analyze_relationships(relationship_query)
        
        match result:
            case Success(rel_result):
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "result": rel_result.result,
                        "explanation": rel_result.explanation,
                        "is_satisfiable": rel_result.is_satisfiable
                    })
                )]
            case Failure(error):
                return [TextContent(
                    type="text",
                    text=f"Error analyzing relationships: {error}"
                )]
            case _:
                # This should never happen, but adding for type safety
                return [TextContent(
                    type="text",
                    text="Unexpected error in simple_relationship_analyzer"
                )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error in simple_relationship_analyzer: {e!s}"
        )]


if __name__ == "__main__":
    app.run()
