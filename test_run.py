import subprocess
import time

# Send inputs: choice 6 (primal to dual), choice 2 (load from file), then Enter keys
inputs = "6\n2\n" + "\n" * 25 + "n\n"

process = subprocess.Popen(
    ['python', 'final_code.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

stdout, stderr = process.communicate(input=inputs, timeout=30)

print(stdout)
if stderr:
    print("STDERR:", stderr)
