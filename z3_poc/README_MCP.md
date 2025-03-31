# Using MCP with Z3 for Constraint Solving

This directory contains examples of how an LLM (Large Language Model) can use the Model Context Protocol (MCP) to solve complex constraint problems using the Z3 theorem prover.

## Overview

The Model Context Protocol (MCP) allows LLMs to access external tools and resources, extending their capabilities beyond their training data. In these examples, we demonstrate how an LLM can use MCP to solve constraint satisfaction problems that would be difficult for the LLM to solve on its own.

## Examples

### 1. MCP Server Example (`mcp_example.py`)

This example demonstrates a simple MCP server that provides Z3 constraint solving capabilities. The server exposes a `solve_constraint` tool that can solve various constraint problems, including:

- Cryptarithmetic puzzles (e.g., SEND + MORE = MONEY)
- N-Queens problem
- General constraint satisfaction problems

The example shows how an LLM would make requests to the MCP server and use the results in its responses to users.

To run this example:

```bash
python z3_poc/mcp_example.py
```

### 2. MCP Client Example (`mcp_client_example.py`)

This example demonstrates how an LLM would use an MCP client to interact with a Z3 MCP server. It shows the LLM's thought process when solving constraint problems, including:

1. Discovering available tools through the MCP protocol
2. Formulating constraint problems in a way the Z3 solver can understand
3. Interpreting the results and presenting them to the user

To run this example:

```bash
python z3_poc/mcp_client_example.py
```

## How It Works

1. The LLM receives a request from a user to solve a constraint problem
2. The LLM uses the MCP protocol to discover available tools from the Z3 MCP server
3. The LLM formulates the problem as a set of variables and constraints
4. The LLM sends a request to the Z3 MCP server to solve the problem
5. The Z3 MCP server solves the problem and returns the solution
6. The LLM interprets the solution and presents it to the user

## Benefits of Using MCP with Z3

1. **Formal Verification**: Z3 provides formal verification of solutions, ensuring correctness
2. **Complex Constraint Solving**: Z3 can efficiently solve problems that would be difficult for an LLM to solve on its own
3. **Precise Mathematical Reasoning**: Z3 excels at precise mathematical reasoning and constraint satisfaction
4. **Complementary Capabilities**: The LLM handles natural language understanding and problem formulation, while Z3 handles the formal reasoning and constraint solving

## Example Problems

### Cryptarithmetic Puzzle (SEND + MORE = MONEY)

This classic puzzle requires finding digit values for letters where:
```
  S E N D
+ M O R E
---------
M O N E Y
```

Each letter represents a unique digit, and the arithmetic must be correct.

### 8-Queens Problem

The 8-Queens problem requires placing 8 queens on an 8×8 chessboard so that no queen can attack another. This means no two queens can share the same row, column, or diagonal.

## Implementation Details

The examples use simulated MCP servers and clients for demonstration purposes. In a real implementation:

1. The MCP server would use the actual Z3 solver to solve the constraints
2. The MCP client would use the MCP protocol to communicate with the server
3. The LLM would use the MCP client to access the server's capabilities

The examples show the basic structure and flow of how an LLM would use MCP to solve constraint problems.
