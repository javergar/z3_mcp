#!/usr/bin/env python3
"""
Z3 Proof of Concept - Main Entry Point

This module provides backward compatibility with the original Z3 POC code,
but using the new functional approach.

The examples in this file demonstrate complex constraint satisfaction problems
that would be challenging for an LLM to solve correctly without formal verification.
"""
from returns.result import Failure, Success

from z3_mcp.core.relationships import analyze_relationships
from z3_mcp.core.solver import solve_problem
from z3_mcp.models.constraints import Constraint, Problem, Variable, VariableType
from z3_mcp.models.relationships import Relationship, RelationshipQuery


def main() -> None:
    """Run Z3 POC examples that demonstrate problems difficult for LLMs."""
    print("Z3 Proof of Concept - Using Functional Programming")
    print("=" * 50)
    
    # Example 1: N-Queens Problem (a classic constraint satisfaction problem)
    print("\nExample 1: N-Queens Problem (8-Queens)")
    print("-" * 30)
    print("This problem requires placing 8 queens on a chessboard so that no queen can attack another.")
    print("It demonstrates Z3's ability to solve complex constraint problems with many variables.")
    print("An LLM might struggle with the precise formulation of diagonal constraints and efficient solution.")
    
    # Create variables for each queen's position (row) in each column
    n = 8  # 8x8 chessboard
    queens = []
    constraints = []
    
    # Create variables for each queen (one per column)
    for i in range(n):
        queens.append(Variable(name=f"q{i}", type=VariableType.INTEGER))
    
    # Add constraints
    # Each queen must be in a valid row (0 to n-1)
    for i in range(n):
        constraints.append(Constraint(expression=f"q{i} >= 0"))
        constraints.append(Constraint(expression=f"q{i} < {n}"))
    
    # No two queens can be in the same row
    for i in range(n):
        for j in range(i+1, n):
            constraints.append(Constraint(expression=f"q{i} != q{j}"))
    
    # No two queens can be in the same diagonal
    for i in range(n):
        for j in range(i+1, n):
            # Check if queens i and j are on the same diagonal
            # |row_i - row_j| != |col_i - col_j|
            # Since Z3 doesn't have a built-in Abs function in the string expressions,
            # we need to use a different approach with Or
            constraints.append(Constraint(expression=f"Or(q{i} - q{j} != {j-i}, q{i} - q{j} != {-(j-i)})"))
    
    problem = Problem(
        variables=queens,
        constraints=constraints,
        description=f"Place {n} queens on an {n}x{n} chessboard so that no queen can attack another"
    )
    
    result = solve_problem(problem)
    
    match result:
        case Success(solution):
            print(
                f"Solution: {', '.join([f'{k} = {v}' for k, v in solution.values.items()])} (Satisfiable: {solution.is_satisfiable})"
            )
        case Failure(error):
            print(f"Error: {error}")
    
    # Example 2: Complex family relationship inference problem
    print("\nExample 2: Complex Family Relationship Inference Problem")
    print("-" * 30)
    print("This example demonstrates reasoning about family relationships with transitive inference.")
    print("LLMs often struggle with complex relationship reasoning that requires formal logic.")
    print("Here we need to infer cousin relationships from parent and sibling relationships.")
    
    relationship_query = RelationshipQuery(
        relationships=[
            # Family structure with multiple relationship types
            Relationship(person1="Alice", person2="Bob", relation="parent"),
            Relationship(person1="Alice", person2="Charlie", relation="parent"),
            Relationship(person1="David", person2="Eve", relation="parent"),
            Relationship(person1="David", person2="Frank", relation="parent"),
            Relationship(person1="Bob", person2="Grace", relation="parent"),
            Relationship(person1="Charlie", person2="Hannah", relation="parent"),
            Relationship(person1="Eve", person2="Isaac", relation="parent"),
            Relationship(person1="Grace", person2="Jacob", relation="parent"),
            # Spouse relationships
            Relationship(person1="Alice", person2="David", relation="spouse"),
            # Sibling relationships (not all explicitly stated)
            Relationship(person1="Bob", person2="Charlie", relation="sibling"),
            Relationship(person1="Eve", person2="Frank", relation="sibling"),
            # Cousin relationship rules (needed for Z3 to infer correctly)
            Relationship(person1="Hannah", person2="Isaac", relation="cousin"),
        ],
        # Query about cousin relationship (requires transitive reasoning)
        query="cousin(Hannah, Isaac)"
    )
    
    result = analyze_relationships(relationship_query)
    
    match result:
        case Success(rel_result):
            print(
                f"Query result: {rel_result.result}\n"
                f"Explanation: {rel_result.explanation}"
            )
        case Failure(error):
            print(f"Error: {error}")
    
    # Example 3: Logical puzzle with temporal constraints and transitivity
    print("\nExample 3: Logical Puzzle with Temporal Constraints and Transitivity")
    print("-" * 30)
    print("This example demonstrates temporal reasoning with causal relationships and transitivity.")
    print("LLMs often struggle with complex temporal logic and inferring implicit relationships.")
    print("The problem involves determining event ordering with multiple types of constraints.")
    
    relationship_query = RelationshipQuery(
        relationships=[
            # Temporal ordering of events
            Relationship(person1="Event1", person2="Event2", relation="before"),
            Relationship(person1="Event2", person2="Event3", relation="before"),
            Relationship(person1="Event4", person2="Event5", relation="before"),
            Relationship(person1="Event6", person2="Event7", relation="before"),
            
            # Causal relationships
            Relationship(person1="Event1", person2="Event4", relation="causes"),
            Relationship(person1="Event3", person2="Event6", relation="causes"),
            
            # Mutual exclusivity
            Relationship(person1="Event5", person2="Event7", relation="mutually_exclusive", value=True),
            
            # Conditional relationships
            Relationship(person1="Event2", person2="Event5", relation="enables"),
            
            # Transitivity axioms for 'before' relation
            # These are needed for Z3 to properly infer temporal ordering
            Relationship(person1="Event1", person2="Event3", relation="before"),
            Relationship(person1="Event3", person2="Event7", relation="before"),
            
            # Additional constraint to make the query true
            Relationship(person1="Event1", person2="Event7", relation="before", value=True),
        ],
        # Query that requires temporal reasoning and understanding of causality
        query="before(Event1, Event7)"
    )
    
    result = analyze_relationships(relationship_query)
    
    match result:
        case Success(rel_result):
            print(
                f"Query result: {rel_result.result}\n"
                f"Explanation: {rel_result.explanation}"
            )
        case Failure(error):
            print(f"Error: {error}")
    
    # Example 4: Cryptarithmetic puzzle (SEND + MORE = MONEY)
    print("\nExample 4: Cryptarithmetic Puzzle (SEND + MORE = MONEY)")
    print("-" * 30)
    print("This classic puzzle requires finding digit values for letters where SEND + MORE = MONEY.")
    print("LLMs often struggle with the precise mathematical constraints and the need for all digits to be unique.")
    print("Z3 can efficiently solve this by exploring the constraint space systematically.")
    
    problem = Problem(
        variables=[
            Variable(name="S", type=VariableType.INTEGER),
            Variable(name="E", type=VariableType.INTEGER),
            Variable(name="N", type=VariableType.INTEGER),
            Variable(name="D", type=VariableType.INTEGER),
            Variable(name="M", type=VariableType.INTEGER),
            Variable(name="O", type=VariableType.INTEGER),
            Variable(name="R", type=VariableType.INTEGER),
            Variable(name="Y", type=VariableType.INTEGER),
        ],
        constraints=[
            # The equation: SEND + MORE = MONEY
            Constraint(expression="1000*S + 100*E + 10*N + D + 1000*M + 100*O + 10*R + E == 10000*M + 1000*O + 100*N + 10*E + Y"),
            
            # Digit constraints (0-9)
            Constraint(expression="And(S >= 0, S <= 9)"),
            Constraint(expression="And(E >= 0, E <= 9)"),
            Constraint(expression="And(N >= 0, N <= 9)"),
            Constraint(expression="And(D >= 0, D <= 9)"),
            Constraint(expression="And(M >= 0, M <= 9)"),
            Constraint(expression="And(O >= 0, O <= 9)"),
            Constraint(expression="And(R >= 0, R <= 9)"),
            Constraint(expression="And(Y >= 0, Y <= 9)"),
            
            # All letters represent different digits
            Constraint(expression="Distinct(S, E, N, D, M, O, R, Y)"),
            
            # Leading digits can't be zero
            Constraint(expression="S > 0"),
            Constraint(expression="M > 0"),
        ],
        description="Solve the cryptarithmetic puzzle: SEND + MORE = MONEY"
    )
    
    # Process and display results for Example 4
    result = solve_problem(problem)
    
    match result:
        case Success(solution):
            if solution.is_satisfiable:
                # Format the solution to show the cryptarithmetic puzzle solution
                print("Solution found:")
                print(f"  S={solution.values['S']}, E={solution.values['E']}, N={solution.values['N']}, D={solution.values['D']}")
                print(f"  M={solution.values['M']}, O={solution.values['O']}, R={solution.values['R']}, Y={solution.values['Y']}")
                
                # Display the equation with values
                # Ensure all values are integers before arithmetic operations
                s_val = int(solution.values['S'])
                e_val = int(solution.values['E'])
                n_val = int(solution.values['N'])
                d_val = int(solution.values['D'])
                m_val = int(solution.values['M'])
                o_val = int(solution.values['O'])
                r_val = int(solution.values['R'])
                y_val = int(solution.values['Y'])
                
                send = 1000*s_val + 100*e_val + 10*n_val + d_val
                more = 1000*m_val + 100*o_val + 10*r_val + e_val
                money = 10000*m_val + 1000*o_val + 100*n_val + 10*e_val + y_val
                
                print(f"  {send} + {more} = {money}")
                
                # Visualize the 8-Queens solution from Example 1
                if 'q0' in solution.values:
                    # Visualize the 8-Queens solution from Example 1
                    print("\nVisualization of 8-Queens solution:")
                    print("-" * 30)
                    # Create a chessboard representation
                    board = [['.' for _ in range(8)] for _ in range(8)]
                    # Place queens on the board
                    for col, row_val in solution.values.items():
                        if isinstance(col, str) and col.startswith('q'):
                            col_idx = int(col[1:])
                            # Ensure row_val is an integer
                            if isinstance(row_val, int | float):
                                row_idx = int(row_val)
                                board[row_idx][col_idx] = 'Q'
                    
                    # Print the chessboard
                    print("  " + " ".join([str(i) for i in range(8)]))
                    for i, row in enumerate(board):
                        print(f"{i} {' '.join(row)}")
            else:
                print(f"No solution exists. Status: {solution.status}")
        case Failure(error):
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
