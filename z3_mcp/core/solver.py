from typing import cast

from returns.maybe import Maybe, Nothing, Some
from returns.result import Failure, Result, Success
from z3 import (
    And,
    Bool,
    BoolRef,
    CheckSatResult,
    Distinct,
    Exists,
    ForAll,
    If,
    Implies,
    Int,
    ModelRef,
    Not,
    Or,
    Real,
    Solver,
    String,
    is_bool,
    is_int,
    is_real,
    is_true,
    sat,
)

from z3_poc.models.constraints import (
    Constraint,
    Problem,
    Solution,
    Variable,
    VariableType,
    Z3Ref,
    Z3Value,
)


def create_variable(variable: Variable) -> Result[tuple[str, Z3Ref], str]:
    """Create a Z3 variable from a Variable model.
    
    Args:
        variable: The variable definition
        
    Returns:
        Result containing a tuple of (variable_name, z3_variable) or an error message
    """
    try:
        name = variable.name
        match variable.type:
            case VariableType.INTEGER:
                return Success((name, cast(Z3Ref, Int(name))))
            case VariableType.REAL:
                return Success((name, cast(Z3Ref, Real(name))))
            case VariableType.BOOLEAN:
                return Success((name, cast(Z3Ref, Bool(name))))
            case VariableType.STRING:
                return Success((name, cast(Z3Ref, String(name))))
            case _:
                return Failure(f"Unsupported variable type: {variable.type}")
    except Exception as e:
        return Failure(f"Error creating variable {variable.name}: {e!s}")


def create_variables(variables: list[Variable]) -> Result[dict[str, Z3Ref], str]:
    """Create Z3 variables from variable definitions.
    
    Args:
        variables: List of variable definitions
        
    Returns:
        Result containing a dictionary of variable names to Z3 variables or an error message
    """
    result_dict = {}
    
    for var in variables:
        result = create_variable(var)
        match result:
            case Success(value):
                name, z3_var = value
                result_dict[name] = z3_var
            case Failure(_):
                return result
    
    return Success(result_dict)


def parse_constraint(constraint: Constraint, variables: dict[str, Z3Ref]) -> Result[BoolRef, str]:
    """Parse a constraint expression into a Z3 constraint.
    
    Args:
        constraint: The constraint definition
        variables: Dictionary of variable names to Z3 variables
        
    Returns:
        Result containing a Z3 constraint or an error message
    """
    try:
        # Create a local dictionary with Z3 variables and functions
        local_dict = {**variables, **{
            'And': And, 'Or': Or, 'Not': Not, 'Implies': Implies,
            'ForAll': ForAll, 'Exists': Exists,
            'If': If, 'Distinct': Distinct,
            'true': True, 'false': False
        }}
        
        # Evaluate the expression in the context of the local dictionary
        z3_constraint = eval(constraint.expression, {"__builtins__": {}}, local_dict)
        return Success(z3_constraint)
    except Exception as e:
        return Failure(f"Error parsing constraint '{constraint.expression}': {e!s}")


def create_constraints(constraints: list[Constraint], variables: dict[str, Z3Ref]) -> Result[list[BoolRef], str]:
    """Create Z3 constraints from constraint definitions.
    
    Args:
        constraints: List of constraint definitions
        variables: Dictionary of variable names to Z3 variables
        
    Returns:
        Result containing a list of Z3 constraints or an error message
    """
    z3_constraints = []
    
    for constraint in constraints:
        result = parse_constraint(constraint, variables)
        match result:
            case Success(value):
                z3_constraints.append(value)
            case Failure(_):
                return result
    
    return Success(z3_constraints)


def solve(variables: dict[str, Z3Ref], constraints: list[BoolRef]) -> Result[tuple[CheckSatResult, ModelRef | None], str]:
    """Solve a Z3 problem.
    
    Args:
        variables: Dictionary of variable names to Z3 variables
        constraints: List of Z3 constraints
        
    Returns:
        Result containing a tuple of (sat_result, model) or an error message
    """
    try:
        solver = Solver()
        solver.add(constraints)
        
        result = solver.check()
        model = None
        
        if result == sat:
            model = solver.model()
        
        return Success((result, model))
    except Exception as e:
        return Failure(f"Error solving constraints: {e!s}")


def get_z3_value(model: ModelRef, z3_var: Z3Ref) -> Maybe[Z3Value]:
    """Get a Z3 value from a model using Maybe for null handling.
    
    Args:
        model: The Z3 model
        z3_var: The Z3 variable
        
    Returns:
        Maybe containing the Z3 value or Nothing
    """
    try:
        z3_value = model[z3_var]
        if z3_value is None:
            return Nothing
        
        # Convert to string first, then parse based on type
        str_value = str(z3_value)
        
        # Use structural pattern matching to handle different types
        match z3_var:
            case _ if is_bool(z3_var):
                return Some(is_true(z3_value))
            case _ if is_int(z3_var):
                return Some(int(str_value))
            case _ if is_real(z3_var):
                # Parse rational numbers like "5/2"
                if '/' in str_value:
                    num_str, den_str = str_value.split('/')
                    return Some(float(int(num_str)) / float(int(den_str)))
                else:
                    return Some(float(str_value))
            case _:
                return Some(str_value)
    except Exception:
        return Nothing


def extract_solution(result: CheckSatResult, model: ModelRef | None, variables: dict[str, Z3Ref]) -> Result[Solution, str]:
    """Extract a solution from a Z3 model.
    
    Args:
        result: The satisfiability result
        model: The Z3 model (if satisfiable)
        variables: Dictionary of variable names to Z3 variables
        
    Returns:
        Result containing a Solution model or an error message
    """
    try:
        status = str(result)
        is_satisfiable = result == sat
        
        values: dict[str, Z3Value] = {}
        
        # Use pattern matching for model handling
        match (is_satisfiable, model):
            case (True, model) if model is not None:
                for name, z3_var in variables.items():
                    # Use Maybe to handle potential None values
                    maybe_value = get_z3_value(model, z3_var)
                    maybe_value.map(lambda value: values.update({name: value}))
            case _:
                # No values to extract
                pass
        
        return Success(Solution(
            values=values,
            is_satisfiable=is_satisfiable,
            status=status
        ))
    except Exception as e:
        return Failure(f"Error extracting solution: {e!s}")


def solve_problem(problem: Problem) -> Result[Solution, str]:
    """Solve a Z3 problem and return the solution.
    
    Args:
        problem: The problem definition
        
    Returns:
        Result containing a Solution or an error message
    """
    try:
        # Create variables
        vars_result = create_variables(problem.variables)
        if isinstance(vars_result, Failure):
            return vars_result
        
        variables = vars_result.unwrap()
        
        # Create constraints
        constraints_result = create_constraints(problem.constraints, variables)
        if isinstance(constraints_result, Failure):
            return constraints_result
        
        z3_constraints = constraints_result.unwrap()
        
        # Solve the problem
        solve_result = solve(variables, z3_constraints)
        if isinstance(solve_result, Failure):
            return solve_result
        
        result_tuple = solve_result.unwrap()
        
        # Extract the solution
        return extract_solution(result_tuple[0], result_tuple[1], variables)
    except Exception as e:
        return Failure(f"Error solving problem: {e!s}")
