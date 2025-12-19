from final_code import parse_distance_matrix, solve_tsp_branch_and_bound

m = parse_distance_matrix('problem.txt')
if m is None:
    print('Failed to read matrix')
else:
    tour,cost = solve_tsp_branch_and_bound(m,['A','B','C','D','E'])
    print('\nResult tour:', tour)
    print('Result cost:', cost)
