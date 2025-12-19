# Test knapsack file loading
import sys
sys.path.insert(0, r'd:\OR Final Code')

# Mock the file to be problem.txt temporarily
import shutil
shutil.copy(r'd:\OR Final Code\knapsack_example.txt', r'd:\OR Final Code\problem.txt')

# Now test the parse function
exec(open(r'd:\OR Final Code\final_code.py').read())

# Test the parser
result = parse_knapsack_problem('problem.txt')
if result:
    print("\n✓ File parsing successful!")
    print(f"  Capacity: {result['capacity']}")
    print(f"  Number of items: {result['n']}")
    print(f"  Weights: {result['weights']}")
    print(f"  Values: {result['values']}")
    print(f"  Names: {result['item_names']}")
else:
    print("\n✗ File parsing failed")
