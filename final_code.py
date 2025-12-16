"""
Operations Research Exam Helper Tool
=====================================
Topics: Simplex Method, Big M Method
Base Python Only - No pip install required

Author: OR Exam Helper
"""

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def clear_screen():
    """Clear screen for better readability"""
    print("\n" + "="*80 + "\n")

def print_fraction(num, precision=4):
    """Convert number to clean string representation"""
    if abs(num - round(num)) < 1e-9:
        return str(int(round(num)))
    return f"{num:.{precision}f}".rstrip('0').rstrip('.')

def get_float_input(prompt):
    """Get float input with error handling"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_int_input(prompt):
    """Get integer input with error handling"""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")

# ============================================================================
# TABLE DISPLAY FUNCTIONS
# ============================================================================

def print_simplex_table(table, basic_vars, var_names, cj, cb, iteration, M=None):
    """
    Print the simplex tableau in exam-friendly format
    
    Format:
    Cj ->        c1    c2    ...
    Cb    B      A1    A2    ...    Xb
    ...
    Zj-Cj        ...               Profit
    """
    print(f"\n{'='*80}")
    print(f"ITERATION {iteration}")
    print('='*80)
    
    num_vars = len(var_names)
    col_width = 10
    
    # Print Cj row
    print(f"{'Cj':<{col_width}}", end="")
    print(f"{'':<{col_width}}", end="")  # Empty space for B column
    for j in range(num_vars):
        cj_val = format_coefficient(cj[j], M)
        print(f"{cj_val:>{col_width}}", end="")
    print(f"{'Xb':>{col_width}}")
    
    print("-" * (col_width * (num_vars + 3)))
    
    # Print header row
    print(f"{'Cb':<{col_width}}", end="")
    print(f"{'B':<{col_width}}", end="")
    for name in var_names:
        print(f"{name:>{col_width}}", end="")
    print(f"{'(RHS)':>{col_width}}")
    
    print("-" * (col_width * (num_vars + 3)))
    
    # Print constraint rows
    num_constraints = len(table)
    for i in range(num_constraints):
        cb_val = format_coefficient(cb[i], M)
        basic_var = basic_vars[i]
        
        # Build the row string
        row_str = f"{cb_val:<{col_width}}{basic_var:<{col_width}}"
        for j in range(num_vars):
            val = print_fraction(table[i][j])
            row_str += f"{val:>{col_width}}"
        rhs_val = print_fraction(table[i][-1])
        row_str += f"{rhs_val:>{col_width}}"
        
        # Print the entire row at once
        print(row_str)
    
    print("-" * (col_width * (num_vars + 3)))
    
    # Calculate and print Zj row
    zj = calculate_zj(table, cb, num_vars)
    print(f"{'Zj':<{col_width}}", end="")
    print(f"{'':<{col_width}}", end="")
    for j in range(num_vars):
        print(f"{format_coefficient(zj[j], M):>{col_width}}", end="")
    print(f"{format_coefficient(zj[-1], M):>{col_width}}")
    
    # Calculate and print Zj-Cj row
    zj_cj = calculate_zj_cj(zj, cj, M)
    print(f"{'Zj-Cj':<{col_width}}", end="")
    print(f"{'':<{col_width}}", end="")
    for j in range(num_vars):
        print(f"{format_coefficient(zj_cj[j], M):>{col_width}}", end="")
    
    # Print profit/Z value
    profit = zj[-1]
    print(f"{'Z=' + format_coefficient(profit, M):>{col_width}}")
    
    print('='*80)
    
    return zj, zj_cj

def format_coefficient(val, M=None):
    """Format coefficient, handling Big M values"""
    if M is None:
        return print_fraction(val)
    
    # Check if value contains M component
    if isinstance(val, tuple):
        const, m_coef = val
        if abs(m_coef) < 1e-9:
            return print_fraction(const)
        elif abs(const) < 1e-9:
            if abs(m_coef - 1) < 1e-9:
                return "M"
            elif abs(m_coef + 1) < 1e-9:
                return "-M"
            else:
                return f"{print_fraction(m_coef)}M"
        else:
            sign = "+" if m_coef > 0 else ""
            if abs(m_coef - 1) < 1e-9:
                return f"{print_fraction(const)}{sign}M"
            elif abs(m_coef + 1) < 1e-9:
                return f"{print_fraction(const)}-M"
            else:
                return f"{print_fraction(const)}{sign}{print_fraction(m_coef)}M"
    return print_fraction(val)

def calculate_zj(table, cb, num_vars):
    """Calculate Zj values for each column"""
    num_constraints = len(table)
    zj = []
    
    # For each column (including RHS)
    for j in range(num_vars + 1):
        col_idx = j if j < num_vars else -1
        zj_val = sum(cb[i] * table[i][col_idx] for i in range(num_constraints))
        zj.append(zj_val)
    
    return zj

def calculate_zj_cj(zj, cj, M=None):
    """Calculate Zj - Cj values"""
    zj_cj = []
    for j in range(len(cj)):
        zj_cj.append(zj[j] - cj[j])
    return zj_cj

# ============================================================================
# FILE INPUT PARSER
# ============================================================================

def parse_expression(expr):
    """
    Parse a linear expression like '3x1 + 2x2 - x3' and return coefficients
    Returns: dict of {variable: coefficient}
    """
    import re
    
    # Remove spaces
    expr = expr.replace(' ', '')
    
    # Dictionary to store coefficients
    coef_dict = {}
    
    # Pattern to match terms like +3x1, -2x2, x3, +x4, -x5
    # Matches: optional sign, optional number, variable
    pattern = r'([+-]?)(\d*\.?\d*)([x]\d+)'
    
    matches = re.findall(pattern, expr)
    
    for sign, coef, var in matches:
        # Handle coefficient
        if coef == '':
            coef_val = 1.0
        else:
            coef_val = float(coef)
        
        # Handle sign
        if sign == '-':
            coef_val = -coef_val
        
        coef_dict[var] = coef_val
    
    return coef_dict

def parse_constraint(line):
    """
    Parse a constraint like 'x1 + 3x2 <= 5' or '2x2 >= 10'
    Returns: (coef_dict, constraint_type, rhs)
    constraint_type: 1 for <=, 2 for >=, 3 for =
    """
    line = line.strip()
    
    # Determine constraint type
    if '<=' in line:
        constraint_type = 1
        parts = line.split('<=')
    elif '>=' in line:
        constraint_type = 2
        parts = line.split('>=')
    elif '=' in line:
        constraint_type = 3
        parts = line.split('=')
    else:
        raise ValueError(f"Invalid constraint: {line}")
    
    if len(parts) != 2:
        raise ValueError(f"Invalid constraint format: {line}")
    
    lhs = parts[0].strip()
    rhs = float(parts[1].strip())
    
    # Parse LHS
    coef_dict = parse_expression(lhs)
    
    return coef_dict, constraint_type, rhs

def read_problem_from_file(filename='problem.txt'):
    """
    Read problem from text file
    Format:
    Line 1: max or min
    Line 2: z = x1 + 2x2 + ...
    Line 3+: constraints like x1 + 3x2 <= 5
    """
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        if len(lines) < 3:
            print("Error: File must have at least 3 lines (objective type, objective function, and at least one constraint)")
            return None
        
        # Parse objective type
        obj_type = lines[0].lower()
        if obj_type not in ['max', 'min', 'maximize', 'minimize']:
            print(f"Error: First line must be 'max' or 'min', got '{lines[0]}'")
            return None
        is_max = obj_type in ['max', 'maximize']
        
        # Parse objective function
        obj_line = lines[1]
        if 'z=' in obj_line.lower():
            obj_line = obj_line.lower().split('z=')[1]
        elif 'z =' in obj_line.lower():
            obj_line = obj_line.lower().split('z =')[1]
        
        obj_coef_dict = parse_expression(obj_line)
        
        # Parse constraints
        constraints_data = []
        for i in range(2, len(lines)):
            coef_dict, constraint_type, rhs = parse_constraint(lines[i])
            constraints_data.append((coef_dict, constraint_type, rhs))
        
        # Determine number of variables
        all_vars = set()
        all_vars.update(obj_coef_dict.keys())
        for coef_dict, _, _ in constraints_data:
            all_vars.update(coef_dict.keys())
        
        # Sort variables (x1, x2, x3, ...)
        var_list = sorted(all_vars, key=lambda x: int(x[1:]))
        num_vars = len(var_list)
        num_constraints = len(constraints_data)
        
        # Build objective coefficient array
        obj_coef = []
        for var in var_list:
            obj_coef.append(obj_coef_dict.get(var, 0.0))
        
        # Build constraint arrays
        constraints = []
        constraint_types = []
        rhs = []
        
        for coef_dict, constraint_type, rhs_val in constraints_data:
            constraint_row = []
            for var in var_list:
                constraint_row.append(coef_dict.get(var, 0.0))
            constraints.append(constraint_row)
            constraint_types.append(constraint_type)
            rhs.append(rhs_val)
        
        problem = {
            'is_max': is_max,
            'num_vars': num_vars,
            'num_constraints': num_constraints,
            'obj_coef': obj_coef,
            'constraints': constraints,
            'constraint_types': constraint_types,
            'rhs': rhs
        }
        
        return problem
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# ============================================================================
# SIMPLEX METHOD FUNCTIONS
# ============================================================================

def input_problem():
    """Input the optimization problem from user"""
    print("\n" + "="*80)
    print("PROBLEM INPUT")
    print("="*80)
    
    # Problem type
    print("\nProblem Type:")
    print("1. Maximization")
    print("2. Minimization")
    prob_type = get_int_input("Enter choice (1/2): ")
    is_max = (prob_type == 1)
    
    # Number of variables and constraints
    num_vars = get_int_input("\nEnter number of decision variables (x1, x2, ...): ")
    num_constraints = get_int_input("Enter number of constraints: ")
    
    # Objective function coefficients
    print(f"\nEnter coefficients of objective function Z:")
    print(f"Z = c1*x1 + c2*x2 + ... + c{num_vars}*x{num_vars}")
    obj_coef = []
    for i in range(num_vars):
        coef = get_float_input(f"  c{i+1} (coefficient of x{i+1}): ")
        obj_coef.append(coef)
    
    # Constraints
    print(f"\nEnter constraints (assume all xi >= 0):")
    print("Constraint types: 1 for <=, 2 for >=, 3 for =")
    
    constraints = []
    constraint_types = []
    rhs = []
    
    for i in range(num_constraints):
        print(f"\nConstraint {i+1}:")
        coefs = []
        for j in range(num_vars):
            coef = get_float_input(f"  Coefficient of x{j+1}: ")
            coefs.append(coef)
        
        con_type = get_int_input("  Constraint type (1: <=, 2: >=, 3: =): ")
        rhs_val = get_float_input("  RHS value: ")
        
        constraints.append(coefs)
        constraint_types.append(con_type)
        rhs.append(rhs_val)
    
    return {
        'is_max': is_max,
        'num_vars': num_vars,
        'num_constraints': num_constraints,
        'obj_coef': obj_coef,
        'constraints': constraints,
        'constraint_types': constraint_types,
        'rhs': rhs
    }

def detect_method(problem):
    """Detect which method should be used based on constraint types"""
    constraint_types = problem['constraint_types']
    
    # If all constraints are <=, use Simplex
    # If any constraint is >= or =, use Big M
    needs_big_m = any(ct in [2, 3] for ct in constraint_types)
    
    if needs_big_m:
        return "BIG_M"
    else:
        return "SIMPLEX"

def setup_simplex_table(problem):
    """
    Setup initial simplex tableau
    Adds slack variables for <= constraints
    """
    num_vars = problem['num_vars']
    num_constraints = problem['num_constraints']
    constraints = problem['constraints']
    rhs = problem['rhs']
    obj_coef = problem['obj_coef']
    is_max = problem['is_max']
    
    # Variable names
    var_names = [f"x{i+1}" for i in range(num_vars)]
    
    # Add slack variables
    for i in range(num_constraints):
        var_names.append(f"s{i+1}")
    
    # Total variables
    total_vars = num_vars + num_constraints
    
    # Build table
    table = []
    for i in range(num_constraints):
        row = constraints[i].copy()
        # Add slack variable columns
        for j in range(num_constraints):
            if i == j:
                row.append(1.0)
            else:
                row.append(0.0)
        row.append(rhs[i])  # RHS
        table.append(row)
    
    # Cj coefficients
    cj = obj_coef.copy()
    # Slack variables have 0 coefficient
    cj.extend([0.0] * num_constraints)
    
    # If minimization, negate Cj (we'll negate back at the end)
    if not is_max:
        cj = [-c for c in cj]
    
    # Basic variables (slack variables initially)
    basic_vars = [f"s{i+1}" for i in range(num_constraints)]
    
    # Cb (coefficients of basic variables)
    cb = [0.0] * num_constraints
    
    return table, basic_vars, var_names, cj, cb

def setup_big_m_table(problem, M=1000):
    """
    Setup initial Big M tableau
    Adds slack (<=), surplus and artificial (>=), artificial (=) variables
    """
    num_vars = problem['num_vars']
    num_constraints = problem['num_constraints']
    constraints = problem['constraints']
    constraint_types = problem['constraint_types']
    rhs = problem['rhs']
    obj_coef = problem['obj_coef']
    is_max = problem['is_max']
    
    # Count each type of additional variable needed
    slack_count = 0
    surplus_count = 0
    artificial_count = 0
    
    var_info = []  # Track what variables to add for each constraint
    
    for i, ct in enumerate(constraint_types):
        if ct == 1:  # <=
            slack_count += 1
            var_info.append({'slack': slack_count, 'surplus': None, 'artificial': None})
        elif ct == 2:  # >=
            surplus_count += 1
            artificial_count += 1
            var_info.append({'slack': None, 'surplus': surplus_count, 'artificial': artificial_count})
        else:  # =
            artificial_count += 1
            var_info.append({'slack': None, 'surplus': None, 'artificial': artificial_count})
    
    # Variable names
    var_names = [f"x{i+1}" for i in range(num_vars)]
    
    # Add slack variable names
    for i in range(1, slack_count + 1):
        var_names.append(f"s{i}")
    
    # Add surplus variable names
    for i in range(1, surplus_count + 1):
        var_names.append(f"S{i}")
    
    # Add artificial variable names
    for i in range(1, artificial_count + 1):
        var_names.append(f"A{i}")
    
    total_vars = num_vars + slack_count + surplus_count + artificial_count
    
    # Build table
    table = []
    basic_vars = []
    cb = []
    
    slack_idx = num_vars
    surplus_idx = num_vars + slack_count
    artificial_idx = num_vars + slack_count + surplus_count
    
    current_slack = 0
    current_surplus = 0
    current_artificial = 0
    
    for i in range(num_constraints):
        row = constraints[i].copy()
        
        # Initialize all additional variable columns to 0
        row.extend([0.0] * (slack_count + surplus_count + artificial_count))
        
        ct = constraint_types[i]
        
        if ct == 1:  # <= : add slack
            current_slack += 1
            row[slack_idx + current_slack - 1] = 1.0
            basic_vars.append(f"s{current_slack}")
            cb.append(0.0)
        elif ct == 2:  # >= : add surplus (-1) and artificial (+1)
            current_surplus += 1
            current_artificial += 1
            row[surplus_idx + current_surplus - 1] = -1.0
            row[artificial_idx + current_artificial - 1] = 1.0
            basic_vars.append(f"A{current_artificial}")
            if is_max:
                cb.append(-M)  # -M for maximization
            else:
                cb.append(M)   # +M for minimization
        else:  # = : add artificial only
            current_artificial += 1
            row[artificial_idx + current_artificial - 1] = 1.0
            basic_vars.append(f"A{current_artificial}")
            if is_max:
                cb.append(-M)
            else:
                cb.append(M)
        
        row.append(rhs[i])  # RHS
        table.append(row)
    
    # Cj coefficients
    cj = obj_coef.copy()
    cj.extend([0.0] * slack_count)    # Slack variables
    cj.extend([0.0] * surplus_count)  # Surplus variables
    
    # Artificial variables
    for i in range(artificial_count):
        if is_max:
            cj.append(-M)  # -M for maximization (penalty)
        else:
            cj.append(M)   # +M for minimization (penalty)
    
    # If minimization, negate Cj
    if not is_max:
        cj = [-c for c in cj]
        cb = [-c for c in cb]
    
    return table, basic_vars, var_names, cj, cb, M, artificial_count

def find_pivot_column(zj_cj, var_names):
    """
    Find pivot column (entering variable)
    For maximization: most negative Zj-Cj
    Returns column index and value
    """
    min_val = 0
    pivot_col = -1
    
    for j in range(len(zj_cj)):
        if zj_cj[j] < min_val:
            min_val = zj_cj[j]
            pivot_col = j
    
    return pivot_col, min_val

def find_pivot_row(table, pivot_col, basic_vars):
    """
    Find pivot row (leaving variable)
    Using minimum ratio test (RHS / pivot column element)
    Only consider positive elements
    """
    min_ratio = float('inf')
    pivot_row = -1
    ratios = []
    
    print("\nRatio Test (Minimum Ratio Rule):")
    print("-" * 40)
    
    for i in range(len(table)):
        element = table[i][pivot_col]
        rhs = table[i][-1]
        
        if element > 1e-9:  # Positive element
            ratio = rhs / element
            ratios.append(ratio)
            print(f"  Row {i+1} ({basic_vars[i]}): {print_fraction(rhs)} / {print_fraction(element)} = {print_fraction(ratio)}")
            
            if ratio < min_ratio and ratio >= 0:
                min_ratio = ratio
                pivot_row = i
        else:
            ratios.append(float('inf'))
            print(f"  Row {i+1} ({basic_vars[i]}): {print_fraction(rhs)} / {print_fraction(element)} = Not applicable (element <= 0)")
    
    return pivot_row, min_ratio, ratios

def perform_pivot_operation(table, pivot_row, pivot_col, basic_vars, var_names, cb, cj):
    """
    Perform pivot operation to get new tableau
    """
    num_rows = len(table)
    num_cols = len(table[0])
    
    pivot_element = table[pivot_row][pivot_col]
    
    print(f"\nPivot Element: {print_fraction(pivot_element)}")
    print(f"Pivot Position: Row {pivot_row + 1}, Column {pivot_col + 1}")
    
    # Create new table
    new_table = [[0.0] * num_cols for _ in range(num_rows)]
    
    # Step 1: Divide pivot row by pivot element
    print(f"\nStep 1: New Pivot Row = Old Pivot Row / {print_fraction(pivot_element)}")
    for j in range(num_cols):
        new_table[pivot_row][j] = table[pivot_row][j] / pivot_element
    
    # Step 2: Make other elements in pivot column = 0
    print("Step 2: For other rows: New Row = Old Row - (element in pivot column) × New Pivot Row")
    
    for i in range(num_rows):
        if i != pivot_row:
            factor = table[i][pivot_col]
            print(f"  Row {i+1}: Factor = {print_fraction(factor)}")
            for j in range(num_cols):
                new_table[i][j] = table[i][j] - factor * new_table[pivot_row][j]
    
    # Update basic variables
    new_basic_vars = basic_vars.copy()
    new_basic_vars[pivot_row] = var_names[pivot_col]
    
    # Update Cb
    new_cb = cb.copy()
    new_cb[pivot_row] = cj[pivot_col]
    
    return new_table, new_basic_vars, new_cb

def check_optimality(zj_cj):
    """Check if current solution is optimal (all Zj-Cj >= 0)"""
    return all(val >= -1e-9 for val in zj_cj)

def check_unbounded(table, pivot_col):
    """Check if problem is unbounded (all elements in pivot column <= 0)"""
    for i in range(len(table)):
        if table[i][pivot_col] > 1e-9:
            return False
    return True

def check_infeasible(basic_vars, table, artificial_vars):
    """Check if problem is infeasible (artificial variable in basis with positive value)"""
    for i, var in enumerate(basic_vars):
        if var.startswith('A') and table[i][-1] > 1e-9:
            return True
    return False

def extract_solution(table, basic_vars, var_names, is_max):
    """Extract the final solution"""
    solution = {}
    
    for var in var_names:
        solution[var] = 0.0
    
    for i, var in enumerate(basic_vars):
        solution[var] = table[i][-1]
    
    return solution

def print_solution(solution, var_names, zj, is_max, num_original_vars):
    """Print the final optimal solution"""
    print("\n" + "="*80)
    print("OPTIMAL SOLUTION FOUND!")
    print("="*80)
    
    print("\nDecision Variables:")
    for i in range(num_original_vars):
        var = f"x{i+1}"
        print(f"  {var} = {print_fraction(solution.get(var, 0))}")
    
    z_value = zj[-1]
    if not is_max:
        z_value = -z_value
    
    print(f"\nOptimal Value of Z = {print_fraction(z_value)}")
    
    print("\nSlack/Surplus Variables:")
    for var in var_names:
        if var.startswith('s') or var.startswith('S'):
            print(f"  {var} = {print_fraction(solution.get(var, 0))}")

def solve_simplex(problem):
    """Main function to solve using Simplex Method"""
    print("\n" + "#"*80)
    print("SOLVING USING SIMPLEX METHOD")
    print("#"*80)
    
    # Setup initial table
    table, basic_vars, var_names, cj, cb = setup_simplex_table(problem)
    
    iteration = 0
    
    # Print initial table
    zj, zj_cj = print_simplex_table(table, basic_vars, var_names, cj, cb, iteration)
    
    while True:
        # Check optimality
        if check_optimality(zj_cj):
            solution = extract_solution(table, basic_vars, var_names, problem['is_max'])
            print_solution(solution, var_names, zj, problem['is_max'], problem['num_vars'])
            break
        
        # Find pivot column
        pivot_col, min_zj_cj = find_pivot_column(zj_cj, var_names)
        
        if pivot_col == -1:
            print("\nOptimal solution reached!")
            break
        
        print(f"\nEntering Variable: {var_names[pivot_col]} (most negative Zj-Cj = {print_fraction(min_zj_cj)})")
        
        # Check unboundedness
        if check_unbounded(table, pivot_col):
            print("\n" + "!"*80)
            print("UNBOUNDED SOLUTION!")
            print("The problem has no finite optimal solution.")
            print("!"*80)
            break
        
        # Find pivot row
        pivot_row, min_ratio, ratios = find_pivot_row(table, pivot_col, basic_vars)
        
        if pivot_row == -1:
            print("\nNo valid pivot row found. Problem may be unbounded.")
            break
        
        print(f"\nLeaving Variable: {basic_vars[pivot_row]} (minimum ratio = {print_fraction(min_ratio)})")
        
        # Wait for user to continue
        input("\n>>> Press Enter to perform pivot operation and see next iteration...")
        
        # Perform pivot operation
        table, basic_vars, cb = perform_pivot_operation(table, pivot_row, pivot_col, basic_vars, var_names, cb, cj)
        
        iteration += 1
        
        # Print new table
        zj, zj_cj = print_simplex_table(table, basic_vars, var_names, cj, cb, iteration)

def solve_big_m(problem):
    """Main function to solve using Big M Method"""
    print("\n" + "#"*80)
    print("SOLVING USING BIG M METHOD")
    print("#"*80)
    
    M = 1000  # Big M value (symbolic)
    
    # Setup initial table
    table, basic_vars, var_names, cj, cb, M_val, artificial_count = setup_big_m_table(problem, M)
    
    # Track artificial variables for infeasibility check
    artificial_vars = [f"A{i+1}" for i in range(artificial_count)]
    
    print(f"\nNote: M is used as a large penalty value (M = {M})")
    print(f"Artificial variables added: {', '.join(artificial_vars)}")
    
    iteration = 0
    
    # Print initial table
    zj, zj_cj = print_simplex_table(table, basic_vars, var_names, cj, cb, iteration, M_val)
    
    while True:
        # Check optimality
        if check_optimality(zj_cj):
            # Check infeasibility
            if check_infeasible(basic_vars, table, artificial_vars):
                print("\n" + "!"*80)
                print("INFEASIBLE SOLUTION!")
                print("Artificial variable(s) in the final basis with positive value.")
                print("The problem has no feasible solution.")
                print("!"*80)
            else:
                solution = extract_solution(table, basic_vars, var_names, problem['is_max'])
                print_solution(solution, var_names, zj, problem['is_max'], problem['num_vars'])
            break
        
        # Find pivot column
        pivot_col, min_zj_cj = find_pivot_column(zj_cj, var_names)
        
        if pivot_col == -1:
            print("\nOptimal solution reached!")
            break
        
        print(f"\nEntering Variable: {var_names[pivot_col]} (most negative Zj-Cj = {print_fraction(min_zj_cj)})")
        
        # Check unboundedness
        if check_unbounded(table, pivot_col):
            print("\n" + "!"*80)
            print("UNBOUNDED SOLUTION!")
            print("The problem has no finite optimal solution.")
            print("!"*80)
            break
        
        # Find pivot row
        pivot_row, min_ratio, ratios = find_pivot_row(table, pivot_col, basic_vars)
        
        if pivot_row == -1:
            print("\nNo valid pivot row found. Problem may be unbounded.")
            break
        
        print(f"\nLeaving Variable: {basic_vars[pivot_row]} (minimum ratio = {print_fraction(min_ratio)})")
        
        # Wait for user to continue
        input("\n>>> Press Enter to perform pivot operation and see next iteration...")
        
        # Perform pivot operation
        table, basic_vars, cb = perform_pivot_operation(table, pivot_row, pivot_col, basic_vars, var_names, cb, cj)
        
        iteration += 1
        
        # Print new table
        zj, zj_cj = print_simplex_table(table, basic_vars, var_names, cj, cb, iteration, M_val)

# ============================================================================
# MAIN MENU
# ============================================================================

def print_problem_summary(problem):
    """Print the entered problem for verification"""
    print("\n" + "="*80)
    print("PROBLEM SUMMARY")
    print("="*80)
    
    # Objective function
    obj_type = "Maximize" if problem['is_max'] else "Minimize"
    obj_terms = []
    for i, c in enumerate(problem['obj_coef']):
        if c >= 0:
            if i == 0:
                obj_terms.append(f"{print_fraction(c)}x{i+1}")
            else:
                obj_terms.append(f"+ {print_fraction(c)}x{i+1}")
        else:
            obj_terms.append(f"- {print_fraction(abs(c))}x{i+1}")
    
    print(f"\n{obj_type} Z = {' '.join(obj_terms)}")
    
    # Constraints
    print("\nSubject to:")
    constraint_symbols = {1: '<=', 2: '>=', 3: '='}
    
    for i in range(problem['num_constraints']):
        terms = []
        for j, c in enumerate(problem['constraints'][i]):
            if c >= 0:
                if j == 0:
                    terms.append(f"{print_fraction(c)}x{j+1}")
                else:
                    terms.append(f"+ {print_fraction(c)}x{j+1}")
            else:
                terms.append(f"- {print_fraction(abs(c))}x{j+1}")
        
        symbol = constraint_symbols[problem['constraint_types'][i]]
        print(f"  {' '.join(terms)} {symbol} {print_fraction(problem['rhs'][i])}")
    
    print(f"\n  x1, x2, ... x{problem['num_vars']} >= 0")

def main():
    """Main function with menu"""
    print("\n" + "="*80)
    print("   OPERATIONS RESEARCH EXAM HELPER")
    print("   Simplex Method & Big M Method Solver")
    print("="*80)
    
    while True:
        print("\n" + "-"*40)
        print("MAIN MENU")
        print("-"*40)
        print("1. Simplex Method (Manual Input)")
        print("2. Big M Method (Manual Input)")
        print("3. Auto-Detect Method (Manual Input)")
        print("4. Load from File (problem.txt)")
        print("5. Exit")
        print("-"*40)
        
        choice = get_int_input("Enter your choice (1-5): ")
        
        if choice == 5:
            print("\nThank you for using OR Exam Helper. Good luck!")
            break
        
        if choice not in [1, 2, 3, 4]:
            print("Invalid choice. Please try again.")
            continue
        
        # Input the problem
        if choice == 4:
            # Load from file
            print("\nLoading problem from 'problem.txt'...")
            problem = read_problem_from_file('problem.txt')
            if problem is None:
                print("Failed to load problem from file.")
                continue
            print("Problem loaded successfully!")
        else:
            # Manual input
            problem = input_problem()
        
        # Print problem summary
        print_problem_summary(problem)
        
        if choice != 4:  # Skip confirmation for file input
            confirm = input("\nIs this correct? (y/n): ").lower()
            if confirm != 'y':
                print("Please re-enter the problem.")
                continue
        else:
            input("\nPress Enter to solve...")
        
        if choice == 1:
            # Check if all constraints are <=
            if any(ct != 1 for ct in problem['constraint_types']):
                print("\n⚠ WARNING: Simplex method requires all constraints to be <= type.")
                print("Consider using Big M method for >= or = constraints.")
                proceed = input("Do you want to continue anyway? (y/n): ").lower()
                if proceed != 'y':
                    continue
            solve_simplex(problem)
        
        elif choice == 2:
            solve_big_m(problem)
        
        elif choice in [3, 4]:
            # Auto-detect method
            method = detect_method(problem)
            if method == "SIMPLEX":
                print("\n" + "*"*80)
                print("AUTO-DETECTION: All constraints are <= type.")
                print("This problem will be solved using SIMPLEX METHOD.")
                print("*"*80)
                input("\nPress Enter to continue...")
                solve_simplex(problem)
            else:
                print("\n" + "*"*80)
                print("AUTO-DETECTION: Problem contains >= or = constraints.")
                print("This problem will be solved using BIG M METHOD.")
                print("*"*80)
                input("\nPress Enter to continue...")
                solve_big_m(problem)
        
        # Ask if user wants to solve another problem
        another = input("\n\nDo you want to solve another problem? (y/n): ").lower()
        if another != 'y':
            print("\nThank you for using OR Exam Helper. Good luck!")
            break

# ============================================================================
# RUN THE PROGRAM
# ============================================================================

if __name__ == "__main__":
    main()
