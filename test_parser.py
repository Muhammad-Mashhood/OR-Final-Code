# Test the file parser
import sys
sys.path.insert(0, 'd:/OR Final Code')
from final_code import read_problem_from_file

problem = read_problem_from_file('d:/OR Final Code/problem.txt')

if problem:
    print("Problem loaded successfully!")
    print(f"Type: {'Maximization' if problem['is_max'] else 'Minimization'}")
    print(f"Variables: {problem['num_vars']}")
    print(f"Constraints: {problem['num_constraints']}")
    print(f"Objective coefficients: {problem['obj_coef']}")
    print(f"Constraint types: {problem['constraint_types']}")
    print(f"Constraints:")
    for i, (constraint, ct, rhs) in enumerate(zip(problem['constraints'], problem['constraint_types'], problem['rhs'])):
        ct_symbol = {1: '<=', 2: '>=', 3: '='}[ct]
        print(f"  {constraint} {ct_symbol} {rhs}")
else:
    print("Failed to load problem")
