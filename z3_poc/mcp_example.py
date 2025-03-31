#!/usr/bin/env python3
"""
Example of how an LLM would use an MCP server for Z3 constraint solving.

This script demonstrates a simple MCP server that provides Z3 constraint solving
capabilities and shows how an LLM would interact with it.
"""
import json
from typing import Any


# Simulate an MCP server that provides Z3 constraint solving
class Z3MCP:
    """Simulated MCP server for Z3 constraint solving."""
    
    def handle_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """Handle an MCP request."""
        if request["method"] == "list_tools":
            return self._list_tools()
        elif request["method"] == "call_tool":
            return self._call_tool(request["params"])
        else:
            return {"error": {"code": -32601, "message": f"Method {request['method']} not found"}}
    
    def _list_tools(self) -> dict[str, Any]:
        """List available tools."""
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
    
    def _call_tool(self, params: dict[str, Any]) -> dict[str, Any]:
        """Call a tool."""
        if params["name"] == "solve_constraint":
            return self._solve_constraint(params["arguments"])
        else:
            return {"error": {"code": -32601, "message": f"Tool {params['name']} not found"}}
    
    def _solve_constraint(self, args: dict[str, Any]) -> dict[str, Any]:
        """Simulate solving a Z3 constraint problem."""
        # In a real implementation, this would use Z3 to solve the constraints
        # For this example, we'll just return a simulated result
        
        # Check if this is the SEND + MORE = MONEY puzzle
        is_money_puzzle = False
        for constraint in args["constraints"]:
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
        for constraint in args["constraints"]:
            if "queen" in constraint.lower() or "diagonal" in constraint.lower():
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
    """Run a simple demonstration of the MCP server."""
    print("Z3 MCP Server Example")
    print("=" * 50)
    
    server = Z3MCP()
    
    # Simulate an LLM making requests to the MCP server
    print("\nLLM: Listing available tools...")
    tools_request = {"method": "list_tools", "params": {}}
    tools_response = server.handle_request(tools_request)
    print(f"MCP Server response: {json.dumps(tools_response, indent=2)}")
    
    print("\nLLM: Solving the SEND + MORE = MONEY puzzle...")
    solve_request = {
        "method": "call_tool",
        "params": {
            "name": "solve_constraint",
            "arguments": {
                "variables": [
                    {"name": "S", "type": "integer"},
                    {"name": "E", "type": "integer"},
                    {"name": "N", "type": "integer"},
                    {"name": "D", "type": "integer"},
                    {"name": "M", "type": "integer"},
                    {"name": "O", "type": "integer"},
                    {"name": "R", "type": "integer"},
                    {"name": "Y", "type": "integer"}
                ],
                "constraints": [
                    "1000*S + 100*E + 10*N + D + 1000*M + 100*O + 10*R + E == 10000*M + 1000*O + 100*N + 10*E + Y",
                    "Distinct(S, E, N, D, M, O, R, Y)",
                    "S > 0",
                    "M > 0"
                ]
            }
        }
    }
    solve_response = server.handle_request(solve_request)
    print(f"MCP Server response: {json.dumps(solve_response, indent=2)}")
    
    print("\nLLM: Now I can use this solution in my response to the user:")
    print("-" * 50)
    solution = json.loads(solve_response["content"][0]["text"])
    print("I've solved the SEND + MORE = MONEY puzzle!")
    print(f"S={solution['values']['S']}, E={solution['values']['E']}, N={solution['values']['N']}, D={solution['values']['D']}")
    print(f"M={solution['values']['M']}, O={solution['values']['O']}, R={solution['values']['R']}, Y={solution['values']['Y']}")
    send = 1000*solution['values']['S'] + 100*solution['values']['E'] + 10*solution['values']['N'] + solution['values']['D']
    more = 1000*solution['values']['M'] + 100*solution['values']['O'] + 10*solution['values']['R'] + solution['values']['E']
    money = 10000*solution['values']['M'] + 1000*solution['values']['O'] + 100*solution['values']['N'] + 10*solution['values']['E'] + solution['values']['Y']
    print(f"{send} + {more} = {money}")


if __name__ == "__main__":
    main()
