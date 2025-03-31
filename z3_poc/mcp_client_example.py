#!/usr/bin/env python3
"""
Example of how an LLM would use an MCP client to interact with a Z3 MCP server.

This script demonstrates how an LLM would use the MCP protocol to solve
constraint problems using a Z3 MCP server.
"""
import json
from typing import Any


# Simulate an LLM using an MCP client to interact with a Z3 MCP server
class LLMWithMCP:
    """Simulated LLM that uses MCP to solve constraint problems."""
    
    def __init__(self):
        """Initialize the LLM with MCP client."""
        self.server_name = "z3-solver"
        print(f"LLM: I have access to the {self.server_name} MCP server.")
    
    def solve_cryptarithmetic_puzzle(self):
        """Solve the SEND + MORE = MONEY puzzle using MCP."""
        print("\nUser: Can you solve the SEND + MORE = MONEY puzzle?")
        print("\nLLM thinking: I'll use the Z3 MCP server to solve this cryptarithmetic puzzle.")
        
        # First, I'll check what tools are available
        print("\nLLM: I'll use the MCP protocol to list available tools:")
        tools = self._simulate_mcp_list_tools()
        print(f"Available tools: {json.dumps(tools, indent=2)}")
        
        # Now I'll use the solve_constraint tool
        print("\nLLM: Now I'll use the solve_constraint tool to solve the puzzle:")
        result = self._simulate_mcp_solve_constraint([
            {"name": "S", "type": "integer"},
            {"name": "E", "type": "integer"},
            {"name": "N", "type": "integer"},
            {"name": "D", "type": "integer"},
            {"name": "M", "type": "integer"},
            {"name": "O", "type": "integer"},
            {"name": "R", "type": "integer"},
            {"name": "Y", "type": "integer"}
        ], [
            "1000*S + 100*E + 10*N + D + 1000*M + 100*O + 10*R + E == 10000*M + 1000*O + 100*N + 10*E + Y",
            "Distinct(S, E, N, D, M, O, R, Y)",
            "S > 0",
            "M > 0"
        ])
        
        # Parse the result
        solution = json.loads(result["content"][0]["text"])
        
        # Formulate a response to the user
        print("\nLLM response to user:")
        print("-" * 50)
        print("I've solved the SEND + MORE = MONEY puzzle using formal verification with Z3!")
        print("Here's the solution:")
        print(f"  S={solution['values']['S']}, E={solution['values']['E']}, N={solution['values']['N']}, D={solution['values']['D']}")
        print(f"  M={solution['values']['M']}, O={solution['values']['O']}, R={solution['values']['R']}, Y={solution['values']['Y']}")
        
        # Calculate the values
        send = 1000*solution['values']['S'] + 100*solution['values']['E'] + 10*solution['values']['N'] + solution['values']['D']
        more = 1000*solution['values']['M'] + 100*solution['values']['O'] + 10*solution['values']['R'] + solution['values']['E']
        money = 10000*solution['values']['M'] + 1000*solution['values']['O'] + 100*solution['values']['N'] + 10*solution['values']['E'] + solution['values']['Y']
        
        print(f"\nLet's verify: {send} + {more} = {money}")
        print(f"  {solution['values']['S']}{solution['values']['E']}{solution['values']['N']}{solution['values']['D']} + {solution['values']['M']}{solution['values']['O']}{solution['values']['R']}{solution['values']['E']} = {solution['values']['M']}{solution['values']['O']}{solution['values']['N']}{solution['values']['E']}{solution['values']['Y']}")
        print(f"  {send} + {more} = {money} ✓")
    
    def solve_n_queens(self):
        """Solve the 8-Queens problem using MCP."""
        print("\nUser: Can you solve the 8-Queens problem?")
        print("\nLLM thinking: I'll use the Z3 MCP server to solve the 8-Queens problem.")
        
        # Create variables for each queen's position
        variables = []
        constraints = []
        
        for i in range(8):
            variables.append({"name": f"q{i}", "type": "integer"})
        
        # Add constraints
        # Each queen must be in a valid row (0 to 7)
        for i in range(8):
            constraints.append(f"q{i} >= 0")
            constraints.append(f"q{i} < 8")
        
        # No two queens can be in the same row
        for i in range(8):
            for j in range(i+1, 8):
                constraints.append(f"q{i} != q{j}")
        
        # No two queens can be in the same diagonal
        for i in range(8):
            for j in range(i+1, 8):
                constraints.append(f"Or(q{i} - q{j} != {j-i}, q{i} - q{j} != {-(j-i)})")
        
        # Use the MCP server to solve the problem
        print("\nLLM: I'll use the MCP protocol to solve the 8-Queens problem:")
        result = self._simulate_mcp_solve_constraint(variables, constraints)
        
        # Parse the result
        solution = json.loads(result["content"][0]["text"])
        
        # Formulate a response to the user
        print("\nLLM response to user:")
        print("-" * 50)
        print("I've solved the 8-Queens problem using formal verification with Z3!")
        print("Here's a solution where no queen can attack another:")
        
        # Create a chessboard representation
        board = [['.' for _ in range(8)] for _ in range(8)]
        
        # Place queens on the board
        for col, row_val in solution["values"].items():
            col_idx = int(col[1:])
            row_idx = row_val
            board[row_idx][col_idx] = 'Q'
        
        # Print the chessboard
        print("\nChessboard representation (Q = queen, . = empty):")
        print("  " + " ".join([str(i) for i in range(8)]))
        for i, row in enumerate(board):
            print(f"{i} {' '.join(row)}")
    
    def _simulate_mcp_list_tools(self) -> dict[str, Any]:
        """Simulate using MCP to list available tools."""
        # In a real implementation, this would use the MCP protocol to communicate with the server
        # For this example, we'll just return a simulated response
        return {
            "tools": [
                {
                    "name": "solve_constraint",
                    "description": "Solve a Z3 constraint problem",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "variables": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "type": {"type": "string", "enum": ["integer", "real", "boolean"]}
                                    },
                                    "required": ["name", "type"]
                                }
                            },
                            "constraints": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            }
                        },
                        "required": ["variables", "constraints"]
                    }
                }
            ]
        }
    
    def _simulate_mcp_solve_constraint(self, variables: list[dict[str, str]], constraints: list[str]) -> dict[str, Any]:
        """Simulate using MCP to solve a constraint problem."""
        # In a real implementation, this would use the MCP protocol to communicate with the server
        # For this example, we'll just return a simulated response
        
        # Check if this is the SEND + MORE = MONEY puzzle
        is_money_puzzle = False
        for constraint in constraints:
            if "10000*M" in constraint and "1000*S" in constraint:
                is_money_puzzle = True
                break
        
        if is_money_puzzle:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "is_satisfiable": True,
                            "values": {
                                "S": 9, "E": 5, "N": 6, "D": 7,
                                "M": 1, "O": 0, "R": 8, "Y": 2
                            },
                            "explanation": "SEND (9567) + MORE (1085) = MONEY (10652)"
                        }, indent=2)
                    }
                ]
            }
        
        # For N-Queens problem
        queens_pattern = False
        for v in variables:
            if v["name"].startswith("q"):
                queens_pattern = True
                break
        
        if queens_pattern:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "is_satisfiable": True,
                            "values": {
                                "q0": 0, "q1": 4, "q2": 7, "q3": 5, 
                                "q4": 2, "q5": 6, "q6": 1, "q7": 3
                            },
                            "explanation": "Valid 8-queens placement where no queen can attack another"
                        }, indent=2)
                    }
                ]
            }
        
        # Default response for other constraints
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "is_satisfiable": True,
                        "values": {
                            "x": 3, "y": 7, "z": 2
                        },
                        "explanation": "Found a solution that satisfies all constraints"
                    }, indent=2)
                }
            ]
        }


def main():
    """Run a demonstration of an LLM using MCP to solve constraint problems."""
    print("LLM Using MCP for Z3 Constraint Solving")
    print("=" * 50)
    
    llm = LLMWithMCP()
    
    # Demonstrate solving the SEND + MORE = MONEY puzzle
    llm.solve_cryptarithmetic_puzzle()
    
    print("\n" + "=" * 50)
    
    # Demonstrate solving the 8-Queens problem
    llm.solve_n_queens()


if __name__ == "__main__":
    main()
