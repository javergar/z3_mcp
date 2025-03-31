# Z3 MCP Server

A Model Context Protocol (MCP) server for Z3 Theorem Prover using functional programming principles.

## Features

- **Constraint Satisfaction Problems**: Solve problems with variables and constraints
- **Relationship Analysis**: Analyze relationships between entities
- **Functional Programming**: Uses pure functions and immutable data structures
- **MCP Server**: Exposes Z3 capabilities through a standardized interface

## Architecture

The project follows a functional programming approach using:

- **Pydantic**: For data validation and serialization
- **Returns**: For functional programming abstractions (Result, Maybe, etc.)
- **FastMCP**: For implementing the MCP server
- **Z3 Solver**: For constraint solving and theorem proving

## Setup

This project uses `uv` for dependency management.

```bash
# Install dependencies
uv sync
```

## Running the Examples

Run the examples using the main module:

```bash
# Run with Python
python -m z3_poc.main

# Or with uv
uv run python -m z3_poc.main
```

## Running the MCP Server

Start the MCP server:

```bash
# Run with Python
python -m z3_poc.server.main

# Or with uv
uv run python -m z3_poc.server.main
```

## MCP Tools

The server provides the following tools:

### solve_constraint_problem

Solves a constraint satisfaction problem with a full Problem model.

### analyze_relationships

Analyzes relationships between entities with a full RelationshipQuery model.

### simple_constraint_solver

A simpler interface for solving constraint problems without requiring the full Problem model.

### simple_relationship_analyzer

A simpler interface for analyzing relationships without requiring the full RelationshipQuery model.

## Example Usage

### Constraint Solving

```python
# Example input for simple_constraint_solver
{
  "variables": [
    {"name": "x", "type": "integer"},
    {"name": "y", "type": "integer"}
  ],
  "constraints": [
    "x + y == 10",
    "x <= 5",
    "y <= 5"
  ],
  "description": "Find values for x and y"
}
```

### Relationship Analysis

```python
# Example input for simple_relationship_analyzer
{
  "relationships": [
    {"person1": "Bob", "person2": "Hanna", "relation": "sibling"},
    {"person1": "Bob", "person2": "Claudia", "relation": "sibling"}
  ],
  "query": "sibling(Hanna, Claudia)"
}
```
