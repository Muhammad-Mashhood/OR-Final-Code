import sys
sys.path.insert(0, 'd:\\OR Final Code')

from final_code import parse_hungarian_problem

result = parse_hungarian_problem('problem.txt')
if result:
    print("SUCCESS!")
    print(f"Problem type: {'MAX' if result['is_max'] else 'MIN'}")
    print(f"Matrix size: {result['n']}x{result['m']}")
    print(f"Matrix: {result['matrix']}")
else:
    print("FAILED!")
