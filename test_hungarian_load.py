"""Test Hungarian Method with file loading"""
import subprocess
import sys

# Test input: choice 8 (Hungarian), choice 2 (load from file), multiple enters to proceed
test_input = "8\n2\n" + "\n" * 30 + "n\n"

# Run the program
proc = subprocess.Popen(
    [sys.executable, "final_code.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

output, errors = proc.communicate(input=test_input, timeout=10)

# Print relevant output
lines = output.split('\n')
printing = False
for line in lines:
    if 'ASSIGNMENT PROBLEM' in line or 'Loading problem' in line or printing:
        printing = True
        print(line)
    if 'Do you want to solve another problem' in line:
        break

if errors:
    print("\n=== ERRORS ===")
    print(errors)
