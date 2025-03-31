# Z3 Theorem Prover with Functional Programming

A Python implementation of abstactions over the Z3 Theorem Prover capabilities using functional programming principles, exposed through a Model Context Protocol (MCP) server.

## Overview

This project demonstrates how to use the Z3 Theorem Prover with a functional programming approach to solve complex constraint satisfaction problems and analyze relationships between entities. It leverages the `returns` library for functional programming abstractions and exposes its capabilities through an MCP server.

## Features

- **Constraint Satisfaction Problems**: Solve complex problems with variables and constraints
- **Relationship Analysis**: Analyze and infer relationships between entities
- **Functional Programming**: Uses pure functions, immutable data structures, and monadic error handling
- **MCP Server**: Exposes Z3 capabilities through a standardized interface

## Project Structure

```
z3_poc/
├── core/                  # Core implementation
│   ├── solver.py          # Constraint satisfaction problem solving
│   └── relationships.py   # Relationship analysis
├── models/                # Data models
│   ├── constraints.py     # Models for constraint problems
│   └── relationships.py   # Models for relationship analysis
├── server/                # MCP server
│   └── main.py            # Server implementation
└── examples/              # Example usage
    └── main.py            # Demonstration of capabilities
```

## Technical Stack

- **Z3 Solver**: Microsoft's theorem prover for constraint solving
- **Returns**: Functional programming library for monadic operations and error handling
- **Pydantic**: Data validation and serialization
- **FastMCP**: Implementation of the Model Context Protocol

## Installation

This project uses `uv` for dependency management.

```bash
# Clone the repository
git clone https://github.com/yourusername/z3_poc.git
cd z3_poc

# Install dependencies
uv pip install -e .

# Install development dependencies (optional)
uv pip install -e ".[dev]"
```

## Usage

### Running Examples

The project includes several examples that demonstrate the capabilities of the Z3 solver:

```bash
# Run the examples
python -m z3_poc.examples.main
```

Examples include:
- N-Queens Problem
- Family Relationship Inference
- Temporal Reasoning with Causal Relationships
- Cryptarithmetic Puzzle (SEND + MORE = MONEY)

### Running the MCP Server

Start the MCP server to expose Z3 capabilities through the Model Context Protocol:

```bash
# Run the server
python -m z3_poc.server.main
```

### Setting up the MCP Server with Claude/Cline

To use the Z3 solver MCP server with Claude through the Cline extension in VSCode, you need to configure the `settings.json` file:


1. **Configuration**: Add the following to the `mcpServers` object in the settings file:

```json
"z3-solver": {
  "command": "uv",
  "args": [
    "--directory",
    "/path/to/your/z3_poc",
    "run",
    "z3_poc/server/main.py"
  ],
  "disabled": false,
  "autoApprove": [
    "simple_constraint_solver", 
    "simple_relationship_analyzer", 
    "solve_constraint_problem", 
    "analyze_relationships"
  ]
}
```

2. **Configuration Options**:
   - `command`: The command to run (using `uv` for Python environment management)
   - `args`: Command arguments, including the path to your project and the server script
   - `disabled`: Set to `false` to enable the server
   - `autoApprove`: List of tools that can be used without explicit approval

4. **Restart**: After updating the settings, restart VSCode or the Claude Desktop app for the changes to take effect.

Once configured, Claude will have access to the Z3 solver capabilities through the MCP server.

## MCP Tools

The server provides the following tools:

### `solve_constraint_problem`

Solves a constraint satisfaction problem with a full Problem model.

```python
# Example input
{
  "problem": {
    "variables": [
      {"name": "x", "type": "integer"},
      {"name": "y", "type": "integer"}
    ],
    "constraints": [
      {"expression": "x + y == 10"},
      {"expression": "x >= 0"},
      {"expression": "y >= 0"}
    ],
    "description": "Find non-negative values for x and y that sum to 10"
  }
}
```

### `analyze_relationships`

Analyzes relationships between entities with a full RelationshipQuery model.

```python
# Example input
{
  "query": {
    "relationships": [
      {"person1": "Alice", "person2": "Bob", "relation": "sibling"},
      {"person1": "Bob", "person2": "Charlie", "relation": "sibling"}
    ],
    "query": "sibling(Alice, Charlie)"
  }
}
```

### `simple_constraint_solver`

A simpler interface for solving constraint problems without requiring the full Problem model.

```python
# Example input
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

### `simple_relationship_analyzer`

A simpler interface for analyzing relationships without requiring the full RelationshipQuery model.

```python
# Example input
{
  "relationships": [
    {"person1": "Bob", "person2": "Hanna", "relation": "sibling"},
    {"person1": "Bob", "person2": "Claudia", "relation": "sibling"}
  ],
  "query": "sibling(Hanna, Claudia)"
}
```

## Functional Programming Approach

This project demonstrates several functional programming principles:

1. **Immutable Data Structures**: Using Pydantic models for immutable data representation
2. **Result Type**: Using `returns.result.Result` for error handling without exceptions
3. **Maybe Type**: Using `returns.maybe.Maybe` for handling nullable values
4. **Do Notation**: Using generator expressions with `Result.do()` for sequential operations
5. **Pattern Matching**: Using Python's match-case for handling different result types

Example of do notation in `analyze_relationships`:

```python
expr = (
    RelationshipResult(...)
    for entities in create_entities(query.relationships)
    for relations in create_relations(query.relationships)
    for _ in add_relationship_assertions(solver, query.relationships, entities, relations)
    for query_expr in parse_query(query.query, entities, relations)
    for (result, explanation, is_satisfiable) in evaluate_query(solver, query_expr)
)

return Result.do(expr)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
