import subprocess

# Test Hungarian Method
# Simple 3x3 minimization problem
inputs = """8
1
3
3
9
2
7
6
8
3
5
4
8



n
"""

process = subprocess.Popen(
    ['python', 'final_code.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

stdout, stderr = process.communicate(input=inputs, timeout=60)

print(stdout)
if stderr:
    print("\nSTDERR:")
    print(stderr)
