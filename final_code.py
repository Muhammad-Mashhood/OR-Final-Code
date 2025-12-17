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

def print_simplex_table(table, basic_vars, var_names, cj, cb, iteration, M=None, pivot_col=None):
    """
    Print the simplex tableau in exam-friendly format
    
    Format:
    Cj ->        c1    c2    ...
    Cb    B      A1    A2    ...    Xb    Ratio
    ...
    Zj-Cj        ...               Profit
    """
    print(f"\n{'='*80}")
    print(f"ITERATION {iteration}")
    print('='*80)
    
    num_vars = len(var_names)
    col_width = 10
    
    # Calculate ratios if pivot column is provided
    ratios = []
    if pivot_col is not None:
        for i in range(len(table)):
            element = table[i][pivot_col]
            rhs = table[i][-1]
            if element > 1e-9:
                ratio = rhs / element
                ratios.append(ratio)
            else:
                ratios.append(None)
    else:
        ratios = [None] * len(table)
    
    # Print Cj row
    print(f"{'Cj':<{col_width}}", end="")
    print(f"{'':<{col_width}}", end="")  # Empty space for B column
    for j in range(num_vars):
        cj_val = format_coefficient(cj[j], M)
        print(f"{cj_val:>{col_width}}", end="")
    print(f"{'Xb':>{col_width}}", end="")
    if pivot_col is not None:  # Only show Ratio header if we have ratios
        print(f"{'Ratio':>{col_width}}")
        separator_length = col_width * (num_vars + 4)
    else:
        print()
        separator_length = col_width * (num_vars + 3)
    
    print("-" * separator_length)
    
    # Print header row
    print(f"{'Cb':<{col_width}}", end="")
    print(f"{'B':<{col_width}}", end="")
    for name in var_names:
        print(f"{name:>{col_width}}", end="")
    print(f"{'(RHS)':>{col_width}}", end="")
    if pivot_col is not None:
        print(f"{'':>{col_width}}")
    else:
        print()
    
    print("-" * separator_length)
    
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
        
        # Add ratio only if pivot_col is provided
        if pivot_col is not None:
            if ratios[i] is not None:
                ratio_str = print_fraction(ratios[i])
                row_str += f"{ratio_str:>{col_width}}"
            else:
                row_str += f"{'-':>{col_width}}"
        
        # Print the entire row at once
        print(row_str)
    
    print("-" * separator_length)
    
    # Calculate and print Zj row
    zj = calculate_zj(table, cb, num_vars)
    print(f"{'Zj':<{col_width}}", end="")
    print(f"{'':<{col_width}}", end="")
    for j in range(num_vars):
        print(f"{format_coefficient(zj[j], M):>{col_width}}", end="")
    print(f"{format_coefficient(zj[-1], M):>{col_width}}", end="")
    print(f"{'':>{col_width}}")
    
    # Calculate and print Zj-Cj row
    zj_cj = calculate_zj_cj(zj, cj, M)
    print(f"{'Zj-Cj':<{col_width}}", end="")
    print(f"{'':<{col_width}}", end="")
    for j in range(num_vars):
        print(f"{format_coefficient(zj_cj[j], M):>{col_width}}", end="")
    
    # Print profit/Z value
    profit = zj[-1]
    print(f"{'Z=' + format_coefficient(profit, M):>{col_width}}", end="")
    print(f"{'':>{col_width}}")
    
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

def setup_simplex_table(problem, var_prefix='x'):
    """
    Setup initial simplex tableau
    Adds slack variables for <= constraints
    var_prefix: 'x' for primal, 'w' for dual
    """
    num_vars = problem['num_vars']
    num_constraints = problem['num_constraints']
    constraints = problem['constraints']
    rhs = problem['rhs']
    obj_coef = problem['obj_coef']
    is_max = problem['is_max']
    
    # Variable names
    var_names = [f"{var_prefix}{i+1}" for i in range(num_vars)]
    
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

def setup_big_m_table(problem, M=10000, var_prefix='x'):
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

def solve_simplex(problem, var_prefix='x'):
    """Main function to solve using Simplex Method"""
    print("\n" + "#"*80)
    print("SOLVING USING SIMPLEX METHOD")
    print("#"*80)
    
    # Setup initial table
    table, basic_vars, var_names, cj, cb = setup_simplex_table(problem, var_prefix)
    
    iteration = 0
    optimal_value = None
    
    while True:
        # Calculate Zj and Zj-Cj to check optimality and find entering variable
        # (We need this before printing the table)
        num_vars = len(var_names)
        zj = calculate_zj(table, cb, num_vars)
        zj_cj = calculate_zj_cj(zj, cj, None)
        
        # Check optimality
        if check_optimality(zj_cj):
            # Print final table without ratios
            print(f"\n{'='*80}")
            print(f"ITERATION {iteration}")
            print('='*80)
            zj_final, zj_cj_final = print_simplex_table(table, basic_vars, var_names, cj, cb, iteration)
            solution = extract_solution(table, basic_vars, var_names, problem['is_max'])
            print_solution(solution, var_names, zj_final, problem['is_max'], problem['num_vars'])
            
            # Calculate optimal value
            optimal_value = zj_final[-1]
            if not problem['is_max']:
                optimal_value = -optimal_value
            break
        
        # Find pivot column
        pivot_col, min_zj_cj = find_pivot_column(zj_cj, var_names)
        
        if pivot_col == -1:
            print("\nOptimal solution reached!")
            break
        
        # Now print table WITH ratios for the entering variable
        zj, zj_cj = print_simplex_table(table, basic_vars, var_names, cj, cb, iteration, pivot_col=pivot_col)
        
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
    
    return optimal_value

def solve_big_m(problem, var_prefix='x'):
    """Main function to solve using Big M Method"""
    print("\n" + "#"*80)
    print("SOLVING USING BIG M METHOD")
    print("#"*80)
    
    M = 10000  # Big M value (symbolic)
    
    # Setup initial table
    table, basic_vars, var_names, cj, cb, M_val, artificial_count = setup_big_m_table(problem, M, var_prefix)
    
    # Track artificial variables for infeasibility check
    artificial_vars = [f"A{i+1}" for i in range(artificial_count)]
    
    print(f"\nNote: M is used as a large penalty value (M = {M})")
    print(f"Artificial variables added: {', '.join(artificial_vars)}")
    
    iteration = 0
    optimal_value = None
    
    while True:
        # Calculate Zj and Zj-Cj to check optimality and find entering variable
        # (We need this before printing the table)
        num_vars = len(var_names)
        zj = calculate_zj(table, cb, num_vars)
        zj_cj = calculate_zj_cj(zj, cj, M_val)
        
        # Check optimality
        if check_optimality(zj_cj):
            # Print final table without ratios
            print(f"\n{'='*80}")
            print(f"ITERATION {iteration}")
            print('='*80)
            zj_final, zj_cj_final = print_simplex_table(table, basic_vars, var_names, cj, cb, iteration, M_val)
            # Check infeasibility
            if check_infeasible(basic_vars, table, artificial_vars):
                print("\n" + "!"*80)
                print("INFEASIBLE SOLUTION!")
                print("Artificial variable(s) in the final basis with positive value.")
                print("The problem has no feasible solution.")
                print("!"*80)
                optimal_value = None
            else:
                solution = extract_solution(table, basic_vars, var_names, problem['is_max'])
                print_solution(solution, var_names, zj_final, problem['is_max'], problem['num_vars'])
                
                # Calculate optimal value
                optimal_value = zj_final[-1]
                if not problem['is_max']:
                    optimal_value = -optimal_value
            break
        
        # Find pivot column
        pivot_col, min_zj_cj = find_pivot_column(zj_cj, var_names)
        
        if pivot_col == -1:
            print("\nOptimal solution reached!")
            break
        
        # Now print table WITH ratios for the entering variable
        zj, zj_cj = print_simplex_table(table, basic_vars, var_names, cj, cb, iteration, M_val, pivot_col)
        
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
    
    return optimal_value

# ============================================================================
# DUAL SIMPLEX METHOD
# ============================================================================

def check_dual_feasibility(table):
    """
    Check if all RHS values are non-negative (primal feasibility)
    Returns: (is_feasible, most_negative_row_index, most_negative_value)
    """
    most_negative = 0
    negative_row = -1
    
    for i in range(len(table)):
        rhs = table[i][-1]
        if rhs < most_negative - 1e-9:
            most_negative = rhs
            negative_row = i
    
    is_feasible = (negative_row == -1)
    return is_feasible, negative_row, most_negative

def find_dual_pivot_column(table, pivot_row, zj_cj):
    """
    Find pivot column for dual simplex
    Rule: Among negative elements in pivot row, choose column with minimum |zj_cj/element|
    """
    min_ratio = float('inf')
    pivot_col = -1
    ratios = []
    
    num_cols = len(table[0]) - 1  # Exclude RHS
    
    for j in range(num_cols):
        element = table[pivot_row][j]
        if element < -1e-9:  # Negative element
            if abs(zj_cj[j]) < 1e-9:  # zj_cj is zero
                ratio = 0
            else:
                ratio = abs(zj_cj[j] / element)
            
            ratios.append((j, element, zj_cj[j], ratio))
            
            if ratio < min_ratio:
                min_ratio = ratio
                pivot_col = j
    
    return pivot_col, min_ratio, ratios

def solve_dual_simplex(problem, var_prefix='x'):
    """
    Solve using Dual Simplex Method
    
    Used when:
    - All Zj-Cj >= 0 (dual feasible / optimality condition satisfied)
    - But some RHS < 0 (primal infeasible)
    
    Common in problems with >= constraints after converting to standard form
    by multiplying constraints by -1
    """
    print("\n" + "#"*80)
    print("SOLVING USING DUAL SIMPLEX METHOD")
    print("#"*80)
    
    print("\n" + "="*80)
    print("DUAL SIMPLEX METHOD - EXPLANATION")
    print("="*80)
    print("\nWhen to use Dual Simplex:")
    print("  • Problem is in canonical form with optimal indicators (Zj-Cj >= 0)")
    print("  • But solution is infeasible (some RHS values < 0)")
    print("  • Common after converting >= constraints by multiplying by -1")
    print()
    print("Algorithm:")
    print("  1. Check if all RHS >= 0:")
    print("     - If YES: Optimal solution found")
    print("     - If NO: Select most negative RHS (leaving variable)")
    print("  2. From leaving row, find entering variable:")
    print("     - Consider only negative elements in the row")
    print("     - Choose minimum |Zj-Cj / element|")
    print("  3. Perform pivot operation")
    print("  4. Repeat until all RHS >= 0")
    print("="*80)
    
    input("\nPress Enter to start solving...")
    
    # Setup initial table (same as regular simplex for standard form)
    table, basic_vars, var_names, cj, cb = setup_simplex_table(problem, var_prefix)
    
    iteration = 0
    optimal_value = None
    
    while True:
        # Calculate Zj and Zj-Cj
        num_vars = len(var_names)
        zj = calculate_zj(table, cb, num_vars)
        zj_cj = calculate_zj_cj(zj, cj, None)
        
        # Check primal feasibility (all RHS >= 0)
        is_feasible, negative_row, most_negative = check_dual_feasibility(table)
        
        if is_feasible:
            # Optimal solution found
            print(f"\n{'='*80}")
            print(f"ITERATION {iteration}")
            print('='*80)
            zj_final, zj_cj_final = print_simplex_table(table, basic_vars, var_names, cj, cb, iteration)
            solution = extract_solution(table, basic_vars, var_names, problem['is_max'])
            print_solution(solution, var_names, zj_final, problem['is_max'], problem['num_vars'])
            
            # Calculate optimal value
            optimal_value = zj_final[-1]
            if not problem['is_max']:
                optimal_value = -optimal_value
            break
        
        # Print current table
        print(f"\n{'='*80}")
        print(f"ITERATION {iteration}")
        print('='*80)
        zj, zj_cj = print_simplex_table(table, basic_vars, var_names, cj, cb, iteration)
        
        # Leaving variable (most negative RHS)
        print(f"\nLeaving Variable: {basic_vars[negative_row]} (RHS = {print_fraction(most_negative)})")
        print(f"Leaving Row: {negative_row + 1}")
        
        # Find entering variable using dual simplex ratio test
        pivot_col, min_ratio, ratios = find_dual_pivot_column(table, negative_row, zj_cj)
        
        if pivot_col == -1:
            print("\n" + "!"*80)
            print("INFEASIBLE SOLUTION!")
            print("No entering variable found. Problem has no feasible solution.")
            print("!"*80)
            return None
        
        print("\nDual Simplex Ratio Test (Minimum |Zj-Cj / element|):")
        print("-" * 40)
        for j, element, zj_cj_val, ratio in ratios:
            print(f"  Column {var_names[j]}: |{print_fraction(zj_cj_val)} / {print_fraction(element)}| = {print_fraction(ratio)}")
        
        print(f"\nEntering Variable: {var_names[pivot_col]} (minimum ratio = {print_fraction(min_ratio)})")
        
        # Wait for user
        input("\n>>> Press Enter to perform pivot operation and see next iteration...")
        
        # Perform pivot operation (same as regular simplex)
        pivot_row = negative_row
        table, basic_vars, cb = perform_pivot_operation(table, pivot_row, pivot_col, basic_vars, var_names, cb, cj)
        
        iteration += 1
    
    return optimal_value

# ============================================================================
# PRIMAL TO DUAL CONVERSION & SHADOW PRICES
# ============================================================================

def convert_to_dual(problem):
    """
    Convert primal problem to dual (FULLY CORRECTED VERSION)
    
    Reference: Operations Research by Taha, 10th Edition
    
    ASYMMETRIC FORM OF DUALITY:
    
    Primal (Max):        Dual (Min):
    Max Z = cx           Min W = yb
    Ax <= b              A^T y >= c
    x >= 0               y >= 0 (or unrestricted based on primal constraints)
    
    Primal (Min):        Dual (Max):
    Min Z = cx           Max W = yb
    Ax >= b              A^T y <= c
    x >= 0               y >= 0
    
    SPECIAL CASE - Min with <= (convert via standard form):
    Min Z = cx           Equivalent to: Max Z' = -cx
    Ax <= b              becomes: Ax <= b
    x >= 0               x >= 0
    
    Then dual: Min W = yb, A^T y >= -c, y >= 0
    Or equivalently using y' = -y where y' >= 0:
    Max W = -yb, A^T y >= c, y >= 0
    
    KEY INSIGHT: For Min with <=, dual objective coefficients are NEGATIVE!
    """
    print("\n" + "#"*80)
    print("PRIMAL TO DUAL CONVERSION")
    print("#"*80)
    
    # Display conversion rules
    print("\nCONVERSION RULES:")
    print("-" * 80)
    
    # Determine constraint type for display
    if problem['is_max']:
        print("Primal (Maximization) -> Dual (Minimization)")
        print()
        print("Primal:                    Dual:")
        print("  Max Z = Sum(cj * xj)      Min W = Sum(bi * yi)")
        print("  Sum(aij * xj) <= bi       Sum(aij * yi) >= cj  (for each j)")
        print("  xj >= 0                    yi >= 0")
    else:
        if all(ct == 1 for ct in problem['constraint_types']):  # All <= constraints
            print("Primal (Minimization with <=) -> Dual (Maximization with <=)")
            print()
            print("Primal:                    Dual:")
            print("  Min Z = Sum(cj * xj)      Max W = Sum(-bi * yi)  NOTE: -bi !")
            print("  Sum(aij * xj) <= bi       Sum(aij * yi) <= cj  (for each j)")
            print("  xj >= 0                    yi >= 0")
            print()
            print("CRITICAL: For Min with <=, dual has:")
            print("  • Objective: -b (negative RHS)")
            print("  • Constraints: <= (same as primal)")
        else:  # >= constraints
            print("Primal (Minimization with >=) -> Dual (Maximization with <=)")
            print()
            print("Primal:                    Dual:")
            print("  Min Z = Sum(cj * xj)      Max W = Sum(bi * yi)")
            print("  Sum(aij * xj) >= bi       Sum(aij * yi) <= cj  (for each j)")
            print("  xj >= 0                    yi >= 0")
    
    print("\nKEY TRANSFORMATIONS:")
    print("  - Number of primal constraints = Number of dual variables")
    print("  - Number of primal variables = Number of dual constraints")
    print("  - Primal objective coefficients -> Dual RHS values")
    print("  - Primal RHS values -> Dual objective coefficients")
    if not problem['is_max'] and all(ct == 1 for ct in problem['constraint_types']):
        print("  - FOR MIN WITH <=: Dual obj = -b (negative!)")
    print("  - Constraint matrix A is transposed (rows <-> columns)")
    print("  - IMPORTANT: By Strong Duality Theorem, optimal values are equal!")
    print("-" * 80)
    
    input("\nPress Enter to see the dual problem...")
    
    # Create dual problem  
    # Based on Hillier & Lieberman "Introduction to Operations Research"
    #
    # Standard form duality:
    #   Primal: Min cx, Ax >= b, x >= 0
    #   Dual:   Max yb, yA <= c, y >= 0
    #
    # For Min with <=: first convert Ax <= b to -Ax >= -b
    # Then apply standard duality
    #
    dual = {}
    
    if not problem['is_max'] and all(ct == 1 for ct in problem['constraint_types']):
        # Special handling for Min with <=
        # Convert to standard form: Ax <= b becomes -Ax >= -b
        # Then dual of Min(-cx), -Ax >= -b is Max(-yb), yA <= c
        # Which simplifies to: Max yb with objective coef = -b (implemented below)
        dual['is_max'] = True
    elif not problem['is_max']:
        # Min with >= or mixed
        dual['is_max'] = True  # Min -> Max
    else:
        # Max -> Min
        dual['is_max'] = False
    
    dual['num_vars'] = problem['num_constraints']
    dual['num_constraints'] = problem['num_vars']
    
    # CRITICAL FIX: Dual objective coefficients
    # For Min with <=: dual objective = -b (NEGATIVE!)
    # For Min with >=: dual objective = +b
    # For Max with <=: dual objective = +b
    if not problem['is_max'] and all(ct == 1 for ct in problem['constraint_types']):
        # Min with <= constraints: negate RHS for dual objective
        dual['obj_coef'] = [-x for x in problem['rhs']]
    else:
        # All other cases: use RHS as-is
        dual['obj_coef'] = problem['rhs'].copy()
    
    # Dual constraints = Transpose of primal constraints
    # For Min with <=: use -A transpose (because we converted to >= form)
    dual['constraints'] = []
    negate_matrix = (not problem['is_max'] and all(ct == 1 for ct in problem['constraint_types']))
    
    for j in range(problem['num_vars']):
        dual_constraint = []
        for i in range(problem['num_constraints']):
            coef = problem['constraints'][i][j]
            if negate_matrix:
                coef = -coef  # Negate for Min with <= case
            dual_constraint.append(coef)
        dual['constraints'].append(dual_constraint)
    
    # Dual RHS = Primal objective coefficients (no change needed)
    dual['rhs'] = problem['obj_coef'].copy()
    
    # CORRECTED Dual constraint types
    # Reference: Winston "Operations Research: Applications and Algorithms"
    # 
    # For MINIMIZATION primal with <= constraints:
    #   Dual is MAXIMIZATION with <= constraints (NOT >=!)
    #   But dual variables are unrestricted in sign (or we use substitution)
    # 
    # Standard symmetric duality (easier to implement):
    #   Primal: Min cx, Ax >= b, x >= 0
    #   Dual: Max yb, yA <= c, y >= 0
    # 
    # For Min with <=, convert to >= by negating both sides:
    #   Ax <= b becomes -Ax >= -b
    # Then apply standard duality
    # 
    # SIMPLER: Use the fact that for Min with <=:
    #   Dual: Max (-b)^T y, A^T y <= c, y >= 0
    # Which matches our objective fix!
    
    if problem['is_max']:
        # Max with <=: Dual is Min with >=
        dual['constraint_types'] = [2] * dual['num_constraints']  # All >=
    else:
        # Min with <=: Dual is Max with <=  (CRITICAL FIX!)
        # Min with >=: Dual is Max with >=
        if all(ct == 1 for ct in problem['constraint_types']):  # All <=
            dual['constraint_types'] = [1] * dual['num_constraints']  # All <= (FIX!)
        elif all(ct == 2 for ct in problem['constraint_types']):  # All >=
            dual['constraint_types'] = [2] * dual['num_constraints']  # All >=
        else:
            # Mixed constraints - handle individually  
            dual['constraint_types'] = []
            for ct in problem['constraint_types']:
                if ct == 1:  # Primal <= becomes Dual <=
                    dual['constraint_types'].append(1)
                elif ct == 2:  # Primal >= becomes Dual >=
                    dual['constraint_types'].append(2)
                else:  # = stays =
                    dual['constraint_types'].append(3)
    
    # CRITICAL: For simplex method, normalize constraints with negative RHS
    # Multiply entire constraint by -1 if RHS < 0
    for i in range(dual['num_constraints']):
        if dual['rhs'][i] < 0:
            # Multiply by -1
            dual['rhs'][i] = -dual['rhs'][i]
            for j in range(len(dual['constraints'][i])):
                dual['constraints'][i][j] = -dual['constraints'][i][j]
            # Flip constraint type: <= becomes >=, >= becomes <=
            if dual['constraint_types'][i] == 1:
                dual['constraint_types'][i] = 2
            elif dual['constraint_types'][i] == 2:
                dual['constraint_types'][i] = 1
    
    return dual

def print_dual_problem(dual):
    """Print dual problem (using w variables to distinguish from primal)"""
    print("\n" + "="*80)
    print("DUAL PROBLEM")
    print("="*80)
    
    # Objective function
    obj_type = "Maximize" if dual['is_max'] else "Minimize"
    obj_terms = []
    for i, c in enumerate(dual['obj_coef']):
        if c >= 0:
            if i == 0:
                obj_terms.append(f"{print_fraction(c)}w{i+1}")
            else:
                obj_terms.append(f"+ {print_fraction(c)}w{i+1}")
        else:
            obj_terms.append(f"- {print_fraction(abs(c))}w{i+1}")
    
    print(f"\n{obj_type} W = {' '.join(obj_terms)}")
    
    # Constraints
    print("\nSubject to:")
    constraint_symbols = {1: '<=', 2: '>=', 3: '='}
    
    for i in range(dual['num_constraints']):
        terms = []
        for j, c in enumerate(dual['constraints'][i]):
            if c >= 0:
                if j == 0:
                    terms.append(f"{print_fraction(c)}w{j+1}")
                else:
                    terms.append(f"+ {print_fraction(c)}w{j+1}")
            else:
                terms.append(f"- {print_fraction(abs(c))}w{j+1}")
        
        symbol = constraint_symbols[dual['constraint_types'][i]]
        print(f"  {' '.join(terms)} {symbol} {print_fraction(dual['rhs'][i])}")
    
    print(f"\n  w1, w2, ... w{dual['num_vars']} >= 0")

def convert_to_dual_and_solve(problem):
    """Convert primal to dual and solve, showing shadow prices"""
    
    # Print primal problem
    print("\n" + "="*80)
    print("PRIMAL PROBLEM")
    print("="*80)
    print_problem_summary(problem)
    
    # Solve primal
    input("\nPress Enter to solve PRIMAL problem...")
    
    primal_result = None
    if any(ct in [2, 3] for ct in problem['constraint_types']):
        print("\nSolving primal using Big M Method...")
        primal_result = solve_big_m(problem)
    else:
        print("\nSolving primal using Simplex Method...")
        primal_result = solve_simplex(problem)
    
    # Convert to dual
    input("\n\nPress Enter to see DUAL conversion...")
    dual = convert_to_dual(problem)
    print_dual_problem(dual)
    
    # Solve dual
    input("\n\nPress Enter to solve DUAL problem...")
    dual_result = None
    if any(ct in [2, 3] for ct in dual['constraint_types']):
        dual_result = solve_big_m(dual, var_prefix='w')
    else:
        dual_result = solve_simplex(dual, var_prefix='w')
    
    # Show duality theorem verification
    print("\n" + "="*80)
    print("STRONG DUALITY THEOREM VERIFICATION")
    print("="*80)
    print("\nThe Strong Duality Theorem states:")
    print("  If primal and dual both have optimal solutions,")
    print("  then their optimal objective values are EQUAL.")
    print()
    print(f"Primal Optimal Value: {primal_result if primal_result is not None else 'N/A'}")
    print(f"Dual Optimal Value:   {dual_result if dual_result is not None else 'N/A'}")
    
    if primal_result is not None and dual_result is not None:
        if abs(primal_result - dual_result) < 1e-6:
            print("\n✓ VERIFICATION PASSED: Primal and Dual optimal values are equal!")
        else:
            print("\n✗ Warning: Values don't match. This might indicate:")
            print("  - Numerical errors in calculation")
            print("  - Incorrect problem formulation")
            print("  - Bug in the conversion or solver")
    
   

# ============================================================================
# MATRIX METHOD SIMPLEX
# ============================================================================

def solve_simplex_matrix_method(problem):
    """
    Solve using Matrix Method with detailed notation
    Shows: A, B, N, b, X, Cb, Cn, B_inverse, etc.
    """
    print("\n" + "#"*80)
    print("SIMPLEX METHOD - MATRIX NOTATION")
    print("#"*80)
    
    # Display formulas first
    print("\n" + "="*80)
    print("MATRIX METHOD FORMULAS & NOTATION")
    print("="*80)
    
    print("\nSTANDARD FORM: Max Z = CX subject to AX = b, X >= 0")
    print()
    print("NOTATION:")
    print("  A     = Coefficient matrix of all variables in constraints (m × n)")
    print("  b     = RHS vector (m × 1)")
    print("  C     = Objective function coefficient vector (1 × n)")
    print("  X     = Decision variable vector (n × 1)")
    print()
    print("PARTITIONED FORM:")
    print("  B     = Basis matrix (coefficients of basic variables) (m × m)")
    print("  N     = Non-basis matrix (coefficients of non-basic variables) (m × (n-m))")
    print("  Cb    = Objective coefficients of basic variables (1 × m)")
    print("  Cn    = Objective coefficients of non-basic variables (1 × (n-m))")
    print("  Xb    = Basic variable values (m × 1)")
    print("  Xn    = Non-basic variable values (n-m × 1) = 0")
    print()
    print("KEY FORMULAS:")
    print("  1. Xb = B^-1 × b             (Basic variable values)")
    print("  2. Zj - Cj = Cb × B^-1 × Aj - Cj  (Reduced costs)")
    print("  3. b_new = B^-1 × b          (Updated RHS)")
    print("  4. Optimality: All (Zj - Cj) >= 0 for maximization")
    print()
    print("TABLEAU STRUCTURE:")
    print("  +----+-------+----------------+-------+")
    print("  | Cb | Basis |  Variables     |  Xb   |")
    print("  +----+-------+----------------+-------+")
    print("  | Cb | B     | B^-1 × A       |B^-1×b |")
    print("  +----+-------+----------------+-------+")
    print("  |    | Zj    | Cb×B^-1×Aj     |Cb×Xb  |")
    print("  |    | Zj-Cj | Zj - Cj        |  Z    |")
    print("  +----+-------+----------------+-------+")
    print()
    print("WHERE:")
    print("  - Each row i shows: B^-1[i,:] × A (updated coefficients)")
    print("  - Xb column shows: B^-1 × b (current basic variable values)")
    print("  - Zj row shows: Cb^T × (B^-1 × A) for each column")
    print("  - Zj-Cj shows optimality indicators")
    print("="*80)
    
    input("\nPress Enter to start solving...")
    
    # Convert to standard form (all <= become = with slack variables)
    num_vars = problem['num_vars']
    num_constraints = problem['num_constraints']
    
    # Build A matrix and b vector
    A = []
    b = []
    
    for i in range(num_constraints):
        row = problem['constraints'][i].copy()
        # Add slack variable columns
        for j in range(num_constraints):
            if i == j:
                row.append(1.0)
            else:
                row.append(0.0)
        A.append(row)
        b.append(problem['rhs'][i])
    
    # C vector
    C = problem['obj_coef'].copy()
    C.extend([0.0] * num_constraints)  # Slack variables have 0 cost
    
    if not problem['is_max']:
        C = [-c for c in C]
    
    total_vars = num_vars + num_constraints
    var_names = [f"x{i+1}" for i in range(num_vars)] + [f"s{i+1}" for i in range(num_constraints)]
    
    # Initial basis: slack variables
    basic_indices = list(range(num_vars, total_vars))
    non_basic_indices = list(range(num_vars))
    
    iteration = 0
    
    while True:
        print("\n" + "="*80)
        print(f"ITERATION {iteration}")
        print("="*80)
        
        # Extract B and N matrices
        B = []
        for i in range(num_constraints):
            B_row = []
            for j in basic_indices:
                B_row.append(A[i][j])
            B.append(B_row)
        
        N = []
        for i in range(num_constraints):
            N_row = []
            for j in non_basic_indices:
                N_row.append(A[i][j])
            N.append(N_row)
        
        # Extract Cb and Cn
        Cb = [C[j] for j in basic_indices]
        Cn = [C[j] for j in non_basic_indices]
        
        # Calculate B_inverse
        B_inv = matrix_inverse(B)
        
        if B_inv is None:
            print("\nError: Basis matrix is singular. Cannot proceed.")
            break
        
        # Calculate Xb = B_inv × b
        Xb = matrix_vector_mult(B_inv, b)
        
        # ===================================================================
        # TABLEAU DISPLAY - SIMPLEX TABLE FORMAT
        # ===================================================================
        print("\n" + "-"*80)
        print("SIMPLEX TABLEAU (Matrix Method)")
        print("-"*80)
        
        # Print tableau header showing formula
        col_width = 10
        print("\nTableau Structure:")
        print(f"{'Cb':<{col_width}}{'Basis':<{col_width}}", end="")
        for var in var_names:
            print(f"{var:>{col_width}}", end="")
        print(f"{'Xb=B^-1b':>{col_width}}")
        
        print("-" * (col_width * (total_vars + 3)))
        
        # Print each row of tableau
        # Tableau row i = B_inv[i] × A (entire constraint matrix)
        for i in range(num_constraints):
            # Cb value for this row
            print(f"{print_fraction(Cb[i]):<{col_width}}", end="")
            # Basic variable name
            print(f"{var_names[basic_indices[i]]:<{col_width}}", end="")
            
            # Coefficients: B_inv × A gives updated constraint coefficients
            for j in range(total_vars):
                A_col_j = [A[row][j] for row in range(num_constraints)]
                coef = sum(B_inv[i][k] * A_col_j[k] for k in range(num_constraints))
                print(f"{print_fraction(coef):>{col_width}}", end="")
            
            # RHS = Xb
            print(f"{print_fraction(Xb[i]):>{col_width}}")
        
        print("-" * (col_width * (total_vars + 3)))
        
        # Zj row
        print(f"{'Zj':<{col_width}}{'':<{col_width}}", end="")
        Zj_row = []
        for j in range(total_vars):
            A_col_j = [A[row][j] for row in range(num_constraints)]
            Binv_Aj = matrix_vector_mult(B_inv, A_col_j)
            Zj = sum(Cb[k] * Binv_Aj[k] for k in range(num_constraints))
            Zj_row.append(Zj)
            print(f"{print_fraction(Zj):>{col_width}}", end="")
        
        Z_current = sum(Cb[i] * Xb[i] for i in range(num_constraints))
        print(f"{print_fraction(Z_current):>{col_width}}")
        
        # Zj-Cj row
        print(f"{'Zj-Cj':<{col_width}}{'':<{col_width}}", end="")
        ZjCj_row = []
        for j in range(total_vars):
            zjcj = Zj_row[j] - C[j]
            ZjCj_row.append(zjcj)
            print(f"{print_fraction(zjcj):>{col_width}}", end="")
        print()
        
        print("="*80)
        
        # ===================================================================
        # DETAILED MATRIX CALCULATIONS
        # ===================================================================
        
        # Display matrices
        print("\n" + "-"*80)
        print("DETAILED MATRIX CALCULATIONS")
        print("-"*80)
        
        print("\nCURRENT BASIS:")
        print(f"  Basic variables: {[var_names[j] for j in basic_indices]}")
        print(f"  Non-basic variables: {[var_names[j] for j in non_basic_indices]}")
        
        print("\nB (Basis Matrix):")
        print_matrix(B)
        
        print("\nB^-1 (Inverse of Basis Matrix):")
        print_matrix(B_inv)
        
        print("\nb (RHS vector):")
        print_vector(b)
        
        print("\nXb = B^-1 × b (Basic variable values):")
        print_vector(Xb)
        
        print("\nCb (Objective coefficients of basic variables):")
        print_vector(Cb)
        
        # Calculate Zj - Cj for non-basic variables
        print("\nREDUCED COSTS FOR NON-BASIC VARIABLES:")
        print("Formula: Zj - Cj = (Cb × B^-1 × Aj) - Cj")
        print()
        
        zj_cj = []
        for k, j in enumerate(non_basic_indices):
            # Get column j from A
            Aj = [A[i][j] for i in range(num_constraints)]
            # Binv × Aj
            Binv_Aj = matrix_vector_mult(B_inv, Aj)
            # Cb × (Binv × Aj)
            Cb_Binv_Aj = sum(Cb[i] * Binv_Aj[i] for i in range(num_constraints))
            # Zj - Cj
            reduced_cost = Cb_Binv_Aj - C[j]
            zj_cj.append(reduced_cost)
            print(f"  {var_names[j]}: Zj - Cj = {print_fraction(reduced_cost)}")
        
        # Check optimality based on Zj-Cj from ALL variables
        all_zj_cj = []
        for j in range(total_vars):
            Aj = [A[i][j] for i in range(num_constraints)]
            Binv_Aj = matrix_vector_mult(B_inv, Aj)
            Cb_Binv_Aj = sum(Cb[i] * Binv_Aj[i] for i in range(num_constraints))
            reduced_cost = Cb_Binv_Aj - C[j]
            all_zj_cj.append(reduced_cost)
        # Check optimality based on Zj-Cj from ALL variables
        all_zj_cj = []
        for j in range(total_vars):
            Aj = [A[i][j] for i in range(num_constraints)]
            Binv_Aj = matrix_vector_mult(B_inv, Aj)
            Cb_Binv_Aj = sum(Cb[i] * Binv_Aj[i] for i in range(num_constraints))
            reduced_cost = Cb_Binv_Aj - C[j]
            all_zj_cj.append(reduced_cost)
        
        # Check optimality
        if all(val >= -1e-9 for val in all_zj_cj):
            print("\n" + "="*80)
            print("OPTIMAL SOLUTION REACHED!")
            print("="*80)
            print("\nAll reduced costs (Zj - Cj) are non-negative.")
            print()
            print("Decision Variables:")
            solution = [0.0] * total_vars
            for i, j in enumerate(basic_indices):
                solution[j] = Xb[i]
            
            for i in range(num_vars):
                print(f"  x{i+1} = {print_fraction(solution[i])}")
            
            Z_value = sum(Cb[i] * Xb[i] for i in range(len(Cb)))
            if not problem['is_max']:
                Z_value = -Z_value
            
            print(f"\nOptimal Value of Z = {print_fraction(Z_value)}")
            break
        
        # Find entering variable (most negative Zj - Cj)
        min_val = min(all_zj_cj)
        entering_var_idx = all_zj_cj.index(min_val)
        
        # Find which list this variable is in
        if entering_var_idx in basic_indices:
            print(f"\nNote: Most negative is a basic variable (shouldn't happen in normal cases)")
        
        print(f"\nENTERING VARIABLE: {var_names[entering_var_idx]} (most negative Zj-Cj = {print_fraction(min_val)})")
        
        # Calculate direction vector d = B_inv × A_entering
        A_entering = [A[i][entering_var_idx] for i in range(num_constraints)]
        d = matrix_vector_mult(B_inv, A_entering)
        
        print("\nDIRECTION VECTOR (d = B^-1 × A_entering):")
        print_vector(d)
        
        # Minimum ratio test
        print("\nMINIMUM RATIO TEST:")
        print("Formula: theta = min{ Xb[i] / d[i] : d[i] > 0 }")
        print()
        
        min_ratio = float('inf')
        leaving_idx = -1
        
        for i in range(len(d)):
            if d[i] > 1e-9:
                ratio = Xb[i] / d[i]
                print(f"  Row {i+1} ({var_names[basic_indices[i]]}): {print_fraction(Xb[i])} / {print_fraction(d[i])} = {print_fraction(ratio)}")
                if ratio < min_ratio:
                    min_ratio = ratio
                    leaving_idx = i
            else:
                print(f"  Row {i+1} ({var_names[basic_indices[i]]}): d[{i+1}] <= 0, skip")
        
        if leaving_idx == -1:
            print("\nProblem is UNBOUNDED!")
            break
        
        leaving_var_idx = basic_indices[leaving_idx]
        print(f"\nLEAVING VARIABLE: {var_names[leaving_var_idx]} (minimum ratio = {print_fraction(min_ratio)})")
        
        # Update basis
        # Find where entering_var_idx is in non_basic_indices
        if entering_var_idx in non_basic_indices:
            entering_idx = non_basic_indices.index(entering_var_idx)
            basic_indices[leaving_idx] = entering_var_idx
            non_basic_indices[entering_idx] = leaving_var_idx
            non_basic_indices.sort()
        else:
            print("\nError: Entering variable is already basic!")
            break
        
        iteration += 1
        
        input("\n>>> Press Enter to continue to next iteration...")

def matrix_inverse(matrix):
    """Calculate matrix inverse using Gauss-Jordan elimination"""
    n = len(matrix)
    # Create augmented matrix [A | I]
    aug = []
    for i in range(n):
        row = matrix[i].copy()
        row.extend([1.0 if i == j else 0.0 for j in range(n)])
        aug.append(row)
    
    # Forward elimination
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(aug[k][i]) > abs(aug[max_row][i]):
                max_row = k
        aug[i], aug[max_row] = aug[max_row], aug[i]
        
        # Check for singular matrix
        if abs(aug[i][i]) < 1e-10:
            return None
        
        # Scale pivot row
        pivot = aug[i][i]
        for j in range(2 * n):
            aug[i][j] /= pivot
        
        # Eliminate column
        for k in range(n):
            if k != i:
                factor = aug[k][i]
                for j in range(2 * n):
                    aug[k][j] -= factor * aug[i][j]
    
    # Extract inverse from right half
    inv = []
    for i in range(n):
        inv.append(aug[i][n:])
    
    return inv

def matrix_vector_mult(matrix, vector):
    """Multiply matrix by vector"""
    result = []
    for row in matrix:
        val = sum(row[i] * vector[i] for i in range(len(vector)))
        result.append(val)
    return result

def matrix_transpose(matrix):
    """Transpose a matrix"""
    rows = len(matrix)
    cols = len(matrix[0])
    result = []
    for j in range(cols):
        row = []
        for i in range(rows):
            row.append(matrix[i][j])
        result.append(row)
    return result

def print_matrix(matrix):
    """Print matrix in formatted way"""
    print("  [", end="")
    for i, row in enumerate(matrix):
        if i > 0:
            print("   ", end="")
        print("[", end="")
        for j, val in enumerate(row):
            print(f"{print_fraction(val):>8}", end="")
            if j < len(row) - 1:
                print(",", end="")
        print("]", end="")
        if i < len(matrix) - 1:
            print()
        else:
            print("]")

def print_vector(vector):
    """Print vector in formatted way"""
    print("  [", end="")
    for i, val in enumerate(vector):
        print(f"{print_fraction(val):>8}", end="")
        if i < len(vector) - 1:
            print(",", end="")
    print("]")

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

def print_assignment_matrix(matrix, title="", selected=None, lines_h=None, lines_v=None):
    """
    Print assignment matrix with formatting
    selected: list of (row, col) tuples to mark
    lines_h: list of row indices with horizontal lines
    lines_v: list of col indices with vertical lines
    """
    if title:
        print("\n" + "="*80)
        print(title)
        print("="*80)
    
    n = len(matrix)
    m = len(matrix[0])
    col_width = 10
    row_label_width = 8
    
    # Print header with > markers for vertical lines
    print(f"\n{'':<{row_label_width}}", end="")
    for j in range(m):
        marker = ">" if lines_v and j in lines_v else " "
        print(f"{marker + 'C' + str(j+1):>{col_width}}", end="")
    print()
    print("-" * (row_label_width + col_width * m))
    
    # Print rows
    for i in range(n):
        # Mark if this row has a horizontal line
        marker = ">" if lines_h and i in lines_h else " "
        row_label = marker + "R" + str(i+1)
        print(f"{row_label:<{row_label_width}}", end="")
        
        for j in range(m):
            val = matrix[i][j]
            val_str = print_fraction(val)
            
            # Check if this cell is selected
            is_selected = selected and (i, j) in selected
            
            if is_selected:
                # Box selected zeros
                print(f"{'[' + val_str + ']':>{col_width}}", end="")
            else:
                print(f"{val_str:>{col_width}}", end="")
        print()
    print()
    
    # If lines are drawn and NOT optimal yet, show which zeros are covered by which lines
    if lines_h or lines_v:
        zeros = [(i, j) for i in range(n) for j in range(m) if abs(matrix[i][j]) < 1e-9]
        
        # Only show detailed coverage if we're not at optimal yet
        # (indicated by having fewer lines than matrix size OR if explicitly requested)
        show_coverage = (len(lines_h) + len(lines_v)) < n
        
        if zeros and show_coverage:
            print("Zeros covered by lines:")
            for i, j in sorted(zeros):
                coverage = []
                if lines_h and i in lines_h:
                    coverage.append(f"Horizontal line through Row {i+1}")
                if lines_v and j in lines_v:
                    coverage.append(f"Vertical line through Col {j+1}")
                if coverage:
                    print(f"  Zero at R{i+1}C{j+1} covered by: {', '.join(coverage)}")
            print()

def row_reduction(matrix):
    """Step 2: Subtract minimum of each row from all elements in that row"""
    print("\n" + "#"*80)
    print("STEP 2: ROW REDUCTION")
    print("#"*80)
    print("\nFor each row, subtract the minimum element from all elements in that row")
    
    n = len(matrix)
    m = len(matrix[0])
    reduced = [row[:] for row in matrix]
    
    for i in range(n):
        min_val = min(matrix[i])
        print(f"\nRow {i+1}: Minimum = {print_fraction(min_val)}")
        for j in range(m):
            reduced[i][j] = matrix[i][j] - min_val
        print(f"  After reduction: {[print_fraction(x) for x in reduced[i]]}")
    
    print_assignment_matrix(reduced, "Matrix after Row Reduction")
    return reduced

def column_reduction(matrix):
    """Step 3: Subtract minimum of each column from all elements in that column"""
    print("\n" + "#"*80)
    print("STEP 3: COLUMN REDUCTION")
    print("#"*80)
    print("\nFor each column, subtract the minimum element from all elements in that column")
    
    n = len(matrix)
    m = len(matrix[0])
    reduced = [row[:] for row in matrix]
    
    for j in range(m):
        col = [matrix[i][j] for i in range(n)]
        min_val = min(col)
        print(f"\nColumn {j+1}: Minimum = {print_fraction(min_val)}")
        for i in range(n):
            reduced[i][j] = matrix[i][j] - min_val
    
    print_assignment_matrix(reduced, "Matrix after Column Reduction")
    return reduced

def find_zeros(matrix):
    """Find all zero positions in matrix"""
    zeros = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if abs(matrix[i][j]) < 1e-9:
                zeros.append((i, j))
    return zeros

def count_zeros_in_row(matrix, row):
    """Count zeros in a specific row"""
    return sum(1 for j in range(len(matrix[0])) if abs(matrix[row][j]) < 1e-9)

def count_zeros_in_col(matrix, col):
    """Count zeros in a specific column"""
    return sum(1 for i in range(len(matrix)) if abs(matrix[i][col]) < 1e-9)

def draw_minimum_lines(matrix):
    """
    Step 4: Draw minimum number of lines to cover all zeros
    Traditional method:
    1. Find rows with unique zeros -> mark those columns (vertical lines)
    2. Find columns with unique zeros -> mark those rows (horizontal lines)
    3. Repeat until no more changes
    Returns: (lines_h, lines_v, num_lines)
    """
    print("\n" + "#"*80)
    print("STEP 4: DRAW MINIMUM LINES TO COVER ALL ZEROS")
    print("#"*80)
    print("\nStrategy: Mark rows/columns with unique zeros")
    
    n = len(matrix)
    m = len(matrix[0])
    
    lines_h = set()  # Horizontal lines (cut rows)
    lines_v = set()  # Vertical lines (cut columns)
    
    changed = True
    iteration = 0
    while changed:
        changed = False
        iteration += 1
        
        # Step 1: Find rows with unique zeros (excluding already marked columns)
        for i in range(n):
            if i in lines_h:  # Skip already marked rows
                continue
            
            # Count unmarked zeros in this row
            unmarked_zeros = [(i, j) for j in range(m) 
                            if abs(matrix[i][j]) < 1e-9 and j not in lines_v]
            
            if len(unmarked_zeros) == 1:
                # Unique zero found! Mark this column (vertical line)
                row, col = unmarked_zeros[0]
                lines_v.add(col)
                print(f"  Row {i+1} has unique zero at C{col+1} -> Draw vertical line through Col {col+1}")
                changed = True
        
        # Step 2: Find columns with unique zeros (excluding already marked rows)
        for j in range(m):
            if j in lines_v:  # Skip already marked columns
                continue
            
            # Count unmarked zeros in this column
            unmarked_zeros = [(i, j) for i in range(n) 
                            if abs(matrix[i][j]) < 1e-9 and i not in lines_h]
            
            if len(unmarked_zeros) == 1:
                # Unique zero found! Mark this row (horizontal line)
                row, col = unmarked_zeros[0]
                lines_h.add(row)
                print(f"  Col {j+1} has unique zero at R{row+1} -> Draw horizontal line through Row {row+1}")
                changed = True
    
    # After unique zeros are handled, cover remaining zeros with greedy approach
    # Count uncovered zeros
    uncovered_zeros = [(i, j) for i in range(n) for j in range(m)
                       if abs(matrix[i][j]) < 1e-9 and i not in lines_h and j not in lines_v]
    
    if uncovered_zeros:
        print(f"\n  {len(uncovered_zeros)} uncovered zeros remaining. Using greedy approach...")
        # Greedy: cover rows/columns with most uncovered zeros
        while uncovered_zeros:
            # Count zeros per row and column
            row_counts = {}
            col_counts = {}
            for i, j in uncovered_zeros:
                row_counts[i] = row_counts.get(i, 0) + 1
                col_counts[j] = col_counts.get(j, 0) + 1
            
            # Find best row or column to cover
            best_row = max(row_counts.items(), key=lambda x: x[1], default=(None, 0))
            best_col = max(col_counts.items(), key=lambda x: x[1], default=(None, 0))
            
            if best_row[1] >= best_col[1] and best_row[0] is not None:
                lines_h.add(best_row[0])
                print(f"  Draw horizontal line through Row {best_row[0]+1} (covers {best_row[1]} zeros)")
            elif best_col[0] is not None:
                lines_v.add(best_col[0])
                print(f"  Draw vertical line through Col {best_col[0]+1} (covers {best_col[1]} zeros)")
            
            # Recalculate uncovered zeros
            uncovered_zeros = [(i, j) for i in range(n) for j in range(m)
                             if abs(matrix[i][j]) < 1e-9 and i not in lines_h and j not in lines_v]
    
    lines_h = list(lines_h)
    lines_v = list(lines_v)
    num_lines = len(lines_h) + len(lines_v)
    
    print(f"\nTotal lines drawn: {num_lines}")
    print(f"Horizontal lines (rows): {[r+1 for r in lines_h]}")
    print(f"Vertical lines (columns): {[c+1 for c in lines_v]}")
    
    print_assignment_matrix(matrix, "Matrix with Lines Drawn", lines_h=lines_h, lines_v=lines_v)
    
    return lines_h, lines_v, num_lines

def create_additional_zeros(matrix, lines_h, lines_v):
    """
    Step 5: Create additional zeros
    1. Find smallest uncovered element
    2. Subtract from all uncovered elements
    3. Add to elements at line intersections
    """
    print("\n" + "#"*80)
    print("STEP 5: CREATE ADDITIONAL ZEROS")
    print("#"*80)
    
    n = len(matrix)
    m = len(matrix[0])
    
    # Find smallest uncovered element
    min_uncovered = float('inf')
    uncovered_count = 0
    for i in range(n):
        for j in range(m):
            if i not in lines_h and j not in lines_v:
                uncovered_count += 1
                if matrix[i][j] < min_uncovered:
                    min_uncovered = matrix[i][j]
    
    if uncovered_count == 0 or min_uncovered == float('inf'):
        print("\nERROR: All elements are covered by lines!")
        print("This shouldn't happen. Returning matrix unchanged.")
        return matrix
    
    print(f"\nSmallest uncovered element: {print_fraction(min_uncovered)}")
    print("\nOperations:")
    print(f"  - Subtract {print_fraction(min_uncovered)} from all uncovered elements")
    print(f"  - Add {print_fraction(min_uncovered)} to elements at line intersections")
    print(f"  - Elements covered by one line remain unchanged")
    
    # Create new matrix
    new_matrix = [row[:] for row in matrix]
    
    for i in range(n):
        for j in range(m):
            in_h = i in lines_h
            in_v = j in lines_v
            
            if not in_h and not in_v:
                # Uncovered: subtract min_uncovered
                new_matrix[i][j] = matrix[i][j] - min_uncovered
            elif in_h and in_v:
                # Intersection: add min_uncovered
                new_matrix[i][j] = matrix[i][j] + min_uncovered
            # else: covered by one line, unchanged
    
    print_assignment_matrix(new_matrix, "Matrix after Creating Additional Zeros")
    
    return new_matrix

def make_assignment(matrix, original_matrix):
    """
    Step 6: Make optimal assignment
    Try to assign one zero per row and column using recursive backtracking
    """
    print("\n" + "#"*80)
    print("STEP 6: MAKE OPTIMAL ASSIGNMENT")
    print("#"*80)
    print("\nAssign one zero per row and column")
    print("Strategy: Use backtracking to find complete assignment")
    
    n = len(matrix)
    m = len(matrix[0])
    
    # Find all zeros positions
    zeros = {}
    for i in range(n):
        zeros[i] = [j for j in range(m) if abs(matrix[i][j]) < 1e-9]
    
    # Use backtracking to find a complete assignment
    best_assignment = []
    best_count = 0
    
    def backtrack(row, current_assignment, used_cols):
        """Recursively assign rows"""
        nonlocal best_assignment, best_count
        
        if row == n:
            if len(current_assignment) > best_count:
                best_count = len(current_assignment)
                best_assignment = current_assignment[:]
            return len(current_assignment) == n
        
        # Try assigning a zero to this row
        for col in zeros[row]:
            if col not in used_cols:
                current_assignment.append((row, col))
                used_cols.add(col)
                
                if backtrack(row + 1, current_assignment, used_cols):
                    return True
                
                # Backtrack
                current_assignment.pop()
                used_cols.remove(col)
        
        # Try skipping this row (if no valid assignment found)
        if backtrack(row + 1, current_assignment, used_cols):
            return True
        
        return False
    
    # Find assignment
    success = backtrack(0, [], set())
    assignment = {i: j for i, j in best_assignment}
    
    # Print assignments
    assigned = best_assignment
    for i, j in sorted(assigned):
        print(f"  Assign: R{i+1} -> C{j+1}")
    
    # Check for unassigned rows
    assigned_rows = {i for i, j in assigned}
    for i in range(n):
        if i not in assigned_rows:
            print(f"  ERROR: R{i+1} could not be assigned!")
    
    if not success or len(assigned) < n:
        print(f"\n[!] WARNING: Could only assign {len(assigned)} out of {n} rows!")
        print("The matrix may need more iterations (Steps 4-5) to create enough zeros.")
    
    print_assignment_matrix(matrix, "Final Assignment", selected=assigned)
    
    # Calculate total cost
    total_cost = sum(original_matrix[i][j] for i, j in assigned)
    
    print("\n" + "="*80)
    print("STEP 7: CALCULATE TOTAL COST")
    print("="*80)
    print("\nUsing original cost matrix:")
    for i, j in sorted(assigned):
        print(f"  R{i+1} -> C{j+1}: Cost = {print_fraction(original_matrix[i][j])}")
    
    print(f"\nTotal Cost = {print_fraction(total_cost)}")
    
    return assigned, total_cost

def parse_hungarian_problem(filename='problem.txt'):
    """Parse Hungarian assignment problem from file
    
    Format:
        Line 1: 'min' or 'max'
        Next lines: comma-separated cost values (one row per line)
    
    Example:
        min
        9,2,7,5
        6,8,3,1
        5,4,8,2
    """
    try:
        # Try utf-8-sig first (handles BOM), fallback to utf-8, then system default
        for encoding in ['utf-8-sig', 'utf-8', None]:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    lines = [line.strip() for line in f.readlines() if line.strip()]
                break
            except (UnicodeDecodeError, LookupError):
                continue
        else:
            print(f"Error: Could not decode file {filename}")
            return None
        
        if not lines:
            print(f"Error: File {filename} is empty")
            return None
        
        # Parse problem type (strip any whitespace and BOM characters)
        problem_type = lines[0].strip().replace('\ufeff', '').replace('\ufffe', '').lower()
        if problem_type not in ['min', 'max']:
            print(f"Error: First line must be 'min' or 'max', found '{lines[0]}'")
            return None
        
        is_max = (problem_type == 'max')
        
        # Parse matrix
        matrix = []
        for i, line in enumerate(lines[1:], start=2):
            try:
                row = [float(x.strip()) for x in line.split(',')]
                if not row:
                    continue
                matrix.append(row)
            except ValueError as e:
                print(f"Error parsing line {i}: {line}")
                print(f"  {e}")
                return None
        
        if not matrix:
            print("Error: No cost matrix found in file")
            return None
        
        # Verify all rows have same length
        row_lengths = [len(row) for row in matrix]
        if len(set(row_lengths)) > 1:
            print(f"Error: Inconsistent row lengths: {row_lengths}")
            return None
        
        return {
            'is_max': is_max,
            'matrix': matrix,
            'n': len(matrix),
            'm': len(matrix[0])
        }
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def solve_hungarian_method():
    """Main function for Hungarian Method"""
    print("\n" + "="*80)
    print("ASSIGNMENT PROBLEM - HUNGARIAN METHOD")
    print("="*80)
    
    # Ask for input method
    print("\n1. Manual Input")
    print("2. Load from File (problem.txt)")
    input_choice = get_int_input("Enter choice (1-2): ")
    
    if input_choice == 2:
        # Load from file
        print("\nLoading problem from 'problem.txt'...")
        problem_data = parse_hungarian_problem()
        if not problem_data:
            return
        
        print("Problem loaded successfully!")
        is_max = problem_data['is_max']
        matrix = problem_data['matrix']
        n = problem_data['n']
        m = problem_data['m']
    else:
        # Manual input
        # Ask if MAX or MIN
        print("\n1. Minimization Problem")
        print("2. Maximization Problem")
        problem_type = get_int_input("Enter choice (1-2): ")
        
        is_max = (problem_type == 2)
        
        # Input matrix
        n = get_int_input("\nEnter number of rows (workers/machines): ")
        m = get_int_input("Enter number of columns (jobs/tasks): ")
        
        print(f"\nEnter the cost matrix ({n}x{m}):")
        matrix = []
        for i in range(n):
            print(f"Row {i+1}:")
            row = []
            for j in range(m):
                val = get_float_input(f"  Element [{i+1},{j+1}]: ")
                row.append(val)
            matrix.append(row)
    
    # Store original matrix
    original_matrix = [row[:] for row in matrix]
    
    print_assignment_matrix(original_matrix, "Original Cost Matrix")
    
    # Step 1: Balance the matrix
    print("\n" + "#"*80)
    print("STEP 1: BALANCE THE MATRIX")
    print("#"*80)
    
    if n < m:
        print(f"\nAdding {m - n} dummy row(s) with cost 0")
        for _ in range(m - n):
            matrix.append([0.0] * m)
        n = m
    elif m < n:
        print(f"\nAdding {n - m} dummy column(s) with cost 0")
        for i in range(n):
            matrix[i].extend([0.0] * (n - m))
        m = n
    else:
        print("\nMatrix is already balanced (square matrix)")
    
    if n != len(original_matrix) or m != len(original_matrix[0]):
        # Extend original matrix for cost calculation
        original_ext = [row[:] for row in original_matrix]
        for i in range(len(original_ext)):
            original_ext[i].extend([0.0] * (n - len(original_matrix[0])))
        for _ in range(n - len(original_matrix)):
            original_ext.append([0.0] * n)
        original_matrix = original_ext
        print_assignment_matrix(matrix, "Balanced Matrix")
    
    # For MAX problem: convert to MIN
    if is_max:
        print("\n" + "#"*80)
        print("CONVERTING MAXIMIZATION TO MINIMIZATION")
        print("#"*80)
        print("\nMethod: New Cost = (Maximum element) - (Original element)")
        
        max_element = max(max(row) for row in matrix)
        print(f"\nMaximum element in matrix: {print_fraction(max_element)}")
        
        for i in range(n):
            for j in range(n):
                matrix[i][j] = max_element - matrix[i][j]
        
        print_assignment_matrix(matrix, "Converted Matrix (for MIN problem)")
    
    # Main Hungarian algorithm
    iteration = 0
    
    # Step 2: Row reduction
    matrix = row_reduction(matrix)
    
    # Step 3: Column reduction
    matrix = column_reduction(matrix)
    
    # Step 4-6: Iterate until optimal
    max_iterations = 20  # Safety limit
    while iteration < max_iterations:
        iteration += 1
        print("\n" + "="*80)
        print(f"ITERATION {iteration}")
        print("="*80)
        
        # Step 4: Draw lines
        lines_h, lines_v, num_lines = draw_minimum_lines(matrix)
        
        # Check if we have enough lines
        if num_lines >= n:
            # Verify that a complete assignment is possible
            # Try to find n independent zeros
            zeros = {}
            for i in range(n):
                zeros[i] = [j for j in range(n) if abs(matrix[i][j]) < 1e-9]
            
            # Quick check: does every row have at least one zero?
            if all(len(zeros[i]) > 0 for i in range(n)):
                # Try to find complete assignment with backtracking
                def can_assign(row, used_cols):
                    if row == n:
                        return True
                    for col in zeros[row]:
                        if col not in used_cols:
                            used_cols.add(col)
                            if can_assign(row + 1, used_cols):
                                return True
                            used_cols.remove(col)
                    return False
                
                if can_assign(0, set()):
                    print("\n" + "="*80)
                    print(f"OPTIMAL! Number of lines ({num_lines}) >= Matrix size ({n})")
                    print("And complete assignment is possible!")
                    print("="*80)
                    break
                else:
                    print(f"\nLines ({num_lines}) >= Matrix size, but complete assignment not possible yet.")
                    print("Need to create more zeros...")
            else:
                print(f"\nLines ({num_lines}) >= Matrix size, but some rows have no zeros.")
                print("Need to create more zeros...")
        else:
            print(f"\nNot optimal yet. Lines ({num_lines}) < Matrix size ({n})")
            print("Need to create more zeros...")
        
        # Step 5: Create additional zeros
        matrix = create_additional_zeros(matrix, lines_h, lines_v)
    
    if iteration >= max_iterations:
        print(f"\n[!] WARNING: Reached maximum iterations ({max_iterations})")
        print("Proceeding with best available assignment...")
    
    # Step 6-7: Make assignment and calculate cost
    input("\nPress Enter to make optimal assignment...")
    assigned, total_cost = make_assignment(matrix, original_matrix)
    
    return assigned, total_cost

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
        print("3. Dual Simplex Method (Manual Input)")
        print("4. Auto-Detect Method (Manual Input)")
        print("5. Load from File (problem.txt)")
        print("6. Primal to Dual Conversion")
        print("7. Simplex with Matrix Method")
        print("8. Assignment Problem (Hungarian Method)")
        print("9. Exit")
        print("-"*40)
        
        choice = get_int_input("Enter your choice (1-9): ")
        
        if choice == 9:
            print("\nThank you for using OR Exam Helper. Good luck!")
            break
        
        if choice not in [1, 2, 3, 4, 5, 6, 7, 8]:
            print("Invalid choice. Please try again.")
            continue
        
        # Handle Assignment Problem
        if choice == 8:
            solve_hungarian_method()
            
            another = input("\n\nDo you want to solve another problem? (y/n): ").lower()
            if another != 'y':
                print("\nThank you for using OR Exam Helper. Good luck!")
                break
            continue
        
        # Handle Dual Simplex Method
        if choice == 3:
            print("\n" + "="*80)
            print("DUAL SIMPLEX METHOD")
            print("="*80)
            print("\n1. Manual Input")
            print("2. Load from File (problem.txt)")
            ds_choice = get_int_input("Enter choice (1-2): ")
            
            if ds_choice == 1:
                problem = input_problem()
            elif ds_choice == 2:
                print("\nLoading problem from 'problem.txt'...")
                problem = read_problem_from_file('problem.txt')
                if problem is None:
                    print("Failed to load problem from file.")
                    continue
                print("Problem loaded successfully!")
            else:
                print("Invalid choice.")
                continue
            
            print_problem_summary(problem)
            
            print("\n⚠ NOTE: Dual Simplex is used when:")
            print("  • All Zj-Cj >= 0 (optimal indicators)")
            print("  • But some RHS < 0 (infeasible solution)")
            print("  • Common with >= constraints converted to standard form")
            
            confirm = input("\nContinue with Dual Simplex? (y/n): ").lower()
            if confirm != 'y':
                continue
            
            solve_dual_simplex(problem)
            
            another = input("\n\nDo you want to solve another problem? (y/n): ").lower()
            if another != 'y':
                print("\nThank you for using OR Exam Helper. Good luck!")
                break
            continue
        
        # Handle Primal to Dual
        if choice == 6:
            print("\n" + "="*80)
            print("PRIMAL TO DUAL CONVERSION")
            print("="*80)
            print("\n1. Manual Input")
            print("2. Load from File (problem.txt)")
            dual_choice = get_int_input("Enter choice (1-2): ")
            
            if dual_choice == 1:
                problem = input_problem()
            elif dual_choice == 2:
                print("\nLoading problem from 'problem.txt'...")
                problem = read_problem_from_file('problem.txt')
                if problem is None:
                    print("Failed to load problem from file.")
                    continue
                print("Problem loaded successfully!")
            else:
                print("Invalid choice.")
                continue
            
            print_problem_summary(problem)
            input("\nPress Enter to convert to dual and solve...")
            convert_to_dual_and_solve(problem)
            
            another = input("\n\nDo you want to solve another problem? (y/n): ").lower()
            if another != 'y':
                print("\nThank you for using OR Exam Helper. Good luck!")
                break
            continue
        
        # Handle Matrix Method
        if choice == 7:
            print("\n" + "="*80)
            print("SIMPLEX WITH MATRIX METHOD")
            print("="*80)
            print("\n1. Manual Input")
            print("2. Load from File (problem.txt)")
            matrix_choice = get_int_input("Enter choice (1-2): ")
            
            if matrix_choice == 1:
                problem = input_problem()
            elif matrix_choice == 2:
                print("\nLoading problem from 'problem.txt'...")
                problem = read_problem_from_file('problem.txt')
                if problem is None:
                    print("Failed to load problem from file.")
                    continue
                print("Problem loaded successfully!")
            else:
                print("Invalid choice.")
                continue
            
            print_problem_summary(problem)
            
            # Check if suitable for matrix method
            if any(ct != 1 for ct in problem['constraint_types']):
                print("\n⚠ NOTE: Matrix method works best with standard form (all <= constraints).")
                print("The problem will be converted to standard form automatically.")
            
            input("\nPress Enter to solve using Matrix Method...")
            solve_simplex_matrix_method(problem)
            
            another = input("\n\nDo you want to solve another problem? (y/n): ").lower()
            if another != 'y':
                print("\nThank you for using OR Exam Helper. Good luck!")
                break
            continue
        
        # Input the problem
        if choice == 5:
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
        
        if choice != 5:  # Skip confirmation for file input
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
        
        elif choice in [4, 5]:
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
