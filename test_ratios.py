# Quick test to verify ratio column
import sys
sys.path.insert(0, 'd:/OR Final Code')

# Test problem
problem = {
    'is_max': True,
    'num_vars': 2,
    'num_constraints': 3,
    'obj_coef': [3, 5],
    'constraints': [[1, 0], [0, 2], [3, 2]],
    'constraint_types': [1, 2, 3],
    'rhs': [4, 12, 18]
}

from final_code import setup_big_m_table, print_simplex_table

table, basic_vars, var_names, cj, cb, M, artificial_count = setup_big_m_table(problem, 1000)

print("Test 1: Initial table (no ratios)")
zj, zj_cj = print_simplex_table(table, basic_vars, var_names, cj, cb, 0, M)

print("\n\nTest 2: Table with ratios for column 1 (x2)")
zj, zj_cj = print_simplex_table(table, basic_vars, var_names, cj, cb, 0, M, pivot_col=1)
