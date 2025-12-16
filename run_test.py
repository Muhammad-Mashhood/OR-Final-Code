import subprocess
import sys

# Prepare input
input_data = """3
1
2
3
3
5
1
0
1
4
0
2
2
12
3
2
3
18
y

n
"""

# Run the program
result = subprocess.run(
    [sys.executable, "final_code.py"],
    cwd="d:/OR Final Code",
    input=input_data,
    capture_output=True,
    text=True
)

print("STDOUT:")
print(result.stdout[:2000])
print("\nSTDERR:")
print(result.stderr[:1000])

output = result.stdout
lines = output.split('\n')

# Find and print the iteration 0 section
print("\nSearching for ITERATION 0...")
for i, line in enumerate(lines):
    if "ITERATION 0" in line:
        print(f"Found at line {i}")
        # Print 25 lines from this point
        for j in range(i-2, min(i+25, len(lines))):
            print(lines[j])
        break
else:
    print("ITERATION 0 not found!")
