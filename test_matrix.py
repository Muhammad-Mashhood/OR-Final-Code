import subprocess

# Test matrix method: choice 7, then choice 2 (load from file)
inputs = "7\n2\n" + "\n" * 10 + "n\n"

process = subprocess.Popen(
    ['python', 'final_code.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

stdout, stderr = process.communicate(input=inputs, timeout=60)

# Save to file for inspection
with open('matrix_test_output.txt', 'w', encoding='utf-8') as f:
    f.write(stdout)
    if stderr:
        f.write("\n\nSTDERR:\n")
        f.write(stderr)

print("Output saved to matrix_test_output.txt")
print("\n" + "="*80)
print("EXTRACT: Tableau Display")
print("="*80)

lines = stdout.split('\n')
in_tableau = False
for i, line in enumerate(lines):
    if 'SIMPLEX TABLEAU' in line:
        in_tableau = True
    if in_tableau:
        print(line)
        if line.strip() == '=' * 80:
            in_tableau = False
            if i > 100:  # Show first tableau only
                break
