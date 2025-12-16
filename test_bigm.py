# Quick test to debug the Big M table setup issue

# Problem: 3 constraints but only 2 rows show in iteration 0

problem = {
    'is_max': True,
    'num_vars': 2,
    'num_constraints': 3,
    'obj_coef': [3, 5],
    'constraints': [[1, 0], [0, 2], [3, 2]],
    'constraint_types': [1, 2, 3],  # <=, >=, =
    'rhs': [4, 12, 18]
}

# Import functions from final_code
import sys
sys.path.insert(0, 'd:/OR Final Code')
from final_code import setup_big_m_table

table, basic_vars, var_names, cj, cb, M_val, artificial_count = setup_big_m_table(problem, M=1000)

print(f"Number of constraints: {problem['num_constraints']}")
print(f"Number of rows in table: {len(table)}")
print(f"Basic variables: {basic_vars}")
print(f"Cb values: {cb}")
print(f"Variable names: {var_names}")
print(f"\nTable rows:")
for i, row in enumerate(table):
    print(f"  Row {i}: {row}")
print(f"\nRow lengths: {[len(row) for row in table]}")
