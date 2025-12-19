

def clear_screen ():

    print ("\n"+"="*80 +"\n")

def print_fraction (num ,precision =4 ):

    if abs (num -round (num ))<1e-9 :
        return str (int (round (num )))
    return f"{num :.{precision }f}".rstrip ('0').rstrip ('.')

def get_float_input (prompt ):

    while True :
        try :
            return float (input (prompt ))
        except ValueError :
            print ("Invalid input. Please enter a number.")

def get_int_input (prompt ):

    while True :
        try :
            return int (input (prompt ))
        except ValueError :
            print ("Invalid input. Please enter an integer.")

def print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration ,M =None ,pivot_col =None ):

    print (f"\n{'='*80 }")
    print (f"ITERATION {iteration }")
    print ('='*80 )

    num_vars =len (var_names )
    col_width =10 

    ratios =[]
    if pivot_col is not None :
        for i in range (len (table )):
            element =table [i ][pivot_col ]
            rhs =table [i ][-1 ]
            if element >1e-9 :
                ratio =rhs /element 
                ratios .append (ratio )
            else :
                ratios .append (None )
    else :
        ratios =[None ]*len (table )

    print (f"{'Cj':<{col_width }}",end ="")
    print (f"{'':<{col_width }}",end ="")
    for j in range (num_vars ):
        cj_val =format_coefficient (cj [j ],M )
        print (f"{cj_val :>{col_width }}",end ="")
    print (f"{'Xb':>{col_width }}",end ="")
    if pivot_col is not None :
        print (f"{'Ratio':>{col_width }}")
        separator_length =col_width *(num_vars +4 )
    else :
        print ()
        separator_length =col_width *(num_vars +3 )

    print ("-"*separator_length )

    print (f"{'Cb':<{col_width }}",end ="")
    print (f"{'B':<{col_width }}",end ="")
    for name in var_names :
        print (f"{name :>{col_width }}",end ="")
    print (f"{'(RHS)':>{col_width }}",end ="")
    if pivot_col is not None :
        print (f"{'':>{col_width }}")
    else :
        print ()

    print ("-"*separator_length )

    num_constraints =len (table )
    for i in range (num_constraints ):
        cb_val =format_coefficient (cb [i ],M )
        basic_var =basic_vars [i ]

        row_str =f"{cb_val :<{col_width }}{basic_var :<{col_width }}"
        for j in range (num_vars ):
            val =print_fraction (table [i ][j ])
            row_str +=f"{val :>{col_width }}"
        rhs_val =print_fraction (table [i ][-1 ])
        row_str +=f"{rhs_val :>{col_width }}"

        if pivot_col is not None :
            if ratios [i ]is not None :
                ratio_str =print_fraction (ratios [i ])
                row_str +=f"{ratio_str :>{col_width }}"
            else :
                row_str +=f"{'-':>{col_width }}"

        print (row_str )

    print ("-"*separator_length )

    zj =calculate_zj (table ,cb ,num_vars )
    print (f"{'Zj':<{col_width }}",end ="")
    print (f"{'':<{col_width }}",end ="")
    for j in range (num_vars ):
        print (f"{format_coefficient (zj [j ],M ):>{col_width }}",end ="")
    print (f"{format_coefficient (zj [-1 ],M ):>{col_width }}",end ="")
    print (f"{'':>{col_width }}")

    zj_cj =calculate_zj_cj (zj ,cj ,M )
    print (f"{'Zj-Cj':<{col_width }}",end ="")
    print (f"{'':<{col_width }}",end ="")
    for j in range (num_vars ):
        print (f"{format_coefficient (zj_cj [j ],M ):>{col_width }}",end ="")

    profit =zj [-1 ]
    print (f"{'Z='+format_coefficient (profit ,M ):>{col_width }}",end ="")
    print (f"{'':>{col_width }}")

    print ('='*80 )

    return zj ,zj_cj 

def format_coefficient (val ,M =None ):

    if M is None :
        return print_fraction (val )

    if isinstance (val ,tuple ):
        const ,m_coef =val 
        if abs (m_coef )<1e-9 :
            return print_fraction (const )
        elif abs (const )<1e-9 :
            if abs (m_coef -1 )<1e-9 :
                return "M"
            elif abs (m_coef +1 )<1e-9 :
                return "-M"
            else :
                return f"{print_fraction (m_coef )}M"
        else :
            sign ="+"if m_coef >0 else ""
            if abs (m_coef -1 )<1e-9 :
                return f"{print_fraction (const )}{sign }M"
            elif abs (m_coef +1 )<1e-9 :
                return f"{print_fraction (const )}-M"
            else :
                return f"{print_fraction (const )}{sign }{print_fraction (m_coef )}M"
    return print_fraction (val )

def calculate_zj (table ,cb ,num_vars ):

    num_constraints =len (table )
    zj =[]

    for j in range (num_vars +1 ):
        col_idx =j if j <num_vars else -1 
        zj_val =sum (cb [i ]*table [i ][col_idx ]for i in range (num_constraints ))
        zj .append (zj_val )

    return zj 

def calculate_zj_cj (zj ,cj ,M =None ):

    zj_cj =[]
    for j in range (len (cj )):
        zj_cj .append (zj [j ]-cj [j ])
    return zj_cj 

def parse_expression (expr ):

    import re 

    expr =expr .replace (' ','')

    coef_dict ={}

    pattern =r'([+-]?)(\d*\.?\d*)([x]\d+)'

    matches =re .findall (pattern ,expr )

    for sign ,coef ,var in matches :
        if coef =='':
            coef_val =1.0 
        else :
            coef_val =float (coef )

        if sign =='-':
            coef_val =-coef_val 

        coef_dict [var ]=coef_val 

    return coef_dict 

def parse_constraint (line ):

    line =line .strip ()

    if '<='in line :
        constraint_type =1 
        parts =line .split ('<=')
    elif '>='in line :
        constraint_type =2 
        parts =line .split ('>=')
    elif '='in line :
        constraint_type =3 
        parts =line .split ('=')
    else :
        raise ValueError (f"Invalid constraint: {line }")

    if len (parts )!=2 :
        raise ValueError (f"Invalid constraint format: {line }")

    lhs =parts [0 ].strip ()
    rhs =float (parts [1 ].strip ())

    coef_dict =parse_expression (lhs )

    return coef_dict ,constraint_type ,rhs 

def read_problem_from_file (filename ='problem.txt'):

    try :
        with open (filename ,'r',encoding ='utf-8-sig')as f :
            raw_lines =f .readlines ()

        if raw_lines :
            raw_lines [0 ]=raw_lines [0 ].lstrip ('\ufeff').lstrip ('\ufffe')

        lines =[line .strip ()for line in raw_lines if line .strip ()]

        if len (lines )<3 :
            print ("Error: File must have at least 3 lines (objective type, objective function, and at least one constraint)")
            return None 

        obj_type =lines [0 ].lower ()
        if obj_type not in ['max','min','maximize','minimize']:
            print (f"Error: First line must be 'max' or 'min', got '{lines [0 ]}'")
            return None 
        is_max =obj_type in ['max','maximize']

        obj_line =lines [1 ]
        if 'z='in obj_line .lower ():
            obj_line =obj_line .lower ().split ('z=')[1 ]
        elif 'z ='in obj_line .lower ():
            obj_line =obj_line .lower ().split ('z =')[1 ]

        obj_coef_dict =parse_expression (obj_line )

        constraints_data =[]
        for i in range (2 ,len (lines )):
            coef_dict ,constraint_type ,rhs =parse_constraint (lines [i ])
            constraints_data .append ((coef_dict ,constraint_type ,rhs ))

        all_vars =set ()
        all_vars .update (obj_coef_dict .keys ())
        for coef_dict ,_ ,_ in constraints_data :
            all_vars .update (coef_dict .keys ())

        var_list =sorted (all_vars ,key =lambda x :int (x [1 :]))
        num_vars =len (var_list )
        num_constraints =len (constraints_data )

        obj_coef =[]
        for var in var_list :
            obj_coef .append (obj_coef_dict .get (var ,0.0 ))

        constraints =[]
        constraint_types =[]
        rhs =[]

        for coef_dict ,constraint_type ,rhs_val in constraints_data :
            constraint_row =[]
            for var in var_list :
                constraint_row .append (coef_dict .get (var ,0.0 ))
            constraints .append (constraint_row )
            constraint_types .append (constraint_type )
            rhs .append (rhs_val )

        problem ={
        'is_max':is_max ,
        'num_vars':num_vars ,
        'num_constraints':num_constraints ,
        'obj_coef':obj_coef ,
        'constraints':constraints ,
        'constraint_types':constraint_types ,
        'rhs':rhs 
        }

        return problem 

    except FileNotFoundError :
        print (f"Error: File '{filename }' not found.")
        return None 
    except Exception as e :
        print (f"Error reading file: {e }")
        return None 

def input_problem ():

    print ("\n"+"="*80 )
    print ("PROBLEM INPUT")
    print ("="*80 )

    print ("\nProblem Type:")
    print ("1. Maximization")
    print ("2. Minimization")
    prob_type =get_int_input ("Enter choice (1/2): ")
    is_max =(prob_type ==1 )

    num_vars =get_int_input ("\nEnter number of decision variables (x1, x2, ...): ")
    num_constraints =get_int_input ("Enter number of constraints: ")

    print (f"\nEnter coefficients of objective function Z:")
    print (f"Z = c1*x1 + c2*x2 + ... + c{num_vars }*x{num_vars }")
    obj_coef =[]
    for i in range (num_vars ):
        coef =get_float_input (f"  c{i +1 } (coefficient of x{i +1 }): ")
        obj_coef .append (coef )

    print (f"\nEnter constraints (assume all xi >= 0):")
    print ("Constraint types: 1 for <=, 2 for >=, 3 for =")

    constraints =[]
    constraint_types =[]
    rhs =[]

    for i in range (num_constraints ):
        print (f"\nConstraint {i +1 }:")
        coefs =[]
        for j in range (num_vars ):
            coef =get_float_input (f"  Coefficient of x{j +1 }: ")
            coefs .append (coef )

        con_type =get_int_input ("  Constraint type (1: <=, 2: >=, 3: =): ")
        rhs_val =get_float_input ("  RHS value: ")

        constraints .append (coefs )
        constraint_types .append (con_type )
        rhs .append (rhs_val )

    return {
    'is_max':is_max ,
    'num_vars':num_vars ,
    'num_constraints':num_constraints ,
    'obj_coef':obj_coef ,
    'constraints':constraints ,
    'constraint_types':constraint_types ,
    'rhs':rhs 
    }

def detect_method (problem ):

    constraint_types =problem ['constraint_types']

    needs_big_m =any (ct in [2 ,3 ]for ct in constraint_types )

    if needs_big_m :
        return "BIG_M"
    else :
        return "SIMPLEX"

def setup_simplex_table (problem ,var_prefix ='x'):

    num_vars =problem ['num_vars']
    num_constraints =problem ['num_constraints']
    constraints =problem ['constraints']
    rhs =problem ['rhs']
    obj_coef =problem ['obj_coef']
    is_max =problem ['is_max']

    var_names =[f"{var_prefix }{i +1 }"for i in range (num_vars )]

    for i in range (num_constraints ):
        var_names .append (f"s{i +1 }")

    total_vars =num_vars +num_constraints 

    table =[]
    for i in range (num_constraints ):
        row =constraints [i ].copy ()
        for j in range (num_constraints ):
            if i ==j :
                row .append (1.0 )
            else :
                row .append (0.0 )
        row .append (rhs [i ])
        table .append (row )

    cj =obj_coef .copy ()
    cj .extend ([0.0 ]*num_constraints )

    if not is_max :
        cj =[-c for c in cj ]

    basic_vars =[f"s{i +1 }"for i in range (num_constraints )]

    cb =[0.0 ]*num_constraints 

    return table ,basic_vars ,var_names ,cj ,cb 

def setup_big_m_table (problem ,M =10000 ,var_prefix ='x'):

    num_vars =problem ['num_vars']
    num_constraints =problem ['num_constraints']
    constraints =problem ['constraints']
    constraint_types =problem ['constraint_types']
    rhs =problem ['rhs']
    obj_coef =problem ['obj_coef']
    is_max =problem ['is_max']

    slack_count =0 
    surplus_count =0 
    artificial_count =0 

    var_info =[]

    for i ,ct in enumerate (constraint_types ):
        if ct ==1 :
            slack_count +=1 
            var_info .append ({'slack':slack_count ,'surplus':None ,'artificial':None })
        elif ct ==2 :
            surplus_count +=1 
            artificial_count +=1 
            var_info .append ({'slack':None ,'surplus':surplus_count ,'artificial':artificial_count })
        else :
            artificial_count +=1 
            var_info .append ({'slack':None ,'surplus':None ,'artificial':artificial_count })

    var_names =[f"x{i +1 }"for i in range (num_vars )]

    for i in range (1 ,slack_count +1 ):
        var_names .append (f"s{i }")

    for i in range (1 ,surplus_count +1 ):
        var_names .append (f"S{i }")

    for i in range (1 ,artificial_count +1 ):
        var_names .append (f"A{i }")

    total_vars =num_vars +slack_count +surplus_count +artificial_count 

    table =[]
    basic_vars =[]
    cb =[]

    slack_idx =num_vars 
    surplus_idx =num_vars +slack_count 
    artificial_idx =num_vars +slack_count +surplus_count 

    current_slack =0 
    current_surplus =0 
    current_artificial =0 

    for i in range (num_constraints ):
        row =constraints [i ].copy ()

        row .extend ([0.0 ]*(slack_count +surplus_count +artificial_count ))

        ct =constraint_types [i ]

        if ct ==1 :
            current_slack +=1 
            row [slack_idx +current_slack -1 ]=1.0 
            basic_vars .append (f"s{current_slack }")
            cb .append (0.0 )
        elif ct ==2 :
            current_surplus +=1 
            current_artificial +=1 
            row [surplus_idx +current_surplus -1 ]=-1.0 
            row [artificial_idx +current_artificial -1 ]=1.0 
            basic_vars .append (f"A{current_artificial }")
            if is_max :
                cb .append (-M )
            else :
                cb .append (M )
        else :
            current_artificial +=1 
            row [artificial_idx +current_artificial -1 ]=1.0 
            basic_vars .append (f"A{current_artificial }")
            if is_max :
                cb .append (-M )
            else :
                cb .append (M )

        row .append (rhs [i ])
        table .append (row )

    cj =obj_coef .copy ()
    cj .extend ([0.0 ]*slack_count )
    cj .extend ([0.0 ]*surplus_count )

    for i in range (artificial_count ):
        if is_max :
            cj .append (-M )
        else :
            cj .append (M )

    if not is_max :
        cj =[-c for c in cj ]
        cb =[-c for c in cb ]

    return table ,basic_vars ,var_names ,cj ,cb ,M ,artificial_count 

def find_pivot_column (zj_cj ,var_names ):

    min_val =0 
    pivot_col =-1 

    for j in range (len (zj_cj )):
        if zj_cj [j ]<min_val :
            min_val =zj_cj [j ]
            pivot_col =j 

    return pivot_col ,min_val 

def find_pivot_row (table ,pivot_col ,basic_vars ):

    min_ratio =float ('inf')
    pivot_row =-1 
    ratios =[]

    print ("\nRatio Test (Minimum Ratio Rule):")
    print ("-"*40 )

    for i in range (len (table )):
        element =table [i ][pivot_col ]
        rhs =table [i ][-1 ]

        if element >1e-9 :
            ratio =rhs /element 
            ratios .append (ratio )
            print (f"  Row {i +1 } ({basic_vars [i ]}): {print_fraction (rhs )} / {print_fraction (element )} = {print_fraction (ratio )}")

            if ratio <min_ratio and ratio >=0 :
                min_ratio =ratio 
                pivot_row =i 
        else :
            ratios .append (float ('inf'))
            print (f"  Row {i +1 } ({basic_vars [i ]}): {print_fraction (rhs )} / {print_fraction (element )} = Not applicable (element <= 0)")

    return pivot_row ,min_ratio ,ratios 

def perform_pivot_operation (table ,pivot_row ,pivot_col ,basic_vars ,var_names ,cb ,cj ):

    num_rows =len (table )
    num_cols =len (table [0 ])

    pivot_element =table [pivot_row ][pivot_col ]

    print (f"\nPivot Element: {print_fraction (pivot_element )}")
    print (f"Pivot Position: Row {pivot_row +1 }, Column {pivot_col +1 }")

    new_table =[[0.0 ]*num_cols for _ in range (num_rows )]

    print (f"\nStep 1: New Pivot Row = Old Pivot Row / {print_fraction (pivot_element )}")
    for j in range (num_cols ):
        new_table [pivot_row ][j ]=table [pivot_row ][j ]/pivot_element 

    print ("Step 2: For other rows: New Row = Old Row - (element in pivot column) x New Pivot Row")

    for i in range (num_rows ):
        if i !=pivot_row :
            factor =table [i ][pivot_col ]
            print (f"  Row {i +1 }: Factor = {print_fraction (factor )}")
            for j in range (num_cols ):
                new_table [i ][j ]=table [i ][j ]-factor *new_table [pivot_row ][j ]

    new_basic_vars =basic_vars .copy ()
    new_basic_vars [pivot_row ]=var_names [pivot_col ]

    new_cb =cb .copy ()
    new_cb [pivot_row ]=cj [pivot_col ]

    return new_table ,new_basic_vars ,new_cb 

def check_optimality (zj_cj ):

    return all (val >=-1e-9 for val in zj_cj )

def check_unbounded (table ,pivot_col ):

    for i in range (len (table )):
        if table [i ][pivot_col ]>1e-9 :
            return False 
    return True 

def check_infeasible (basic_vars ,table ,artificial_vars ):

    for i ,var in enumerate (basic_vars ):
        if var .startswith ('A')and table [i ][-1 ]>1e-9 :
            return True 
    return False 

def check_rhs_feasibility (table ):

    for i in range (len (table )):
        if table [i ][-1 ]<-1e-9 :
            return False 
    return True 

def extract_solution (table ,basic_vars ,var_names ,is_max ):

    solution ={}

    for var in var_names :
        solution [var ]=0.0 

    for i ,var in enumerate (basic_vars ):
        solution [var ]=table [i ][-1 ]

    return solution 

def print_solution (solution ,var_names ,zj ,is_max ,num_original_vars ):

    print ("\n"+"="*80 )
    print ("OPTIMAL SOLUTION FOUND!")
    print ("="*80 )

    print ("\nDecision Variables:")
    for i in range (num_original_vars ):
        var =f"x{i +1 }"
        print (f"  {var } = {print_fraction (solution .get (var ,0 ))}")

    z_value =zj [-1 ]
    if not is_max :
        z_value =-z_value 

    print (f"\nOptimal Value of Z = {print_fraction (z_value )}")

    print ("\nSlack/Surplus Variables:")
    for var in var_names :
        if var .startswith ('s')or var .startswith ('S'):
            print (f"  {var } = {print_fraction (solution .get (var ,0 ))}")

def continue_simplex_from_table (table ,basic_vars ,var_names ,cj ,cb ,problem ,start_iteration =0 ):

    iteration =start_iteration 
    optimal_value =None 

    while True :
        num_vars =len (var_names )
        zj =calculate_zj (table ,cb ,num_vars )
        zj_cj =calculate_zj_cj (zj ,cj ,None )

        if check_optimality (zj_cj ):
            print (f"\n{'='*80 }")
            print (f"ITERATION {iteration }")
            print ('='*80 )
            zj_final ,zj_cj_final =print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration )

            if not check_rhs_feasibility (table ):
                print ("\n"+"!"*80 )
                print ("OPTIMAL BUT INFEASIBLE - Switching to Dual Simplex")
                print ("!"*80 )
                input ("\n>>> Press Enter to continue...")
                return None ,table ,basic_vars ,var_names ,cj ,cb 

            solution =extract_solution (table ,basic_vars ,var_names ,problem ['is_max'])
            print_solution (solution ,var_names ,zj_final ,problem ['is_max'],problem ['num_vars'])

            optimal_value =zj_final [-1 ]
            if not problem ['is_max']:
                optimal_value =-optimal_value 
            break 

        pivot_col ,min_zj_cj =find_pivot_column (zj_cj ,var_names )

        if pivot_col ==-1 :
            print ("\nOptimal solution reached!")
            break 

        zj ,zj_cj =print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration ,pivot_col =pivot_col )

        print (f"\nEntering Variable: {var_names [pivot_col ]} (most negative Zj-Cj = {print_fraction (min_zj_cj )})")

        if check_unbounded (table ,pivot_col ):
            print ("\n"+"!"*80 )
            print ("UNBOUNDED SOLUTION!")
            print ("!"*80 )
            break 

        pivot_row ,min_ratio ,ratios =find_pivot_row (table ,pivot_col ,basic_vars )

        if pivot_row ==-1 :
            print ("\nNo valid pivot row found. Problem may be unbounded.")
            break 

        print (f"\nLeaving Variable: {basic_vars [pivot_row ]} (minimum ratio = {print_fraction (min_ratio )})")

        input ("\n>>> Press Enter to perform pivot operation and see next iteration...")

        table ,basic_vars ,cb =perform_pivot_operation (table ,pivot_row ,pivot_col ,basic_vars ,var_names ,cb ,cj )

        iteration +=1 

    return optimal_value ,table ,basic_vars ,var_names ,cj ,cb 

def solve_simplex (problem ,var_prefix ='x'):

    print ("\n"+"#"*80 )
    print ("SOLVING USING SIMPLEX METHOD")
    print ("#"*80 )

    table ,basic_vars ,var_names ,cj ,cb =setup_simplex_table (problem ,var_prefix )

    iteration =0 
    optimal_value =None 

    while True :
        num_vars =len (var_names )
        zj =calculate_zj (table ,cb ,num_vars )
        zj_cj =calculate_zj_cj (zj ,cj ,None )

        if check_optimality (zj_cj ):
            print (f"\n{'='*80 }")
            print (f"ITERATION {iteration }")
            print ('='*80 )
            zj_final ,zj_cj_final =print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration )

            if not check_rhs_feasibility (table ):
                print ("\n"+"!"*80 )
                print ("CONDITION DETECTED: OPTIMAL BUT INFEASIBLE")
                print ("!"*80 )
                print ("The current solution is optimal (all Zj-Cj >= 0)")
                print ("BUT there are negative RHS values (infeasible solution).")
                print ("\nThis requires DUAL SIMPLEX METHOD to restore feasibility.")
                print ("!"*80 )

                input ("\n>>> Press Enter to switch to Dual Simplex Method...")

                return solve_dual_simplex (problem ,var_prefix )

            solution =extract_solution (table ,basic_vars ,var_names ,problem ['is_max'])
            print_solution (solution ,var_names ,zj_final ,problem ['is_max'],problem ['num_vars'])

            optimal_value =zj_final [-1 ]
            if not problem ['is_max']:
                optimal_value =-optimal_value 
            break 

        if not check_rhs_feasibility (table ):
            print (f"\n{'='*80 }")
            print (f"ITERATION {iteration }")
            print ('='*80 )
            zj_temp ,zj_cj_temp =print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration )

            print ("\n"+"!"*80 )
            print ("CONDITION DETECTED: NOT OPTIMAL AND INFEASIBLE")
            print ("!"*80 )
            print ("The current solution is NOT optimal (some Zj-Cj < 0)")
            print ("AND there are negative RHS values (infeasible solution).")
            print ("\nThis requires BIG M METHOD to find a feasible solution.")
            print ("!"*80 )

            input ("\n>>> Press Enter to switch to Big M Method...")

            return solve_big_m (problem ,var_prefix )

        pivot_col ,min_zj_cj =find_pivot_column (zj_cj ,var_names )

        if pivot_col ==-1 :
            print ("\nOptimal solution reached!")
            break 

        zj ,zj_cj =print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration ,pivot_col =pivot_col )

        print (f"\nEntering Variable: {var_names [pivot_col ]} (most negative Zj-Cj = {print_fraction (min_zj_cj )})")

        if check_unbounded (table ,pivot_col ):
            print ("\n"+"!"*80 )
            print ("UNBOUNDED SOLUTION!")
            print ("The problem has no finite optimal solution.")
            print ("!"*80 )
            break 

        pivot_row ,min_ratio ,ratios =find_pivot_row (table ,pivot_col ,basic_vars )

        if pivot_row ==-1 :
            print ("\nNo valid pivot row found. Problem may be unbounded.")
            break 

        print (f"\nLeaving Variable: {basic_vars [pivot_row ]} (minimum ratio = {print_fraction (min_ratio )})")

        input ("\n>>> Press Enter to perform pivot operation and see next iteration...")

        table ,basic_vars ,cb =perform_pivot_operation (table ,pivot_row ,pivot_col ,basic_vars ,var_names ,cb ,cj )

        iteration +=1 

    return optimal_value 

def solve_big_m (problem ,var_prefix ='x'):

    print ("\n"+"#"*80 )
    print ("SOLVING USING BIG M METHOD")
    print ("#"*80 )

    M =10000 

    table ,basic_vars ,var_names ,cj ,cb ,M_val ,artificial_count =setup_big_m_table (problem ,M ,var_prefix )

    artificial_vars =[f"A{i +1 }"for i in range (artificial_count )]

    print (f"\nNote: M is used as a large penalty value (M = {M })")
    print (f"Artificial variables added: {', '.join (artificial_vars )}")

    iteration =0 
    optimal_value =None 

    while True :
        num_vars =len (var_names )
        zj =calculate_zj (table ,cb ,num_vars )
        zj_cj =calculate_zj_cj (zj ,cj ,M_val )

        if check_optimality (zj_cj ):
            print (f"\n{'='*80 }")
            print (f"ITERATION {iteration }")
            print ('='*80 )
            zj_final ,zj_cj_final =print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration ,M_val )
            if check_infeasible (basic_vars ,table ,artificial_vars ):
                print ("\n"+"!"*80 )
                print ("INFEASIBLE SOLUTION!")
                print ("Artificial variable(s) in the final basis with positive value.")
                print ("The problem has no feasible solution.")
                print ("!"*80 )
                optimal_value =None 
            else :
                solution =extract_solution (table ,basic_vars ,var_names ,problem ['is_max'])
                print_solution (solution ,var_names ,zj_final ,problem ['is_max'],problem ['num_vars'])

                optimal_value =zj_final [-1 ]
                if not problem ['is_max']:
                    optimal_value =-optimal_value 
            break 

        pivot_col ,min_zj_cj =find_pivot_column (zj_cj ,var_names )

        if pivot_col ==-1 :
            print ("\nOptimal solution reached!")
            break 

        zj ,zj_cj =print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration ,M_val ,pivot_col )

        print (f"\nEntering Variable: {var_names [pivot_col ]} (most negative Zj-Cj = {print_fraction (min_zj_cj )})")

        if check_unbounded (table ,pivot_col ):
            print ("\n"+"!"*80 )
            print ("UNBOUNDED SOLUTION!")
            print ("The problem has no finite optimal solution.")
            print ("!"*80 )
            break 

        pivot_row ,min_ratio ,ratios =find_pivot_row (table ,pivot_col ,basic_vars )

        if pivot_row ==-1 :
            print ("\nNo valid pivot row found. Problem may be unbounded.")
            break 

        print (f"\nLeaving Variable: {basic_vars [pivot_row ]} (minimum ratio = {print_fraction (min_ratio )})")

        input ("\n>>> Press Enter to perform pivot operation and see next iteration...")

        table ,basic_vars ,cb =perform_pivot_operation (table ,pivot_row ,pivot_col ,basic_vars ,var_names ,cb ,cj )

        iteration +=1 

    return optimal_value 

def check_dual_feasibility (table ):

    most_negative =0 
    negative_row =-1 

    for i in range (len (table )):
        rhs =table [i ][-1 ]
        if rhs <most_negative -1e-9 :
            most_negative =rhs 
            negative_row =i 

    is_feasible =(negative_row ==-1 )
    return is_feasible ,negative_row ,most_negative 

def find_dual_pivot_column (table ,pivot_row ,zj_cj ):

    min_ratio =float ('inf')
    pivot_col =-1 
    ratios =[]

    num_cols =len (table [0 ])-1 

    for j in range (num_cols ):
        element =table [pivot_row ][j ]
        if element <-1e-9 :
            if abs (zj_cj [j ])<1e-9 :
                ratio =0 
            else :
                ratio =abs (zj_cj [j ]/element )

            ratios .append ((j ,element ,zj_cj [j ],ratio ))

            if ratio <min_ratio :
                min_ratio =ratio 
                pivot_col =j 

    return pivot_col ,min_ratio ,ratios 

def solve_dual_simplex (problem ,var_prefix ='x'):

    print ("\n"+"#"*80 )
    print ("SOLVING USING DUAL SIMPLEX METHOD")
    print ("#"*80 )

    print ("\n"+"="*80 )
  
    print ("="*80 )

    input ("\nPress Enter to start solving...")

    table ,basic_vars ,var_names ,cj ,cb =setup_simplex_table (problem ,var_prefix )

    iteration =0 
    optimal_value =None 

    while True :
        num_vars =len (var_names )
        zj =calculate_zj (table ,cb ,num_vars )
        zj_cj =calculate_zj_cj (zj ,cj ,None )

        is_feasible ,negative_row ,most_negative =check_dual_feasibility (table )

        if is_feasible :
            print (f"\n{'='*80 }")
            print (f"ITERATION {iteration }")
            print ('='*80 )
            zj_final ,zj_cj_final =print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration )
            solution =extract_solution (table ,basic_vars ,var_names ,problem ['is_max'])
            print_solution (solution ,var_names ,zj_final ,problem ['is_max'],problem ['num_vars'])

            optimal_value =zj_final [-1 ]
            if not problem ['is_max']:
                optimal_value =-optimal_value 
            break 

        print (f"\n{'='*80 }")
        print (f"ITERATION {iteration }")
        print ('='*80 )
        zj ,zj_cj =print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration )

        print (f"\nLeaving Variable: {basic_vars [negative_row ]} (RHS = {print_fraction (most_negative )})")
        print (f"Leaving Row: {negative_row +1 }")

        pivot_col ,min_ratio ,ratios =find_dual_pivot_column (table ,negative_row ,zj_cj )

        if pivot_col ==-1 :
            print ("\n"+"!"*80 )
            print ("INFEASIBLE SOLUTION!")
            print ("No entering variable found. Problem has no feasible solution.")
            print ("!"*80 )
            return None 

        print ("\nDual Simplex Ratio Test (Minimum |Zj-Cj / element|):")
        print ("-"*40 )
        for j ,element ,zj_cj_val ,ratio in ratios :
            print (f"  Column {var_names [j ]}: |{print_fraction (zj_cj_val )} / {print_fraction (element )}| = {print_fraction (ratio )}")

        print (f"\nEntering Variable: {var_names [pivot_col ]} (minimum ratio = {print_fraction (min_ratio )})")

        input ("\n>>> Press Enter to perform pivot operation and see next iteration...")

        pivot_row =negative_row 
        table ,basic_vars ,cb =perform_pivot_operation (table ,pivot_row ,pivot_col ,basic_vars ,var_names ,cb ,cj )

        iteration +=1 

    return optimal_value 

def convert_to_dual (problem ):

    print ("\n"+"#"*80 )
    print ("PRIMAL TO DUAL CONVERSION")
    print ("#"*80 )

    print ("\nCONVERSION RULES:")
    print ("-"*80 )

    if problem ['is_max']:
        print ("Primal (Maximization) -> Dual (Minimization)")
        print ()
        print ("Primal:                    Dual:")
        print ("  Max Z = Sum(cj * xj)      Min W = Sum(bi * yi)")
        print ("  Sum(aij * xj) <= bi       Sum(aij * yi) >= cj  (for each j)")
        print ("  xj >= 0                    yi >= 0")
    else :
        if all (ct ==1 for ct in problem ['constraint_types']):
            print ("Primal (Minimization with <=) -> Dual (Maximization with <=)")
            print ()
            print ("Primal:                    Dual:")
            print ("  Min Z = Sum(cj * xj)      Max W = Sum(-bi * yi)  NOTE: -bi !")
            print ("  Sum(aij * xj) <= bi       Sum(aij * yi) <= cj  (for each j)")
            print ("  xj >= 0                    yi >= 0")
            print ()
            print ("CRITICAL: For Min with <=, dual has:")
            print ("  • Objective: -b (negative RHS)")
            print ("  • Constraints: <= (same as primal)")
        else :
            print ("Primal (Minimization with >=) -> Dual (Maximization with <=)")
            print ()
            print ("Primal:                    Dual:")
            print ("  Min Z = Sum(cj * xj)      Max W = Sum(bi * yi)")
            print ("  Sum(aij * xj) >= bi       Sum(aij * yi) <= cj  (for each j)")
            print ("  xj >= 0                    yi >= 0")

    print ("\nKEY TRANSFORMATIONS:")
    print ("  - Number of primal constraints = Number of dual variables")
    print ("  - Number of primal variables = Number of dual constraints")
    print ("  - Primal objective coefficients -> Dual RHS values")
    print ("  - Primal RHS values -> Dual objective coefficients")
    if not problem ['is_max']and all (ct ==1 for ct in problem ['constraint_types']):
        print ("  - FOR MIN WITH <=: Dual obj = -b (negative!)")
    print ("  - Constraint matrix A is transposed (rows <-> columns)")
    print ("  - IMPORTANT: By Strong Duality Theorem, optimal values are equal!")
    print ("-"*80 )

    input ("\nPress Enter to see the dual problem...")

    dual ={}

    if not problem ['is_max']and all (ct ==1 for ct in problem ['constraint_types']):
        dual ['is_max']=True 
    elif not problem ['is_max']:
        dual ['is_max']=True 
    else :
        dual ['is_max']=False 

    dual ['num_vars']=problem ['num_constraints']
    dual ['num_constraints']=problem ['num_vars']

    if not problem ['is_max']and all (ct ==1 for ct in problem ['constraint_types']):
        dual ['obj_coef']=[-x for x in problem ['rhs']]
    else :
        dual ['obj_coef']=problem ['rhs'].copy ()

    dual ['constraints']=[]
    negate_matrix =(not problem ['is_max']and all (ct ==1 for ct in problem ['constraint_types']))

    for j in range (problem ['num_vars']):
        dual_constraint =[]
        for i in range (problem ['num_constraints']):
            coef =problem ['constraints'][i ][j ]
            if negate_matrix :
                coef =-coef 
            dual_constraint .append (coef )
        dual ['constraints'].append (dual_constraint )

    dual ['rhs']=problem ['obj_coef'].copy ()

    if problem ['is_max']:
        dual ['constraint_types']=[2 ]*dual ['num_constraints']
    else :
        if all (ct ==1 for ct in problem ['constraint_types']):
            dual ['constraint_types']=[1 ]*dual ['num_constraints']
        elif all (ct ==2 for ct in problem ['constraint_types']):
            dual ['constraint_types']=[2 ]*dual ['num_constraints']
        else :
            dual ['constraint_types']=[]
            for ct in problem ['constraint_types']:
                if ct ==1 :
                    dual ['constraint_types'].append (1 )
                elif ct ==2 :
                    dual ['constraint_types'].append (2 )
                else :
                    dual ['constraint_types'].append (3 )

    for i in range (dual ['num_constraints']):
        if dual ['rhs'][i ]<0 :
            dual ['rhs'][i ]=-dual ['rhs'][i ]
            for j in range (len (dual ['constraints'][i ])):
                dual ['constraints'][i ][j ]=-dual ['constraints'][i ][j ]
            if dual ['constraint_types'][i ]==1 :
                dual ['constraint_types'][i ]=2 
            elif dual ['constraint_types'][i ]==2 :
                dual ['constraint_types'][i ]=1 

    return dual 

def print_dual_problem (dual ):

    print ("\n"+"="*80 )
    print ("DUAL PROBLEM")
    print ("="*80 )

    obj_type ="Maximize"if dual ['is_max']else "Minimize"
    obj_terms =[]
    for i ,c in enumerate (dual ['obj_coef']):
        if c >=0 :
            if i ==0 :
                obj_terms .append (f"{print_fraction (c )}w{i +1 }")
            else :
                obj_terms .append (f"+ {print_fraction (c )}w{i +1 }")
        else :
            obj_terms .append (f"- {print_fraction (abs (c ))}w{i +1 }")

    print (f"\n{obj_type } W = {' '.join (obj_terms )}")

    print ("\nSubject to:")
    constraint_symbols ={1 :'<=',2 :'>=',3 :'='}

    for i in range (dual ['num_constraints']):
        terms =[]
        for j ,c in enumerate (dual ['constraints'][i ]):
            if c >=0 :
                if j ==0 :
                    terms .append (f"{print_fraction (c )}w{j +1 }")
                else :
                    terms .append (f"+ {print_fraction (c )}w{j +1 }")
            else :
                terms .append (f"- {print_fraction (abs (c ))}w{j +1 }")

        symbol =constraint_symbols [dual ['constraint_types'][i ]]
        print (f"  {' '.join (terms )} {symbol } {print_fraction (dual ['rhs'][i ])}")

    print (f"\n  w1, w2, ... w{dual ['num_vars']} >= 0")

def convert_to_dual_and_solve (problem ):

    print ("\n"+"="*80 )
    print ("PRIMAL PROBLEM")
    print ("="*80 )
    print_problem_summary (problem )

    input ("\nPress Enter to solve PRIMAL problem...")

    primal_result =None 
    if any (ct in [2 ,3 ]for ct in problem ['constraint_types']):
        print ("\nSolving primal using Big M Method...")
        primal_result =solve_big_m (problem )
    else :
        print ("\nSolving primal using Simplex Method...")
        primal_result =solve_simplex (problem )

    input ("\n\nPress Enter to see DUAL conversion...")
    dual =convert_to_dual (problem )
    print_dual_problem (dual )

    input ("\n\nPress Enter to solve DUAL problem...")
    dual_result =None 
    if any (ct in [2 ,3 ]for ct in dual ['constraint_types']):
        dual_result =solve_big_m (dual ,var_prefix ='w')
    else :
        dual_result =solve_simplex (dual ,var_prefix ='w')

    print ("\n"+"="*80 )
    print ("STRONG DUALITY THEOREM VERIFICATION")
    print ("="*80 )
    print ("\nThe Strong Duality Theorem states:")
    print ("  If primal and dual both have optimal solutions,")
    print ("  then their optimal objective values are EQUAL.")
    print ()
    print (f"Primal Optimal Value: {primal_result if primal_result is not None else 'N/A'}")
    print (f"Dual Optimal Value:   {dual_result if dual_result is not None else 'N/A'}")

    if primal_result is not None and dual_result is not None :
        if abs (primal_result -dual_result )<1e-6 :
            print ("\nOK VERIFICATION PASSED: Primal and Dual optimal values are equal!")
        else :
            print ("\nX Warning: Values don't match. This might indicate:")
            print ("  - Numerical errors in calculation")
            print ("  - Incorrect problem formulation")
            print ("  - Bug in the conversion or solver")

def solve_simplex_matrix_method (problem ):

    print ("\n"+"#"*80 )
    print ("SIMPLEX METHOD - MATRIX NOTATION")
    print ("#"*80 )

    print ("\n"+"="*80 )
   
    print ("="*80 )

    input ("\nPress Enter to start solving...")

    num_vars =problem ['num_vars']
    num_constraints =problem ['num_constraints']

    A =[]
    b =[]

    for i in range (num_constraints ):
        row =problem ['constraints'][i ].copy ()
        for j in range (num_constraints ):
            if i ==j :
                row .append (1.0 )
            else :
                row .append (0.0 )
        A .append (row )
        b .append (problem ['rhs'][i ])

    C =problem ['obj_coef'].copy ()
    C .extend ([0.0 ]*num_constraints )

    if not problem ['is_max']:
        C =[-c for c in C ]

    total_vars =num_vars +num_constraints 
    var_names =[f"x{i +1 }"for i in range (num_vars )]+[f"s{i +1 }"for i in range (num_constraints )]

    basic_indices =list (range (num_vars ,total_vars ))
    non_basic_indices =list (range (num_vars ))

    iteration =0 

    while True :
        print ("\n"+"="*80 )
        print (f"ITERATION {iteration }")
        print ("="*80 )

        B =[]
        for i in range (num_constraints ):
            B_row =[]
            for j in basic_indices :
                B_row .append (A [i ][j ])
            B .append (B_row )

        N =[]
        for i in range (num_constraints ):
            N_row =[]
            for j in non_basic_indices :
                N_row .append (A [i ][j ])
            N .append (N_row )

        Cb =[C [j ]for j in basic_indices ]
        Cn =[C [j ]for j in non_basic_indices ]

        B_inv =matrix_inverse (B )

        if B_inv is None :
            print ("\nError: Basis matrix is singular. Cannot proceed.")
            break 

        Xb =matrix_vector_mult (B_inv ,b )

        print ("\n"+"-"*80 )
        print ("SIMPLEX TABLEAU (Matrix Method)")
        print ("-"*80 )

        col_width =10 
        print ("\nTableau Structure:")
        print (f"{'Cb':<{col_width }}{'Basis':<{col_width }}",end ="")
        for var in var_names :
            print (f"{var :>{col_width }}",end ="")
        print (f"{'Xb=B^-1b':>{col_width }}")

        print ("-"*(col_width *(total_vars +3 )))

        for i in range (num_constraints ):
            print (f"{print_fraction (Cb [i ]):<{col_width }}",end ="")
            print (f"{var_names [basic_indices [i ]]:<{col_width }}",end ="")

            for j in range (total_vars ):
                A_col_j =[A [row ][j ]for row in range (num_constraints )]
                coef =sum (B_inv [i ][k ]*A_col_j [k ]for k in range (num_constraints ))
                print (f"{print_fraction (coef ):>{col_width }}",end ="")

            print (f"{print_fraction (Xb [i ]):>{col_width }}")

        print ("-"*(col_width *(total_vars +3 )))

        print (f"{'Zj':<{col_width }}{'':<{col_width }}",end ="")
        Zj_row =[]
        for j in range (total_vars ):
            A_col_j =[A [row ][j ]for row in range (num_constraints )]
            Binv_Aj =matrix_vector_mult (B_inv ,A_col_j )
            Zj =sum (Cb [k ]*Binv_Aj [k ]for k in range (num_constraints ))
            Zj_row .append (Zj )
            print (f"{print_fraction (Zj ):>{col_width }}",end ="")

        Z_current =sum (Cb [i ]*Xb [i ]for i in range (num_constraints ))
        print (f"{print_fraction (Z_current ):>{col_width }}")

        print (f"{'Zj-Cj':<{col_width }}{'':<{col_width }}",end ="")
        ZjCj_row =[]
        for j in range (total_vars ):
            zjcj =Zj_row [j ]-C [j ]
            ZjCj_row .append (zjcj )
            print (f"{print_fraction (zjcj ):>{col_width }}",end ="")
        print ()

        print ("="*80 )

        print ("\n"+"-"*80 )
        print ("DETAILED MATRIX CALCULATIONS")
        print ("-"*80 )

        print ("\nCURRENT BASIS:")
        print (f"  Basic variables: {[var_names [j ]for j in basic_indices ]}")
        print (f"  Non-basic variables: {[var_names [j ]for j in non_basic_indices ]}")

        print ("\nB (Basis Matrix):")
        print_matrix (B )

        print ("\nB^-1 (Inverse of Basis Matrix):")
        print_matrix (B_inv )

        print ("\nb (RHS vector):")
        print_vector (b )

        print ("\nXb :")
        print_vector (Xb )

        print ("\nCb :")
        print_vector (Cb )

        print ("\nREDUCED COSTS FOR NON-BASIC VARIABLES:")
        print ("Zj - Cj: ")
        print ()

        zj_cj =[]
        for k ,j in enumerate (non_basic_indices ):
            Aj =[A [i ][j ]for i in range (num_constraints )]
            Binv_Aj =matrix_vector_mult (B_inv ,Aj )
            Cb_Binv_Aj =sum (Cb [i ]*Binv_Aj [i ]for i in range (num_constraints ))
            reduced_cost =Cb_Binv_Aj -C [j ]
            zj_cj .append (reduced_cost )
            print (f"  {var_names [j ]}: Zj - Cj = {print_fraction (reduced_cost )}")

        all_zj_cj =[]
        for j in range (total_vars ):
            Aj =[A [i ][j ]for i in range (num_constraints )]
            Binv_Aj =matrix_vector_mult (B_inv ,Aj )
            Cb_Binv_Aj =sum (Cb [i ]*Binv_Aj [i ]for i in range (num_constraints ))
            reduced_cost =Cb_Binv_Aj -C [j ]
            all_zj_cj .append (reduced_cost )
        all_zj_cj =[]
        for j in range (total_vars ):
            Aj =[A [i ][j ]for i in range (num_constraints )]
            Binv_Aj =matrix_vector_mult (B_inv ,Aj )
            Cb_Binv_Aj =sum (Cb [i ]*Binv_Aj [i ]for i in range (num_constraints ))
            reduced_cost =Cb_Binv_Aj -C [j ]
            all_zj_cj .append (reduced_cost )

        if all (val >=-1e-9 for val in all_zj_cj ):
            print ("\n"+"="*80 )
            print ("OPTIMAL SOLUTION REACHED!")
            print ("="*80 )
            print ("\nAll reduced costs (Zj - Cj) are non-negative.")
            print ()
            print ("Decision Variables:")
            solution =[0.0 ]*total_vars 
            for i ,j in enumerate (basic_indices ):
                solution [j ]=Xb [i ]

            for i in range (num_vars ):
                print (f"  x{i +1 } = {print_fraction (solution [i ])}")

            Z_value =sum (Cb [i ]*Xb [i ]for i in range (len (Cb )))
            if not problem ['is_max']:
                Z_value =-Z_value 

            print (f"\nOptimal Value of Z = {print_fraction (Z_value )}")
            break 

        min_val =min (all_zj_cj )
        entering_var_idx =all_zj_cj .index (min_val )

        if entering_var_idx in basic_indices :
            print (f"\nNote: Most negative is a basic variable (shouldn't happen in normal cases)")

        print (f"\nENTERING VARIABLE: {var_names [entering_var_idx ]} (most negative Zj-Cj = {print_fraction (min_val )})")

        A_entering =[A [i ][entering_var_idx ]for i in range (num_constraints )]
        d =matrix_vector_mult (B_inv ,A_entering )

        print ("\nDIRECTION VECTOR (d = B^-1 x A_entering):")
        print_vector (d )

        print ("\nMINIMUM RATIO TEST:")
     
        print ()

        min_ratio =float ('inf')
        leaving_idx =-1 

        for i in range (len (d )):
            if d [i ]>1e-9 :
                ratio =Xb [i ]/d [i ]
                print (f"  Row {i +1 } ({var_names [basic_indices [i ]]}): {print_fraction (Xb [i ])} / {print_fraction (d [i ])} = {print_fraction (ratio )}")
                if ratio <min_ratio :
                    min_ratio =ratio 
                    leaving_idx =i 
            else :
                print (f"  Row {i +1 } ({var_names [basic_indices [i ]]}): d[{i +1 }] <= 0, skip")

        if leaving_idx ==-1 :
            print ("\nProblem is UNBOUNDED!")
            break 

        leaving_var_idx =basic_indices [leaving_idx ]
        print (f"\nLEAVING VARIABLE: {var_names [leaving_var_idx ]} (minimum ratio = {print_fraction (min_ratio )})")

        if entering_var_idx in non_basic_indices :
            entering_idx =non_basic_indices .index (entering_var_idx )
            basic_indices [leaving_idx ]=entering_var_idx 
            non_basic_indices [entering_idx ]=leaving_var_idx 
            non_basic_indices .sort ()
        else :
            print ("\nError: Entering variable is already basic!")
            break 

        iteration +=1 

        input ("\n>>> Press Enter to continue to next iteration...")

def matrix_inverse (matrix ):

    n =len (matrix )
    aug =[]
    for i in range (n ):
        row =matrix [i ].copy ()
        row .extend ([1.0 if i ==j else 0.0 for j in range (n )])
        aug .append (row )

    for i in range (n ):
        max_row =i 
        for k in range (i +1 ,n ):
            if abs (aug [k ][i ])>abs (aug [max_row ][i ]):
                max_row =k 
        aug [i ],aug [max_row ]=aug [max_row ],aug [i ]

        if abs (aug [i ][i ])<1e-10 :
            return None 

        pivot =aug [i ][i ]
        for j in range (2 *n ):
            aug [i ][j ]/=pivot 

        for k in range (n ):
            if k !=i :
                factor =aug [k ][i ]
                for j in range (2 *n ):
                    aug [k ][j ]-=factor *aug [i ][j ]

    inv =[]
    for i in range (n ):
        inv .append (aug [i ][n :])

    return inv 

def matrix_vector_mult (matrix ,vector ):

    result =[]
    for row in matrix :
        val =sum (row [i ]*vector [i ]for i in range (len (vector )))
        result .append (val )
    return result 

def matrix_transpose (matrix ):

    rows =len (matrix )
    cols =len (matrix [0 ])
    result =[]
    for j in range (cols ):
        row =[]
        for i in range (rows ):
            row .append (matrix [i ][j ])
        result .append (row )
    return result 

def print_matrix (matrix ):

    print ("  [",end ="")
    for i ,row in enumerate (matrix ):
        if i >0 :
            print ("   ",end ="")
        print ("[",end ="")
        for j ,val in enumerate (row ):
            print (f"{print_fraction (val ):>8}",end ="")
            if j <len (row )-1 :
                print (",",end ="")
        print ("]",end ="")
        if i <len (matrix )-1 :
            print ()
        else :
            print ("]")

def print_vector (vector ):

    print ("  [",end ="")
    for i ,val in enumerate (vector ):
        print (f"{print_fraction (val ):>8}",end ="")
        if i <len (vector )-1 :
            print (",",end ="")
    print ("]")

def print_problem_summary (problem ):

    print ("\n"+"="*80 )
    print ("PROBLEM SUMMARY")
    print ("="*80 )

    obj_type ="Maximize"if problem ['is_max']else "Minimize"
    obj_terms =[]
    for i ,c in enumerate (problem ['obj_coef']):
        if c >=0 :
            if i ==0 :
                obj_terms .append (f"{print_fraction (c )}x{i +1 }")
            else :
                obj_terms .append (f"+ {print_fraction (c )}x{i +1 }")
        else :
            obj_terms .append (f"- {print_fraction (abs (c ))}x{i +1 }")

    print (f"\n{obj_type } Z = {' '.join (obj_terms )}")

    print ("\nSubject to:")
    constraint_symbols ={1 :'<=',2 :'>=',3 :'='}

    for i in range (problem ['num_constraints']):
        terms =[]
        for j ,c in enumerate (problem ['constraints'][i ]):
            if c >=0 :
                if j ==0 :
                    terms .append (f"{print_fraction (c )}x{j +1 }")
                else :
                    terms .append (f"+ {print_fraction (c )}x{j +1 }")
            else :
                terms .append (f"- {print_fraction (abs (c ))}x{j +1 }")

        symbol =constraint_symbols [problem ['constraint_types'][i ]]
        print (f"  {' '.join (terms )} {symbol } {print_fraction (problem ['rhs'][i ])}")

    print (f"\n  x1, x2, ... x{problem ['num_vars']} >= 0")

def print_assignment_matrix (matrix ,title ="",selected =None ,lines_h =None ,lines_v =None ):

    if title :
        print ("\n"+"="*80 )
        print (title )
        print ("="*80 )

    n =len (matrix )
    m =len (matrix [0 ])
    col_width =10 
    row_label_width =8 

    print (f"\n{'':<{row_label_width }}",end ="")
    for j in range (m ):
        marker =">"if lines_v and j in lines_v else " "
        print (f"{marker +'C'+str (j +1 ):>{col_width }}",end ="")
    print ()
    print ("-"*(row_label_width +col_width *m ))

    for i in range (n ):
        marker =">"if lines_h and i in lines_h else " "
        row_label =marker +"R"+str (i +1 )
        print (f"{row_label :<{row_label_width }}",end ="")

        for j in range (m ):
            val =matrix [i ][j ]
            val_str =print_fraction (val )

            is_selected =selected and (i ,j )in selected 

            if is_selected :
                print (f"{'['+val_str +']':>{col_width }}",end ="")
            else :
                print (f"{val_str :>{col_width }}",end ="")
        print ()
    print ()

    if lines_h or lines_v :
        zeros =[(i ,j )for i in range (n )for j in range (m )if abs (matrix [i ][j ])<1e-9 ]

        show_coverage =(len (lines_h )+len (lines_v ))<n 

        if zeros and show_coverage :
            print ("Zeros covered by lines:")
            for i ,j in sorted (zeros ):
                coverage =[]
                if lines_h and i in lines_h :
                    coverage .append (f"Horizontal line through Row {i +1 }")
                if lines_v and j in lines_v :
                    coverage .append (f"Vertical line through Col {j +1 }")
                if coverage :
                    print (f"  Zero at R{i +1 }C{j +1 } covered by: {', '.join (coverage )}")
            print ()

def row_reduction (matrix ):

    print ("\n"+"#"*80 )
    print ("STEP 2: ROW REDUCTION")
    print ("#"*80 )
    print ("\nFor each row, subtract the minimum element from all elements in that row")

    n =len (matrix )
    m =len (matrix [0 ])
    reduced =[row [:]for row in matrix ]

    for i in range (n ):
        min_val =min (matrix [i ])
        print (f"\nRow {i +1 }: Minimum = {print_fraction (min_val )}")
        for j in range (m ):
            reduced [i ][j ]=matrix [i ][j ]-min_val 
        print (f"  After reduction: {[print_fraction (x )for x in reduced [i ]]}")

    print_assignment_matrix (reduced ,"Matrix after Row Reduction")
    return reduced 

def column_reduction (matrix ):

    print ("\n"+"#"*80 )
    print ("STEP 3: COLUMN REDUCTION")
    print ("#"*80 )
    print ("\nFor each column, subtract the minimum element from all elements in that column")

    n =len (matrix )
    m =len (matrix [0 ])
    reduced =[row [:]for row in matrix ]

    for j in range (m ):
        col =[matrix [i ][j ]for i in range (n )]
        min_val =min (col )
        print (f"\nColumn {j +1 }: Minimum = {print_fraction (min_val )}")
        for i in range (n ):
            reduced [i ][j ]=matrix [i ][j ]-min_val 

    print_assignment_matrix (reduced ,"Matrix after Column Reduction")
    return reduced 

def find_zeros (matrix ):

    zeros =[]
    for i in range (len (matrix )):
        for j in range (len (matrix [0 ])):
            if abs (matrix [i ][j ])<1e-9 :
                zeros .append ((i ,j ))
    return zeros 

def count_zeros_in_row (matrix ,row ):

    return sum (1 for j in range (len (matrix [0 ]))if abs (matrix [row ][j ])<1e-9 )

def count_zeros_in_col (matrix ,col ):

    return sum (1 for i in range (len (matrix ))if abs (matrix [i ][col ])<1e-9 )

def draw_minimum_lines (matrix ):

    print ("\n"+"#"*80 )
    print ("STEP 4: DRAW MINIMUM LINES TO COVER ALL ZEROS")
    print ("#"*80 )
    print ("\nStrategy: Mark rows/columns with unique zeros")

    n =len (matrix )
    m =len (matrix [0 ])

    lines_h =set ()
    lines_v =set ()

    changed =True 
    iteration =0 
    while changed :
        changed =False 
        iteration +=1 

        for i in range (n ):
            if i in lines_h :
                continue 

            unmarked_zeros =[(i ,j )for j in range (m )
            if abs (matrix [i ][j ])<1e-9 and j not in lines_v ]

            if len (unmarked_zeros )==1 :
                row ,col =unmarked_zeros [0 ]
                lines_v .add (col )
                print (f"  Row {i +1 } has unique zero at C{col +1 } -> Draw vertical line through Col {col +1 }")
                changed =True 

        for j in range (m ):
            if j in lines_v :
                continue 

            unmarked_zeros =[(i ,j )for i in range (n )
            if abs (matrix [i ][j ])<1e-9 and i not in lines_h ]

            if len (unmarked_zeros )==1 :
                row ,col =unmarked_zeros [0 ]
                lines_h .add (row )
                print (f"  Col {j +1 } has unique zero at R{row +1 } -> Draw horizontal line through Row {row +1 }")
                changed =True 

    uncovered_zeros =[(i ,j )for i in range (n )for j in range (m )
    if abs (matrix [i ][j ])<1e-9 and i not in lines_h and j not in lines_v ]

    if uncovered_zeros :
        print (f"\n  {len (uncovered_zeros )} uncovered zeros remaining. Using greedy approach...")
        while uncovered_zeros :
            row_counts ={}
            col_counts ={}
            for i ,j in uncovered_zeros :
                row_counts [i ]=row_counts .get (i ,0 )+1 
                col_counts [j ]=col_counts .get (j ,0 )+1 

            best_row =max (row_counts .items (),key =lambda x :x [1 ],default =(None ,0 ))
            best_col =max (col_counts .items (),key =lambda x :x [1 ],default =(None ,0 ))

            if best_row [1 ]>=best_col [1 ]and best_row [0 ]is not None :
                lines_h .add (best_row [0 ])
                print (f"  Draw horizontal line through Row {best_row [0 ]+1 } (covers {best_row [1 ]} zeros)")
            elif best_col [0 ]is not None :
                lines_v .add (best_col [0 ])
                print (f"  Draw vertical line through Col {best_col [0 ]+1 } (covers {best_col [1 ]} zeros)")

            uncovered_zeros =[(i ,j )for i in range (n )for j in range (m )
            if abs (matrix [i ][j ])<1e-9 and i not in lines_h and j not in lines_v ]

    lines_h =list (lines_h )
    lines_v =list (lines_v )
    num_lines =len (lines_h )+len (lines_v )

    print (f"\nTotal lines drawn: {num_lines }")
    print (f"Horizontal lines (rows): {[r +1 for r in lines_h ]}")
    print (f"Vertical lines (columns): {[c +1 for c in lines_v ]}")

    print_assignment_matrix (matrix ,"Matrix with Lines Drawn",lines_h =lines_h ,lines_v =lines_v )

    return lines_h ,lines_v ,num_lines 

def create_additional_zeros (matrix ,lines_h ,lines_v ):

    print ("\n"+"#"*80 )
    print ("STEP 5: CREATE ADDITIONAL ZEROS")
    print ("#"*80 )

    n =len (matrix )
    m =len (matrix [0 ])

    min_uncovered =float ('inf')
    uncovered_count =0 
    for i in range (n ):
        for j in range (m ):
            if i not in lines_h and j not in lines_v :
                uncovered_count +=1 
                if matrix [i ][j ]<min_uncovered :
                    min_uncovered =matrix [i ][j ]

    if uncovered_count ==0 or min_uncovered ==float ('inf'):
        print ("\nERROR: All elements are covered by lines!")
        print ("This shouldn't happen. Returning matrix unchanged.")
        return matrix 

    print (f"\nSmallest uncovered element: {print_fraction (min_uncovered )}")
    print ("\nOperations:")
    print (f"  - Subtract {print_fraction (min_uncovered )} from all uncovered elements")
    print (f"  - Add {print_fraction (min_uncovered )} to elements at line intersections")
    print (f"  - Elements covered by one line remain unchanged")

    new_matrix =[row [:]for row in matrix ]

    for i in range (n ):
        for j in range (m ):
            in_h =i in lines_h 
            in_v =j in lines_v 

            if not in_h and not in_v :
                new_matrix [i ][j ]=matrix [i ][j ]-min_uncovered 
            elif in_h and in_v :
                new_matrix [i ][j ]=matrix [i ][j ]+min_uncovered 

    print_assignment_matrix (new_matrix ,"Matrix after Creating Additional Zeros")

    return new_matrix 

def make_assignment (matrix ,original_matrix ):

    print ("\n"+"#"*80 )
    print ("STEP 6: MAKE OPTIMAL ASSIGNMENT")
    print ("#"*80 )
    print ("\nAssign one zero per row and column")
    print ("Strategy: Use backtracking to find complete assignment")

    n =len (matrix )
    m =len (matrix [0 ])

    zeros ={}
    for i in range (n ):
        zeros [i ]=[j for j in range (m )if abs (matrix [i ][j ])<1e-9 ]

    best_assignment =[]
    best_count =0 

    def backtrack (row ,current_assignment ,used_cols ):

        nonlocal best_assignment ,best_count 

        if row ==n :
            if len (current_assignment )>best_count :
                best_count =len (current_assignment )
                best_assignment =current_assignment [:]
            return len (current_assignment )==n 

        for col in zeros [row ]:
            if col not in used_cols :
                current_assignment .append ((row ,col ))
                used_cols .add (col )

                if backtrack (row +1 ,current_assignment ,used_cols ):
                    return True 

                current_assignment .pop ()
                used_cols .remove (col )

        if backtrack (row +1 ,current_assignment ,used_cols ):
            return True 

        return False 

    success =backtrack (0 ,[],set ())
    assignment ={i :j for i ,j in best_assignment }

    assigned =best_assignment 
    for i ,j in sorted (assigned ):
        print (f"  Assign: R{i +1 } -> C{j +1 }")

    assigned_rows ={i for i ,j in assigned }
    for i in range (n ):
        if i not in assigned_rows :
            print (f"  ERROR: R{i +1 } could not be assigned!")

    if not success or len (assigned )<n :
        print (f"\n[!] WARNING: Could only assign {len (assigned )} out of {n } rows!")
        print ("The matrix may need more iterations (Steps 4-5) to create enough zeros.")

    print_assignment_matrix (matrix ,"Final Assignment",selected =assigned )

    total_cost =sum (original_matrix [i ][j ]for i ,j in assigned )

    print ("\n"+"="*80 )
    print ("STEP 7: CALCULATE TOTAL COST")
    print ("="*80 )
    print ("\nUsing original cost matrix:")
    for i ,j in sorted (assigned ):
        print (f"  R{i +1 } -> C{j +1 }: Cost = {print_fraction (original_matrix [i ][j ])}")

    print (f"\nTotal Cost = {print_fraction (total_cost )}")

    return assigned ,total_cost 

def parse_hungarian_problem (filename ='problem.txt'):

    try :
        for encoding in ['utf-8-sig','utf-8',None ]:
            try :
                with open (filename ,'r',encoding =encoding )as f :
                    lines =[line .strip ()for line in f .readlines ()if line .strip ()]
                break 
            except (UnicodeDecodeError ,LookupError ):
                continue 
        else :
            print (f"Error: Could not decode file {filename }")
            return None 

        if not lines :
            print (f"Error: File {filename } is empty")
            return None 

        problem_type =lines [0 ].strip ().replace ('\ufeff','').replace ('\ufffe','').lower ()
        if problem_type not in ['min','max']:
            print (f"Error: First line must be 'min' or 'max', found '{lines [0 ]}'")
            return None 

        is_max =(problem_type =='max')

        matrix =[]
        for i ,line in enumerate (lines [1 :],start =2 ):
            try :
                row =[float (x .strip ())for x in line .split ()]
                if not row :
                    continue 
                matrix .append (row )
            except ValueError as e :
                print (f"Error parsing line {i }: {line }")
                print (f"  {e }")
                return None 

        if not matrix :
            print ("Error: No cost matrix found in file")
            return None 

        row_lengths =[len (row )for row in matrix ]
        if len (set (row_lengths ))>1 :
            print (f"Error: Inconsistent row lengths: {row_lengths }")
            return None 

        return {
        'is_max':is_max ,
        'matrix':matrix ,
        'n':len (matrix ),
        'm':len (matrix [0 ])
        }

    except FileNotFoundError :
        print (f"Error: File '{filename }' not found")
        return None 
    except Exception as e :
        print (f"Error reading file: {e }")
        return None 

def solve_hungarian_method ():

    print ("\n"+"="*80 )
    print ("ASSIGNMENT PROBLEM - HUNGARIAN METHOD")
    print ("="*80 )

    print ("\n1. Manual Input")
    print ("2. Load from File (problem.txt)")
    input_choice =get_int_input ("Enter choice (1-2): ")

    if input_choice ==2 :
        print ("\nLoading problem from 'problem.txt'...")
        problem_data =parse_hungarian_problem ()
        if not problem_data :
            return 

        print ("Problem loaded successfully!")
        is_max =problem_data ['is_max']
        matrix =problem_data ['matrix']
        n =problem_data ['n']
        m =problem_data ['m']
    else :
        print ("\n1. Minimization Problem")
        print ("2. Maximization Problem")
        problem_type =get_int_input ("Enter choice (1-2): ")

        is_max =(problem_type ==2 )

        n =get_int_input ("\nEnter number of rows (workers/machines): ")
        m =get_int_input ("Enter number of columns (jobs/tasks): ")

        print (f"\nEnter the cost matrix ({n }x{m }):")
        matrix =[]
        for i in range (n ):
            print (f"Row {i +1 }:")
            row =[]
            for j in range (m ):
                val =get_float_input (f"  Element [{i +1 },{j +1 }]: ")
                row .append (val )
            matrix .append (row )

    original_matrix =[row [:]for row in matrix ]

    print_assignment_matrix (original_matrix ,"Original Cost Matrix")

    print ("\n"+"#"*80 )
    print ("STEP 1: BALANCE THE MATRIX")
    print ("#"*80 )

    if n <m :
        print (f"\nAdding {m -n } dummy row(s) with cost 0")
        for _ in range (m -n ):
            matrix .append ([0.0 ]*m )
        n =m 
    elif m <n :
        print (f"\nAdding {n -m } dummy column(s) with cost 0")
        for i in range (n ):
            matrix [i ].extend ([0.0 ]*(n -m ))
        m =n 
    else :
        print ("\nMatrix is already balanced (square matrix)")

    if n !=len (original_matrix )or m !=len (original_matrix [0 ]):
        original_ext =[row [:]for row in original_matrix ]
        for i in range (len (original_ext )):
            original_ext [i ].extend ([0.0 ]*(n -len (original_matrix [0 ])))
        for _ in range (n -len (original_matrix )):
            original_ext .append ([0.0 ]*n )
        original_matrix =original_ext 
        print_assignment_matrix (matrix ,"Balanced Matrix")

    if is_max :
        print ("\n"+"#"*80 )
        print ("CONVERTING MAXIMIZATION TO MINIMIZATION")
        print ("#"*80 )
        print ("\nMethod: New Cost = (Maximum element) - (Original element)")

        max_element =max (max (row )for row in matrix )
        print (f"\nMaximum element in matrix: {print_fraction (max_element )}")

        for i in range (n ):
            for j in range (n ):
                matrix [i ][j ]=max_element -matrix [i ][j ]

        print_assignment_matrix (matrix ,"Converted Matrix (for MIN problem)")

    iteration =0 

    matrix =row_reduction (matrix )

    matrix =column_reduction (matrix )

    max_iterations =20 
    while iteration <max_iterations :
        iteration +=1 
        print ("\n"+"="*80 )
        print (f"ITERATION {iteration }")
        print ("="*80 )

        lines_h ,lines_v ,num_lines =draw_minimum_lines (matrix )

        if num_lines >=n :
            zeros ={}
            for i in range (n ):
                zeros [i ]=[j for j in range (n )if abs (matrix [i ][j ])<1e-9 ]

            if all (len (zeros [i ])>0 for i in range (n )):
                def can_assign (row ,used_cols ):
                    if row ==n :
                        return True 
                    for col in zeros [row ]:
                        if col not in used_cols :
                            used_cols .add (col )
                            if can_assign (row +1 ,used_cols ):
                                return True 
                            used_cols .remove (col )
                    return False 

                if can_assign (0 ,set ()):
                    print ("\n"+"="*80 )
                    print (f"OPTIMAL! Number of lines ({num_lines }) >= Matrix size ({n })")
                    print ("And complete assignment is possible!")
                    print ("="*80 )
                    break 
                else :
                    print (f"\nLines ({num_lines }) >= Matrix size, but complete assignment not possible yet.")
                    print ("Need to create more zeros...")
            else :
                print (f"\nLines ({num_lines }) >= Matrix size, but some rows have no zeros.")
                print ("Need to create more zeros...")
        else :
            print (f"\nNot optimal yet. Lines ({num_lines }) < Matrix size ({n })")
            print ("Need to create more zeros...")

        matrix =create_additional_zeros (matrix ,lines_h ,lines_v )

    if iteration >=max_iterations :
        print (f"\n[!] WARNING: Reached maximum iterations ({max_iterations })")
        print ("Proceeding with best available assignment...")

    input ("\nPress Enter to make optimal assignment...")
    assigned ,total_cost =make_assignment (matrix ,original_matrix )

    return assigned ,total_cost 

def parse_transportation_problem (filepath ):

    try :
        with open (filepath ,'r',encoding ='utf-8-sig')as f :
            content =f .read ()

        content =content .lstrip ('\ufeff')
        lines =[line .strip ()for line in content .split ('\n')if line .strip ()]

        if not lines :
            return None 

        all_rows =[]
        for line in lines :
            row =[int (x )for x in line .split ()]
            if row :
                all_rows .append (row )

        if len (all_rows )<2 :
            return None 

        demand_row =all_rows [-1 ]

        m =len (all_rows )-1 
        n =len (demand_row )

        cost_matrix =[]
        supply =[]

        for i in range (m ):
            row =all_rows [i ]
            if len (row )==n +1 :
                cost_matrix .append (row [:n ])
                supply .append (row [n ])
            else :
                return None 

        demand =demand_row [:n ]

        return {
        'sources':m ,
        'destinations':n ,
        'cost_matrix':cost_matrix ,
        'supply':supply ,
        'demand':demand 
        }
    except :
        return None 

def print_transportation_table (allocation ,cost_matrix ,supply ,demand ,title =""):

    m =len (supply )
    n =len (demand )

    if title :
        print (f"\n{title }")
        print ("="*80 )

    print ("\n"+" "*12 ,end ="")
    for j in range (n ):
        print (f"D{j +1 :^10}",end ="")
    print (f"{'Supply':^12}")
    print ("-"*80 )

    for i in range (m ):
        print (f"S{i +1 :^10} |",end ="")
        for j in range (n ):
            if allocation [i ][j ]>0 :
                print (f"{allocation [i ][j ]:>4}({cost_matrix [i ][j ]:<2}) ",end ="")
            else :
                print (f"  - ({cost_matrix [i ][j ]:<2}) ",end ="")
        print (f" | {supply [i ]:>5}")

    print ("-"*80 )
    print (f"{'Demand':^10} |",end ="")
    for j in range (n ):
        print (f"{demand [j ]:^10}",end ="")
    print ()

    total_cost =0 
    for i in range (m ):
        for j in range (n ):
            total_cost +=allocation [i ][j ]*cost_matrix [i ][j ]

    print (f"\nTotal Transportation Cost: {total_cost }")
    print ()

def northwest_corner_method (cost_matrix ,supply ,demand ):

    m =len (supply )
    n =len (demand )

    supply_copy =supply [:]
    demand_copy =demand [:]

    allocation =[[0 ]*n for _ in range (m )]

    print ("\nNORTHWEST CORNER METHOD")
    print ("="*80 )
    print ("\nStarting from top-left corner (S1, D1)")

    i ,j =0 ,0 
    step =1 

    while i <m and j <n :
        quantity =min (supply_copy [i ],demand_copy [j ])
        allocation [i ][j ]=quantity 

        print (f"\nStep {step }: Allocate {quantity } to cell (S{i +1 }, D{j +1 })")
        print (f"  Supply[S{i +1 }] = {supply_copy [i ]} - {quantity } = {supply_copy [i ]-quantity }")
        print (f"  Demand[D{j +1 }] = {demand_copy [j ]} - {quantity } = {demand_copy [j ]-quantity }")

        supply_copy [i ]-=quantity 
        demand_copy [j ]-=quantity 

        if supply_copy [i ]==0 :
            print (f"  Supply for S{i +1 } exhausted, move to next source")
            i +=1 
        if demand_copy [j ]==0 :
            print (f"  Demand for D{j +1 } satisfied, move to next destination")
            j +=1 

        step +=1 

    return allocation 

def least_cost_method (cost_matrix ,supply ,demand ):

    m =len (supply )
    n =len (demand )

    supply_copy =supply [:]
    demand_copy =demand [:]

    allocation =[[0 ]*n for _ in range (m )]

    print ("\nLEAST COST METHOD")
    print ("="*80 )
    print ("\nAllocating to cells with minimum cost first")

    step =1 

    while any (s >0 for s in supply_copy )and any (d >0 for d in demand_copy ):
        min_cost =float ('inf')
        min_i ,min_j =-1 ,-1 

        for i in range (m ):
            for j in range (n ):
                if supply_copy [i ]>0 and demand_copy [j ]>0 :
                    if cost_matrix [i ][j ]<min_cost :
                        min_cost =cost_matrix [i ][j ]
                        min_i =i 
                        min_j =j 

        if min_i ==-1 :
            break 

        quantity =min (supply_copy [min_i ],demand_copy [min_j ])
        allocation [min_i ][min_j ]=quantity 

        print (f"\nStep {step }: Minimum cost = {min_cost } at cell (S{min_i +1 }, D{min_j +1 })")
        print (f"  Allocate {quantity } to cell (S{min_i +1 }, D{min_j +1 })")
        print (f"  Supply[S{min_i +1 }] = {supply_copy [min_i ]} - {quantity } = {supply_copy [min_i ]-quantity }")
        print (f"  Demand[D{min_j +1 }] = {demand_copy [min_j ]} - {quantity } = {demand_copy [min_j ]-quantity }")

        supply_copy [min_i ]-=quantity 
        demand_copy [min_j ]-=quantity 

        step +=1 

    return allocation 

def vogel_approximation_method (cost_matrix ,supply ,demand ):

    m =len (supply )
    n =len (demand )

    supply_copy =supply [:]
    demand_copy =demand [:]

    allocation =[[0 ]*n for _ in range (m )]

    print ("\nVOGEL'S APPROXIMATION METHOD (VAM)")
    print ("="*80 )
    print ("\nCalculating penalties (difference between two smallest costs)")

    step =1 

    while any (s >0 for s in supply_copy )and any (d >0 for d in demand_copy ):
        print (f"\nStep {step }:")

        row_penalties =[]
        for i in range (m ):
            if supply_copy [i ]==0 :
                row_penalties .append (-1 )
                continue 

            costs =[]
            for j in range (n ):
                if demand_copy [j ]>0 :
                    costs .append (cost_matrix [i ][j ])

            if len (costs )>=2 :
                costs .sort ()
                row_penalties .append (costs [1 ]-costs [0 ])
            elif len (costs )==1 :
                row_penalties .append (costs [0 ])
            else :
                row_penalties .append (-1 )

        col_penalties =[]
        for j in range (n ):
            if demand_copy [j ]==0 :
                col_penalties .append (-1 )
                continue 

            costs =[]
            for i in range (m ):
                if supply_copy [i ]>0 :
                    costs .append (cost_matrix [i ][j ])

            if len (costs )>=2 :
                costs .sort ()
                col_penalties .append (costs [1 ]-costs [0 ])
            elif len (costs )==1 :
                col_penalties .append (costs [0 ])
            else :
                col_penalties .append (-1 )

        print ("  Row Penalties:",[p if p >=0 else "-"for p in row_penalties ])
        print ("  Col Penalties:",[p if p >=0 else "-"for p in col_penalties ])

        max_row_penalty =max (row_penalties )
        max_col_penalty =max (col_penalties )

        if max_row_penalty >=max_col_penalty :
            row_idx =row_penalties .index (max_row_penalty )
            print (f"  Maximum penalty = {max_row_penalty } in Row S{row_idx +1 }")

            min_cost =float ('inf')
            min_j =-1 
            for j in range (n ):
                if demand_copy [j ]>0 and cost_matrix [row_idx ][j ]<min_cost :
                    min_cost =cost_matrix [row_idx ][j ]
                    min_j =j 

            i ,j =row_idx ,min_j 
        else :
            col_idx =col_penalties .index (max_col_penalty )
            print (f"  Maximum penalty = {max_col_penalty } in Column D{col_idx +1 }")

            min_cost =float ('inf')
            min_i =-1 
            for i in range (m ):
                if supply_copy [i ]>0 and cost_matrix [i ][col_idx ]<min_cost :
                    min_cost =cost_matrix [i ][col_idx ]
                    min_i =i 

            i ,j =min_i ,col_idx 

        quantity =min (supply_copy [i ],demand_copy [j ])
        allocation [i ][j ]=quantity 

        print (f"  Allocate {quantity } to cell (S{i +1 }, D{j +1 }) with cost {cost_matrix [i ][j ]}")

        supply_copy [i ]-=quantity 
        demand_copy [j ]-=quantity 

        step +=1 

    return allocation 

def check_degeneracy (allocation ,m ,n ):

    basic_cells =0 
    for i in range (m ):
        for j in range (n ):
            if allocation [i ][j ]>0 :
                basic_cells +=1 

    required =m +n -1 

    print (f"\nDEGENERACY CHECK:")
    print (f"  Number of allocations: {basic_cells }")
    print (f"  Required allocations: {required } (m + n - 1 = {m } + {n } - 1)")

    if basic_cells <required :
        print (f"  STATUS: DEGENERATE (Need {required -basic_cells } more allocation(s))")
        print (f"  ACTION: Add epsilon (very small value) to {required -basic_cells } independent cell(s)")
        return True ,required -basic_cells 
    elif basic_cells ==required :
        print (f"  STATUS: NON-DEGENERATE")
        return False ,0 
    else :
        print (f"  STATUS: ERROR - Too many allocations")
        return False ,0 

def handle_degeneracy (allocation ,cost_matrix ,m ,n ,num_epsilon ):

    print (f"\nHANDLING DEGENERACY:")
    print (f"  Need to add {num_epsilon } epsilon value(s) to independent cell(s)")

    candidates =[]
    for i in range (m ):
        for j in range (n ):
            if allocation [i ][j ]==0 :
                candidates .append ((cost_matrix [i ][j ],i ,j ))

    candidates .sort ()

    added =0 
    for cost ,i ,j in candidates :
        if added >=num_epsilon :
            break 

        allocation [i ][j ]=0.001 
        print (f"  Added epsilon to cell (S{i +1 }, D{j +1 }) with cost {cost }")
        added +=1 

    return allocation 

def calculate_uv_values (allocation ,cost_matrix ,m ,n ):

    u =[None ]*m 
    v =[None ]*n 

    u [0 ]=0 

    print ("\nCALCULATING u AND v VALUES:")
    print ("  Using: u[i] + v[j] = c[i][j] for allocated cells")
    print ("  Starting with u[S1] = 0")

    changed =True 
    iteration =1 
    while changed :
        changed =False 

        for i in range (m ):
            for j in range (n ):
                if allocation [i ][j ]>0 or (isinstance (allocation [i ][j ],float )and allocation [i ][j ]>0 ):
                    if u [i ]is not None and v [j ]is None :
                        v [j ]=cost_matrix [i ][j ]-u [i ]
                        print (f"  v[D{j +1 }] = c[S{i +1 },D{j +1 }] - u[S{i +1 }] = {cost_matrix [i ][j ]} - {u [i ]} = {v [j ]}")
                        changed =True 
                    elif u [i ]is None and v [j ]is not None :
                        u [i ]=cost_matrix [i ][j ]-v [j ]
                        print (f"  u[S{i +1 }] = c[S{i +1 },D{j +1 }] - v[D{j +1 }] = {cost_matrix [i ][j ]} - {v [j ]} = {u [i ]}")
                        changed =True 

    print (f"\n  u values: {['u[S'+str (i +1 )+']='+str (u [i ])for i in range (m )]}")
    print (f"  v values: {['v[D'+str (j +1 )+']='+str (v [j ])for j in range (n )]}")

    return u ,v 

def calculate_opportunity_costs (allocation ,cost_matrix ,u ,v ,m ,n ):

    opportunity_costs =[[None ]*n for _ in range (m )]

    print ("\nCALCULATING OPPORTUNITY COSTS (Pij = cij - ui - vj):")
    print ("  For non-allocated cells only:")

    min_cost =float ('inf')
    min_i ,min_j =-1 ,-1 

    for i in range (m ):
        for j in range (n ):
            if allocation [i ][j ]==0 :
                opportunity_costs [i ][j ]=cost_matrix [i ][j ]-u [i ]-v [j ]
                print (f"  P[S{i +1 },D{j +1 }] = {cost_matrix [i ][j ]} - {u [i ]} - {v [j ]} = {opportunity_costs [i ][j ]}")

                if opportunity_costs [i ][j ]<min_cost :
                    min_cost =opportunity_costs [i ][j ]
                    min_i =i 
                    min_j =j 

    return opportunity_costs ,min_i ,min_j ,min_cost 

def find_loop (allocation ,start_i ,start_j ,m ,n ):

    basic_cells =[]
    for i in range (m ):
        for j in range (n ):
            if allocation [i ][j ]>0 or (isinstance (allocation [i ][j ],float )and allocation [i ][j ]>0 ):
                basic_cells .append ((i ,j ))

    basic_cells .append ((start_i ,start_j ))

    def find_path (current ,path ,direction ):

        if len (path )>1 and current ==path [0 ]and len (path )%2 ==0 :
            return path 

        i ,j =current 

        if direction ==0 :
            for cell in basic_cells :
                if cell [0 ]==i and cell [1 ]!=j and cell not in path :
                    result =find_path (cell ,path +[cell ],1 )
                    if result :
                        return result 
            if (start_i ,start_j )in [(c [0 ],c [1 ])for c in basic_cells if c [0 ]==i and c [1 ]!=j ]:
                if len (path )>2 :
                    return path +[(start_i ,start_j )]
        else :
            for cell in basic_cells :
                if cell [1 ]==j and cell [0 ]!=i and cell not in path :
                    result =find_path (cell ,path +[cell ],0 )
                    if result :
                        return result 
            if (start_i ,start_j )in [(c [0 ],c [1 ])for c in basic_cells if c [1 ]==j and c [0 ]!=i ]:
                if len (path )>2 :
                    return path +[(start_i ,start_j )]

        return None 

    loop =find_path ((start_i ,start_j ),[(start_i ,start_j )],0 )
    if not loop :
        loop =find_path ((start_i ,start_j ),[(start_i ,start_j )],1 )

    return loop 

def print_loop (loop ):

    if not loop :
        print ("  ERROR: Could not find loop")
        return 

    print ("\n  LOOP PATH:")
    print ("  ",end ="")
    for i ,cell in enumerate (loop ):
        if i <len (loop )-1 :
            print (f"(S{cell [0 ]+1 },D{cell [1 ]+1 }) --> ",end ="")
        else :
            print (f"(S{cell [0 ]+1 },D{cell [1 ]+1 })")

    print ("\n  LOOP ADJUSTMENTS:")
    for i ,cell in enumerate (loop [:-1 ]):
        sign ='+'if i %2 ==0 else '-'
        print (f"    (S{cell [0 ]+1 },D{cell [1 ]+1 }): {sign }")

def adjust_allocation (allocation ,loop ):

    if not loop or len (loop )<4 :
        return allocation 

    min_value =float ('inf')
    for i ,cell in enumerate (loop [:-1 ]):
        if i %2 ==1 :
            if allocation [cell [0 ]][cell [1 ]]<min_value :
                min_value =allocation [cell [0 ]][cell [1 ]]

    print (f"\n  Minimum value in negative cells: {min_value }")
    print (f"  Adjusting allocations by {min_value }:")

    for i ,cell in enumerate (loop [:-1 ]):
        if i %2 ==0 :
            allocation [cell [0 ]][cell [1 ]]+=min_value 
            print (f"    (S{cell [0 ]+1 },D{cell [1 ]+1 }): {allocation [cell [0 ]][cell [1 ]]-min_value } + {min_value } = {allocation [cell [0 ]][cell [1 ]]}")
        else :
            allocation [cell [0 ]][cell [1 ]]-=min_value 
            print (f"    (S{cell [0 ]+1 },D{cell [1 ]+1 }): {allocation [cell [0 ]][cell [1 ]]+min_value } - {min_value } = {allocation [cell [0 ]][cell [1 ]]}")

    return allocation 

def modi_method (allocation ,cost_matrix ,supply ,demand ):

    m =len (supply )
    n =len (demand )

    print ("\n"+"="*80 )
    print ("APPLYING MODI METHOD (MODIFIED DISTRIBUTION METHOD)")
    print ("="*80 )

    iteration =1 

    while True :
        print (f"\n{'='*80 }")
        print (f"ITERATION {iteration }")
        print ("="*80 )

        print_transportation_table (allocation ,cost_matrix ,supply ,demand ,
        f"Current Allocation (Iteration {iteration })")

        is_degenerate ,num_epsilon =check_degeneracy (allocation ,m ,n )
        if is_degenerate :
            allocation =handle_degeneracy (allocation ,cost_matrix ,m ,n ,num_epsilon )
            print_transportation_table (allocation ,cost_matrix ,supply ,demand ,
            "Allocation after handling degeneracy")

        u ,v =calculate_uv_values (allocation ,cost_matrix ,m ,n )

        opp_costs ,min_i ,min_j ,min_cost =calculate_opportunity_costs (
        allocation ,cost_matrix ,u ,v ,m ,n )

        print (f"\n  Minimum opportunity cost: {min_cost }")
        if min_cost >=0 :
            print (f"  All opportunity costs are non-negative.")
            print (f"\n  OPTIMAL SOLUTION REACHED!")
            break 

        print (f"  Most negative opportunity cost: {min_cost } at cell (S{min_i +1 }, D{min_j +1 })")
        print (f"  This cell will enter the basis.")

        print (f"\nFINDING CLOSED LOOP starting from (S{min_i +1 }, D{min_j +1 }):")
        loop =find_loop (allocation ,min_i ,min_j ,m ,n )

        if not loop :
            print ("  ERROR: Could not find closed loop. Solution may be incorrect.")
            break 

        print_loop (loop )

        print (f"\nADJUSTING ALLOCATIONS:")
        allocation =adjust_allocation (allocation ,loop )

        iteration +=1 

        print ("\n"+"-"*80 )
        input ("Press Enter to continue to next iteration...")

    return allocation 

def solve_transportation_problem ():

    print ("\n"+"="*80 )
    print ("   TRANSPORTATION PROBLEM SOLVER")
    print ("="*80 )

    print ("\nHow would you like to input the problem?")
    print ("1. Manual Input")
    print ("2. Load from problem.txt")

    input_choice =get_int_input ("\nEnter choice (1-2): ")

    if input_choice ==2 :
        problem =parse_transportation_problem ('problem.txt')
        if not problem :
            print ("\nError: Could not parse transportation problem from file.")
            print ("File format:")
            print ("  Row 1-M: cost1 cost2 ... costN supply")
            print ("  Row M+1: demand1 demand2 ... demandN")
            print ("\nExample (3 sources, 4 destinations):")
            print ("  19 30 50 10 7")
            print ("  70 30 40 60 9")
            print ("  40 8 70 20 32")
            print ("  7 9 18 14")
            return 

        m =problem ['sources']
        n =problem ['destinations']
        cost_matrix =problem ['cost_matrix']
        supply =problem ['supply']
        demand =problem ['demand']

        print (f"\nLoaded problem: {m } sources, {n } destinations")
    else :
        m =get_int_input ("\nEnter number of sources (m): ")
        n =get_int_input ("Enter number of destinations (n): ")

        print (f"\nEnter cost matrix ({m }x{n }):")
        cost_matrix =[]
        for i in range (m ):
            row =[]
            print (f"Row {i +1 } (space-separated): ",end ="")
            values =input ().split ()
            for val in values :
                row .append (int (val ))
            cost_matrix .append (row )

        print (f"\nEnter supply for {m } sources (space-separated): ",end ="")
        supply =[int (x )for x in input ().split ()]

        print (f"Enter demand for {n } destinations (space-separated): ",end ="")
        demand =[int (x )for x in input ().split ()]

    total_supply =sum (supply )
    total_demand =sum (demand )

    print (f"\nTotal Supply: {total_supply }")
    print (f"Total Demand: {total_demand }")

    if total_supply !=total_demand :
        print ("\nWARNING: Problem is UNBALANCED!")
        print ("This solver requires balanced problems.")
        print ("You need to add a dummy source or destination.")
        return 

    print ("\nProblem is BALANCED. Proceeding...")

    print ("\n"+"="*80 )
    print ("STEP 1: INITIAL BASIC FEASIBLE SOLUTION")
    print ("="*80 )
    print ("\nChoose method for initial solution:")
    print ("1. Northwest Corner Method")
    print ("2. Least Cost Method")
    print ("3. Vogel's Approximation Method (VAM)")

    method_choice =get_int_input ("\nEnter choice (1-3): ")

    if method_choice ==1 :
        allocation =northwest_corner_method (cost_matrix ,supply ,demand )
    elif method_choice ==2 :
        allocation =least_cost_method (cost_matrix ,supply ,demand )
    elif method_choice ==3 :
        allocation =vogel_approximation_method (cost_matrix ,supply ,demand )
    else :
        print ("Invalid choice. Using Northwest Corner Method.")
        allocation =northwest_corner_method (cost_matrix ,supply ,demand )

    print_transportation_table (allocation ,cost_matrix ,supply ,demand ,
    "\nInitial Basic Feasible Solution")

    input ("\nPress Enter to proceed to optimization using MODI method...")

    final_allocation =modi_method (allocation ,cost_matrix ,supply ,demand )

    print ("\n"+"="*80 )
    print ("FINAL OPTIMAL SOLUTION")
    print ("="*80 )
    print_transportation_table (final_allocation ,cost_matrix ,supply ,demand ,
    "Final Allocation")

    print ("\nDETAILED SHIPPING SCHEDULE:")
    for i in range (m ):
        for j in range (n ):
            if final_allocation [i ][j ]>0 :
                cost =final_allocation [i ][j ]*cost_matrix [i ][j ]
                print (f"  Ship {final_allocation [i ][j ]} units from S{i +1 } to D{j +1 } at cost {cost_matrix [i ][j ]} per unit = {cost }")

def find_objective_coefficient_range (table ,basic_vars ,var_names ,cj ,cb ,var_index ,is_max ):

    print (f"\n{'='*80 }")
    print (f"FINDING RANGE FOR COEFFICIENT OF {var_names [var_index ]}")
    print ('='*80 )

    is_basic =var_names [var_index ]in basic_vars 

    if is_basic :
        print (f"\n{var_names [var_index ]} is a BASIC variable")
        print ("\nFor basic variables, we analyze the Zj-Cj row.")
        print ("The current solution remains optimal as long as all Zj-Cj >= 0")

        basic_row =basic_vars .index (var_names [var_index ])

        current_c =cj [var_index ]
        print (f"\nCurrent coefficient: C{var_index +1 } = {current_c }")

        print (f"\nLet C{var_index +1 } = C (variable coefficient)")
        print (f"\nFor each non-basic variable, we calculate Zj-Cj as a function of C:")

        lower_bound =float ('-inf')
        upper_bound =float ('inf')

        for j in range (len (var_names )):
            if var_names [j ]not in basic_vars :

                coeff_of_c =table [basic_row ][j ]

                constant =0 
                for i ,bv in enumerate (basic_vars ):
                    if i !=basic_row :
                        constant +=cb [i ]*table [i ][j ]

                zj_minus_cj_expr =f"{coeff_of_c :.4g}C + {constant :.4g} - {cj [j ]:.4g}"
                final_constant =constant -cj [j ]

                print (f"\n  {var_names [j ]}: Zj-Cj = {coeff_of_c :.4g}*C + ({final_constant :.4g})")

                if abs (coeff_of_c )>1e-9 :
                    if coeff_of_c >0 :
                        bound =-final_constant /coeff_of_c 
                        print (f"      Constraint: C >= {bound :.4g}")
                        lower_bound =max (lower_bound ,bound )
                    else :
                        bound =-final_constant /coeff_of_c 
                        print (f"      Constraint: C <= {bound :.4g}")
                        upper_bound =min (upper_bound ,bound )
                else :
                    if final_constant <-1e-9 :
                        print (f"      INFEASIBLE: {final_constant :.4g} < 0 (independent of C)")
                        return None ,None 
                    else :
                        print (f"      Always satisfied: {final_constant :.4g} >= 0")

        print (f"\n{'='*80 }")
        print (f"OPTIMAL RANGE FOR C{var_index +1 }:")
        if lower_bound ==float ('-inf')and upper_bound ==float ('inf'):
            print (f"  All real numbers (no restrictions)")
        elif lower_bound ==float ('-inf'):
            print (f"  C{var_index +1 } <= {upper_bound :.4g}")
        elif upper_bound ==float ('inf'):
            print (f"  C{var_index +1 } >= {lower_bound :.4g}")
        else :
            print (f"  {lower_bound :.4g} <= C{var_index +1 } <= {upper_bound :.4g}")
        print ('='*80 )

        return lower_bound ,upper_bound 

    else :
        print (f"\n{var_names [var_index ]} is a NON-BASIC variable (currently 0)")
        print ("\nFor non-basic variables, we check its Zj-Cj value.")
        print ("The solution remains optimal as long as Zj-Cj >= 0")

        zj =0 
        for i ,bv in enumerate (basic_vars ):
            zj +=cb [i ]*table [i ][var_index ]

        current_c =cj [var_index ]
        print (f"\nCurrent coefficient: C{var_index +1 } = {current_c }")
        print (f"Zj (contribution from basic variables) = {zj :.4g}")
        print (f"Current Zj-Cj = {zj :.4g} - {current_c :.4g} = {zj -current_c :.4g}")

        print (f"\nFor optimality: Zj - C{var_index +1 } >= 0")
        print (f"                C{var_index +1 } <= {zj :.4g}")

        lower_bound =float ('-inf')
        upper_bound =zj 

        print (f"\n{'='*80 }")
        print (f"OPTIMAL RANGE FOR C{var_index +1 }:")
        print (f"  C{var_index +1 } <= {upper_bound :.4g}")
        print (f"  (Any value up to {upper_bound :.4g})")
        print ('='*80 )

        return lower_bound ,upper_bound 

def apply_objective_coefficient_change (problem ,table ,basic_vars ,var_names ,cj ,cb ,var_index ,new_value ):

    print (f"\n{'='*80 }")
    print (f"APPLYING COEFFICIENT CHANGE")
    print ('='*80 )

    old_value =cj [var_index ]
    print (f"\nChanging coefficient of {var_names [var_index ]}:")
    print (f"  Old value: {old_value }")
    print (f"  New value: {new_value }")
    print (f"  Change: {new_value -old_value :+.4g}")

    new_cj =cj .copy ()
    new_cj [var_index ]=new_value 

    new_cb =cb .copy ()
    if var_names [var_index ]in basic_vars :
        basic_row =basic_vars .index (var_names [var_index ])
        new_cb [basic_row ]=new_value 
        print (f"\n{var_names [var_index ]} is basic, updating Cb[{basic_row }] = {new_value }")

    print (f"\nRecalculating Zj and Zj-Cj rows...")

    num_vars =len (var_names )
    new_zj =calculate_zj (table ,new_cb ,num_vars )
    new_zj_cj =calculate_zj_cj (new_zj ,new_cj ,None )

    print (f"\n{'='*80 }")
    print ("UPDATED SIMPLEX TABLE")
    print ('='*80 )
    print_simplex_table (table ,basic_vars ,var_names ,new_cj ,new_cb ,iteration =0 )

    still_optimal =check_optimality (new_zj_cj )

    print (f"\n{'='*80 }")
    if still_optimal :
        print ("SOLUTION REMAINS OPTIMAL!")
        print ('='*80 )
        print ("\nAll Zj-Cj values are >= 0")
        print ("The current basis is still optimal with the new coefficient.")

        new_z_value =new_zj [-1 ]
        old_z_value =0 
        for i ,bv in enumerate (basic_vars ):
            old_z_value +=cb [i ]*table [i ][-1 ]

        print (f"\nObjective function value:")
        print (f"  Old Z = {old_z_value :.4g}")
        print (f"  New Z = {new_z_value :.4g}")
        print (f"  Change = {new_z_value -old_z_value :+.4g}")

        return True ,new_cj ,new_cb 
    else :
        print ("SOLUTION BECOMES NON-OPTIMAL!")
        print ('='*80 )
        print ("\nOne or more Zj-Cj values are negative:")
        for j in range (len (var_names )):
            if new_zj_cj [j ]<-1e-9 :
                print (f"  {var_names [j ]}: Zj-Cj = {new_zj_cj [j ]:.4g} < 0")

        print ("\nThe current basis is no longer optimal.")
        print ("Need to continue with Simplex Method to find new optimal solution.")

        input ("\n>>> Press Enter to continue with Simplex Method...")

        return False ,new_cj ,new_cb 

def get_basis_matrix (table ,basic_vars ,var_names ):

    m =len (table )
    n =len (var_names )

    basis_cols =[]
    for bv in basic_vars :
        if bv in var_names :
            basis_cols .append (var_names .index (bv ))

    B =[]
    for i in range (m ):
        row =[]
        for col_idx in basis_cols :
            row .append (table [i ][col_idx ])
        B .append (row )

    return B ,basis_cols 

def matrix_multiply (A ,B ):

    if not A or not B :
        return None 

    rows_A =len (A )
    cols_A =len (A [0 ])
    rows_B =len (B )
    cols_B =len (B [0 ])if isinstance (B [0 ],list )else 1 

    if cols_A !=rows_B :
        return None 

    if not isinstance (B [0 ],list ):
        result =[]
        for i in range (rows_A ):
            val =sum (A [i ][j ]*B [j ]for j in range (cols_A ))
            result .append (val )
        return result 

    result =[[0 for _ in range (cols_B )]for _ in range (rows_A )]
    for i in range (rows_A ):
        for j in range (cols_B ):
            for k in range (cols_A ):
                result [i ][j ]+=A [i ][k ]*B [k ][j ]

    return result 

def matrix_inverse (matrix ):

    n =len (matrix )

    augmented =[]
    for i in range (n ):
        row =matrix [i ][:]+[0 ]*n 
        row [n +i ]=1 
        augmented .append (row )

    for i in range (n ):
        max_row =i 
        for k in range (i +1 ,n ):
            if abs (augmented [k ][i ])>abs (augmented [max_row ][i ]):
                max_row =k 

        augmented [i ],augmented [max_row ]=augmented [max_row ],augmented [i ]

        if abs (augmented [i ][i ])<1e-10 :
            return None 

        pivot =augmented [i ][i ]
        for j in range (2 *n ):
            augmented [i ][j ]/=pivot 

        for k in range (n ):
            if k !=i :
                factor =augmented [k ][i ]
                for j in range (2 *n ):
                    augmented [k ][j ]-=factor *augmented [i ][j ]

    inverse =[]
    for i in range (n ):
        inverse .append (augmented [i ][n :])

    return inverse 

def print_matrix (matrix ,title ="Matrix",precision =4 ):

    print (f"\n{title }:")
    print ("-"*60 )
    for row in matrix :
        row_str ="  ".join ([f"{val :>{precision +6 }.{precision }f}"for val in row ])
        print (f"  [{row_str }]")
    print ("-"*60 )

def calculate_b_inverse (table ,basic_vars ,var_names ,problem ):

    m =len (table )

    slack_cols =[]
    for j ,var_name in enumerate (var_names ):
        if var_name .startswith ('s')or var_name .startswith ('S')or var_name .startswith ('a')or var_name .startswith ('A'):
            slack_cols .append (j )

    if len (slack_cols )>=m :
        B_inv =[]
        for i in range (m ):
            row =[]
            for j in slack_cols [:m ]:
                row .append (table [i ][j ])
            B_inv .append (row )
        return B_inv 

    B ,basis_cols =get_basis_matrix (table ,basic_vars ,var_names )
    return matrix_inverse (B )

def find_rhs_feasibility_range (table ,basic_vars ,var_names ,cj ,cb ,problem ,resource_index ):

    print (f"\n{'='*80 }")
    print (f"FINDING FEASIBILITY RANGE FOR CONSTRAINT {resource_index +1 }")
    print ('='*80 )

    m =len (table )

    if resource_index >=m :
        print (f"\n[!] Error: Constraint index {resource_index +1 } is out of range (1-{m })")
        return None ,None 

    original_b =[problem ['rhs'][i ]for i in range (m )]
    current_b_i =original_b [resource_index ]

    print (f"\nOriginal constraint {resource_index +1 }: b{resource_index +1 } = {current_b_i :.4g}")
    print (f"\nCurrent basic solution (X_B) at optimal:")
    for i ,bv in enumerate (basic_vars ):
        print (f"  {bv } = {table [i ][-1 ]:.4g}")

    B_inv =calculate_b_inverse (table ,basic_vars ,var_names ,problem )

    if B_inv is None :
        print ("\n[!] Error: Could not calculate B inverse")
        return None ,None 

    print_matrix (B_inv ,"B^-1 (Inverse of Basis Matrix)")

    print (f"\nLet b{resource_index +1 } = {current_b_i :.4g} + Δ")
    print (f"\nFor each basic variable, the new value will be:")
    print (f"  X_B(new)[j] = X_B(current)[j] + Δ * B^-1[j][{resource_index }]")

    lower_bound =float ('-inf')
    upper_bound =float ('inf')

    print (f"\nFor feasibility, all X_B(new)[j] >= 0:")
    for j in range (m ):
        current_val =table [j ][-1 ]
        b_inv_coeff =B_inv [j ][resource_index ]

        print (f"\n  {basic_vars [j ]}: {current_val :.4g} + {b_inv_coeff :.4g}*Δ >= 0")

        if abs (b_inv_coeff )<1e-9 :
            if current_val <-1e-9 :
                print (f"      INFEASIBLE: {current_val :.4g} < 0 (independent of Δ)")
                return None ,None 
            else :
                print (f"      Always satisfied")
        else :
            bound_delta =-current_val /b_inv_coeff 

            if b_inv_coeff >0 :
                print (f"      Constraint: Δ >= {bound_delta :.4g}")
                lower_bound =max (lower_bound ,bound_delta )
            else :
                print (f"      Constraint: Δ <= {bound_delta :.4g}")
                upper_bound =min (upper_bound ,bound_delta )

    if lower_bound ==float ('-inf'):
        b_lower =float ('-inf')
    else :
        b_lower =current_b_i +lower_bound 

    if upper_bound ==float ('inf'):
        b_upper =float ('inf')
    else :
        b_upper =current_b_i +upper_bound 

    print (f"\n{'='*80 }")
    print (f"FEASIBILITY RANGE FOR b{resource_index +1 }:")

    if b_lower ==float ('-inf')and b_upper ==float ('inf'):
        print (f"  All real numbers (no restrictions)")
    elif b_lower ==float ('-inf'):
        print (f"  b{resource_index +1 } <= {b_upper :.4g}")
        print (f"  Δ <= {upper_bound :.4g}")
    elif b_upper ==float ('inf'):
        print (f"  b{resource_index +1 } >= {b_lower :.4g}")
        print (f"  Δ >= {lower_bound :.4g}")
    else :
        print (f"  {b_lower :.4g} <= b{resource_index +1 } <= {b_upper :.4g}")
        print (f"  {lower_bound :.4g} <= Δ <= {upper_bound :.4g}")

    print ('='*80 )

    return b_lower ,b_upper 

def apply_rhs_change (problem ,table ,basic_vars ,var_names ,cj ,cb ,resource_index ,new_value ):

    print (f"\n{'='*80 }")
    print (f"APPLYING RHS CHANGE TO CONSTRAINT {resource_index +1 }")
    print ('='*80 )

    m =len (table )

    if resource_index >=m :
        print (f"\n[!] Error: Constraint index {resource_index +1 } is out of range (1-{m })")
        return None ,None ,None 

    original_b =[problem ['rhs'][i ]for i in range (m )]
    old_value =original_b [resource_index ]
    delta =new_value -old_value 

    print (f"\nChanging ORIGINAL constraint {resource_index +1 } RHS:")
    print (f"  Old value: b{resource_index +1 } = {old_value :.4g}")
    print (f"  New value: b{resource_index +1 } = {new_value :.4g}")
    print (f"  Change: Δ = {delta :+.4g}")

    B_inv =calculate_b_inverse (table ,basic_vars ,var_names ,problem )

    if B_inv is None :
        print ("\n[!] Error: Could not calculate B inverse")
        return None ,None ,None 

    print_matrix (B_inv ,"B^-1 (Inverse of Basis Matrix)")

    new_b =original_b [:]
    new_b [resource_index ]=new_value 

    print (f"\nOriginal b vector: {[f'{x :.4g}'for x in original_b ]}")
    print (f"New b vector:      {[f'{x :.4g}'for x in new_b ]}")

    new_xb =matrix_multiply (B_inv ,new_b )

    if new_xb is None :
        print ("\n[!] Error: Matrix multiplication failed")
        return None ,None ,None 

    print (f"\nCalculating NEW X_B = B^-1 x b_new:")
    print (f"\nNEW basic variable values:")

    new_table =[row [:]for row in table ]

    for j in range (m ):
        old_xb =table [j ][-1 ]
        new_table [j ][-1 ]=new_xb [j ]
        print (f"  {basic_vars [j ]}: {old_xb :.4g} -> {new_xb [j ]:.4g} (change: {new_xb [j ]-old_xb :+.4g})")

    problem ['rhs'][resource_index ]=new_value 

    print (f"\n{'='*80 }")
    print ("UPDATED SIMPLEX TABLE")
    print ('='*80 )
    print_simplex_table (new_table ,basic_vars ,var_names ,cj ,cb ,iteration =0 )

    is_feasible =True 
    negative_vars =[]

    print (f"\n{'='*80 }")
    print ("FEASIBILITY CHECK")
    print ('='*80 )

    for j in range (m ):
        if new_table [j ][-1 ]<-1e-9 :
            is_feasible =False 
            negative_vars .append ((basic_vars [j ],new_table [j ][-1 ]))
            print (f"  {basic_vars [j ]} = {new_table [j ][-1 ]:.4g} < 0  [INFEASIBLE]")
        else :
            print (f"  {basic_vars [j ]} = {new_table [j ][-1 ]:.4g} >= 0  [OK]")

    if is_feasible :
        print (f"\n{'='*80 }")
        print ("SOLUTION IS FEASIBLE!")
        print ('='*80 )

        new_z =sum (cb [i ]*new_table [i ][-1 ]for i in range (m ))
        print (f"\nNew objective function value: Z = {new_z :.4g}")

        return new_table ,basic_vars ,cb 

    else :
        print (f"\n{'='*80 }")
        print ("SOLUTION IS INFEASIBLE!")
        print ('='*80 )
        print (f"\nThe following variables are negative:")
        for var ,val in negative_vars :
            print (f"  {var } = {val :.4g}")

        print (f"\nApplying DUAL SIMPLEX METHOD to restore feasibility...")
        input ("\nPress Enter to continue with Dual Simplex...")

        return apply_dual_simplex_to_table (new_table ,basic_vars ,var_names ,cj ,cb ,problem )

def apply_dual_simplex_to_table (table ,basic_vars ,var_names ,cj ,cb ,problem ):

    print (f"\n{'='*80 }")
    print ("DUAL SIMPLEX METHOD")
    print ('='*80 )

    iteration =1 

    while True :
        num_vars =len (var_names )
        zj =calculate_zj (table ,cb ,num_vars )
        zj_cj =calculate_zj_cj (zj ,cj ,None )

        is_feasible ,negative_row ,most_negative =check_dual_feasibility (table )

        if is_feasible :
            print (f"\n{'='*80 }")
            print (f"ITERATION {iteration }")
            print ('='*80 )
            zj_final ,zj_cj_final =print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration )

            print (f"\n{'='*80 }")
            print ("FEASIBLE SOLUTION RESTORED!")
            print ('='*80 )

            z_value =sum (cb [i ]*table [i ][-1 ]for i in range (len (table )))
            print (f"\nObjective function value: Z = {z_value :.4g}")

            return table ,basic_vars ,cb 

        print (f"\n{'='*80 }")
        print (f"ITERATION {iteration }")
        print ('='*80 )
        zj ,zj_cj =print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration )

        print (f"\nLeaving Variable: {basic_vars [negative_row ]} (RHS = {print_fraction (most_negative )})")

        pivot_col ,min_ratio ,ratios =find_dual_pivot_column (table ,negative_row ,zj_cj )

        if pivot_col ==-1 :
            print ("\n"+"!"*80 )
            print ("PROBLEM IS INFEASIBLE!")
            print ("!"*80 )
            print ("\nThe dual simplex method could not find an entering variable.")
            print ("This means the constraints are contradictory and cannot be")
            print ("satisfied simultaneously. No feasible solution exists.")
            return None ,None ,None 

        print ("\nDual Simplex Ratio Test:")
        for j ,element ,zj_cj_val ,ratio in ratios :
            print (f"  {var_names [j ]}: |{print_fraction (zj_cj_val )} / {print_fraction (element )}| = {print_fraction (ratio )}")

        print (f"\nEntering Variable: {var_names [pivot_col ]} (minimum ratio = {print_fraction (min_ratio )})")

        input ("\n>>> Press Enter to perform pivot operation...")

        pivot_row =negative_row 
        table ,basic_vars ,cb =perform_pivot_operation (table ,pivot_row ,pivot_col ,basic_vars ,var_names ,cb ,cj )

        iteration +=1 

def find_shadow_price_via_dual (problem ,table ,basic_vars ,var_names ,cj ,cb ,resource_index ):

    print (f"\n{'='*80 }")
    print (f"FINDING SHADOW PRICE FOR CONSTRAINT {resource_index +1 } VIA DUAL")
    print ('='*80 )

    m =len (table )
    n =problem ['num_vars']

    if resource_index >=m :
        print (f"\n[!] Error: Constraint index {resource_index +1 } is out of range (1-{m })")
        return None 

    print ("\n"+"-"*80 )
    print ("SHADOW PRICE INTERPRETATION:")
    print ("-"*80 )
    print ("The shadow price (dual price) represents the rate of change in the")
    print ("objective function value per unit increase in the resource.")
    print ("Shadow Price = Value of corresponding dual variable at optimum")
    print ("-"*80 )

    print (f"\n{'='*80 }")
    print ("STEP 1: PRIMAL PROBLEM")
    print ('='*80 )

    obj_type ="Maximize"if problem ['is_max']else "Minimize"
    print (f"\n{obj_type } Z = ",end ="")
    terms =[]
    for j in range (n ):
        coeff =problem ['obj_coef'][j ]
        if coeff !=0 :
            terms .append (f"{coeff }x{j +1 }")
    print (" + ".join (terms ))

    print ("\nSubject to:")
    for i in range (m ):
        constraint_str ="  "
        terms =[]
        for j in range (n ):
            coeff =problem ['constraints'][i ][j ]
            if coeff !=0 :
                terms .append (f"{coeff }x{j +1 }")
        constraint_str +=" + ".join (terms )if terms else "0"

        ct =problem ['constraint_types'][i ]
        if ct ==1 :
            constraint_str +=f" <= {problem ['rhs'][i ]}"
        elif ct ==2 :
            constraint_str +=f" = {problem ['rhs'][i ]}"
        else :
            constraint_str +=f" >= {problem ['rhs'][i ]}"
        print (constraint_str )

    print ("  x1, x2, ... >= 0")

    print (f"\n{'='*80 }")
    print ("STEP 2: CONVERT TO DUAL PROBLEM")
    print ('='*80 )

    print ("\nDUAL CONVERSION RULES:")
    if problem ['is_max']:
        print ("  Primal (Max) -> Dual (Min)")
        print ("  • Number of dual variables = Number of primal constraints")
        print ("  • Dual objective coefficients = Primal RHS values")
        print ("  • Dual RHS values = Primal objective coefficients")
        print ("  • Primal <= constraint -> Dual variable >= 0")
        print ("  • Transpose constraint matrix")
        dual_is_max =False 
    else :
        print ("  Primal (Min) -> Dual (Max)")
        print ("  • Number of dual variables = Number of primal constraints")
        print ("  • Dual objective coefficients = Primal RHS values")
        print ("  • Dual RHS values = Primal objective coefficients")
        print ("  • Primal >= constraint -> Dual variable >= 0")
        print ("  • Transpose constraint matrix")
        dual_is_max =True 

    print (f"\n{'='*80 }")
    print ("STEP 3: DUAL PROBLEM FORMULATION")
    print ('='*80 )

    dual_obj_type ="Minimize"if problem ['is_max']else "Maximize"
    print (f"\n{dual_obj_type } W = ",end ="")
    terms =[]
    for i in range (m ):
        coeff =problem ['rhs'][i ]
        if coeff !=0 :
            terms .append (f"{coeff }y{i +1 }")
    print (" + ".join (terms ))

    print ("\nSubject to:")
    for j in range (n ):
        constraint_str ="  "
        terms =[]
        for i in range (m ):
            coeff =problem ['constraints'][i ][j ]
            if coeff !=0 :
                terms .append (f"{coeff }y{i +1 }")
        constraint_str +=" + ".join (terms )if terms else "0"

        if problem ['is_max']:
            constraint_str +=f" >= {problem ['obj_coef'][j ]}"
        else :
            constraint_str +=f" <= {problem ['obj_coef'][j ]}"
        print (constraint_str )

    print ("  y1, y2, ... >= 0")

    print (f"\n{'='*80 }")
    print ("STEP 4: FINDING SHADOW PRICES FROM OPTIMAL TABLEAU")
    print ('='*80 )

    print ("\nBy DUALITY THEOREM:")
    print ("  At optimality, Shadow Price of constraint i = Zj of slack variable si")
    print ("  (This is the value of dual variable yi)")

    shadow_prices =[]
    print (f"\n{'Constraint':<12} {'Slack Var':<12} {'Zj Value':<12} {'Shadow Price':<12}")
    print ("-"*48 )

    for i in range (m ):
        slack_var =f"s{i +1 }"
        if slack_var in var_names :
            slack_col =var_names .index (slack_var )
            zj_slack =sum (cb [j ]*table [j ][slack_col ]for j in range (m ))

            if slack_var in basic_vars :
                slack_row =basic_vars .index (slack_var )
                slack_value =table [slack_row ][-1 ]
            else :
                slack_value =0 

            if slack_value >1e-9 :
                shadow_price =0 
            else :
                shadow_price =zj_slack if problem ['is_max']else -zj_slack 

            shadow_prices .append (shadow_price )
            print (f"Constraint {i +1 :<3} s{i +1 :<11} {zj_slack :<12.4g} {shadow_price :<12.4g}")
        else :
            shadow_prices .append (0 )
            print (f"Constraint {i +1 :<3} {'N/A':<11} {'N/A':<12} {0 :<12.4g}")

    print (f"\n{'='*80 }")
    print ("STEP 5: VERIFICATION - COMPLEMENTARY SLACKNESS")
    print ('='*80 )

    print ("\nComplementary Slackness Conditions:")
    print ("  • If primal slack > 0, then dual variable = 0")
    print ("  • If dual variable > 0, then primal constraint is binding (slack = 0)")

    print ("\nVerification:")
    for i in range (m ):
        slack_var =f"s{i +1 }"
        if slack_var in basic_vars :
            slack_row =basic_vars .index (slack_var )
            slack_value =table [slack_row ][-1 ]
        elif slack_var in var_names :
            slack_value =0 
        else :
            slack_value ="N/A"

        if isinstance (slack_value ,str ):
            print (f"  Constraint {i +1 }: Slack = {slack_value }, Shadow Price = {shadow_prices [i ]:.4g}")
        elif slack_value >1e-9 :
            print (f"  Constraint {i +1 }: Slack = {slack_value :.4g} > 0 => Shadow Price = 0 OK")
        else :
            print (f"  Constraint {i +1 }: Slack = 0 (Binding) => Shadow Price = {shadow_prices [i ]:.4g}")

    print (f"\n{'='*80 }")
    print (f"RESULT: SHADOW PRICE FOR CONSTRAINT {resource_index +1 }")
    print ('='*80 )

    shadow_price =shadow_prices [resource_index ]
    print (f"\n  Shadow Price (y{resource_index +1 }) = {shadow_price :.4g}")

    print (f"\n  INTERPRETATION:")
    if shadow_price ==0 :
        print (f"  • Constraint {resource_index +1 } is NON-BINDING (has slack)")
        print (f"  • Increasing RHS will NOT change optimal Z")
    elif shadow_price >0 :
        print (f"  • Constraint {resource_index +1 } is BINDING")
        print (f"  • For each unit increase in RHS, Z increases by {shadow_price :.4g}")
    else :
        print (f"  • Constraint {resource_index +1 } is BINDING")
        print (f"  • For each unit increase in RHS, Z decreases by {abs (shadow_price ):.4g}")

    print (f"\n{'='*80 }")
    print (f"STEP 6: FEASIBILITY RANGE FOR CONSTRAINT {resource_index +1 }")
    print ('='*80 )

    find_rhs_feasibility_range (table ,basic_vars ,var_names ,cj ,cb ,problem ,resource_index )

    return shadow_price 

def apply_multiple_rhs_changes (problem ,table ,basic_vars ,var_names ,cj ,cb ,new_b_vector ):

    print (f"\n{'='*80 }")
    print (f"APPLYING MULTIPLE RHS CHANGES")
    print ('='*80 )

    m =len (table )

    if len (new_b_vector )!=m :
        print (f"\n[!] Error: Expected {m } values, got {len (new_b_vector )}")
        return None ,None ,None 

    original_b =[problem ['rhs'][i ]for i in range (m )]

    print (f"\nChanging ALL constraint RHS values:")
    print (f"\n{'Constraint':<12} {'Old Value':<12} {'New Value':<12} {'Change':<12}")
    print ("-"*48 )

    all_same =True 
    for i in range (m ):
        delta =new_b_vector [i ]-original_b [i ]
        if abs (delta )>1e-9 :
            all_same =False 
        print (f"b{i +1 :<11} {original_b [i ]:<12.4g} {new_b_vector [i ]:<12.4g} {delta :<+12.4g}")

    if all_same :
        print ("\n[!] No changes detected - all values are the same!")
        return table ,basic_vars ,cb 

    B_inv =calculate_b_inverse (table ,basic_vars ,var_names ,problem )

    if B_inv is None :
        print ("\n[!] Error: Could not calculate B inverse")
        return None ,None ,None 

    print_matrix (B_inv ,"B^-1 (Inverse of Basis Matrix)")

    print (f"\nOriginal b vector: {[f'{x :.4g}'for x in original_b ]}")
    print (f"New b vector:      {[f'{x :.4g}'for x in new_b_vector ]}")

    new_xb =matrix_multiply (B_inv ,new_b_vector )

    if new_xb is None :
        print ("\n[!] Error: Matrix multiplication failed")
        return None ,None ,None 

    print (f"\nCalculating NEW X_B = B^-1 x b_new:")
    print (f"\n{'Basic Var':<12} {'Old Value':<12} {'New Value':<12} {'Change':<12}")
    print ("-"*48 )

    new_table =[row [:]for row in table ]

    for j in range (m ):
        old_xb =table [j ][-1 ]
        new_table [j ][-1 ]=new_xb [j ]
        print (f"{basic_vars [j ]:<12} {old_xb :<12.4g} {new_xb [j ]:<12.4g} {new_xb [j ]-old_xb :<+12.4g}")

    for i in range (m ):
        problem ['rhs'][i ]=new_b_vector [i ]

    print (f"\n{'='*80 }")
    print ("UPDATED SIMPLEX TABLE")
    print ('='*80 )
    print_simplex_table (new_table ,basic_vars ,var_names ,cj ,cb ,iteration =0 )

    is_feasible =True 
    negative_vars =[]

    print (f"\n{'='*80 }")
    print ("FEASIBILITY CHECK")
    print ('='*80 )

    for j in range (m ):
        if new_table [j ][-1 ]<-1e-9 :
            is_feasible =False 
            negative_vars .append ((basic_vars [j ],new_table [j ][-1 ]))
            print (f"  {basic_vars [j ]} = {new_table [j ][-1 ]:.4g} < 0  [INFEASIBLE]")
        else :
            print (f"  {basic_vars [j ]} = {new_table [j ][-1 ]:.4g} >= 0  [OK]")

    if is_feasible :
        print (f"\n{'='*80 }")
        print ("SOLUTION IS FEASIBLE!")
        print ('='*80 )

        new_z =sum (cb [i ]*new_table [i ][-1 ]for i in range (m ))
        old_z =sum (cb [i ]*table [i ][-1 ]for i in range (m ))
        print (f"\nObjective function value:")
        print (f"  Old Z = {old_z :.4g}")
        print (f"  New Z = {new_z :.4g}")
        print (f"  Change = {new_z -old_z :+.4g}")

        return new_table ,basic_vars ,cb 

    else :
        print (f"\n{'='*80 }")
        print ("SOLUTION IS INFEASIBLE!")
        print ('='*80 )
        print (f"\nThe following variables are negative:")
        for var ,val in negative_vars :
            print (f"  {var } = {val :.4g}")

        print (f"\nApplying DUAL SIMPLEX METHOD to restore feasibility...")
        input ("\nPress Enter to continue with Dual Simplex...")

        return apply_dual_simplex_to_table (new_table ,basic_vars ,var_names ,cj ,cb ,problem )

def sensitivity_analysis_case2_menu (problem ,table ,basic_vars ,var_names ,cj ,cb ):

    print ("\n"+"="*80 )
    print ("CASE 2: CHANGE IN RHS (RESOURCES/CONSTRAINTS)")
    print ("="*80 )

    print ("\nOptions:")
    print ("1. Change a single constraint RHS value")
    print ("2. Change multiple constraint RHS values")
    print ("3. Find feasibility range for a constraint")
    print ("4. Find shadow price of a constraint")
    print ("5. Find ranges for all constraints")
    print ("6. Find shadow prices for all constraints")
    print ("7. Back to main menu")

    option =get_int_input ("\nEnter choice (1-7): ")

    if option ==7 :
        return table ,basic_vars ,cb 

    m =len (table )

    if option ==1 :
        print (f"\nOriginal problem constraints: 1 to {m }")
        print ("\nCurrent original RHS values (b vector):")
        for i in range (m ):
            print (f"  b{i +1 } = {problem ['rhs'][i ]:.4g}")

        resource_choice =get_int_input (f"\nWhich constraint to change (1-{m }): ")

        if 1 <=resource_choice <=m :
            idx =resource_choice -1 
            print (f"\nCurrent ORIGINAL RHS: b{resource_choice } = {problem ['rhs'][idx ]:.4g}")
            new_value =get_float_input (f"Enter new value for b{resource_choice }: ")

            result =apply_rhs_change (problem ,table ,basic_vars ,var_names ,cj ,cb ,idx ,new_value )

            if result [0 ]is not None :
                table ,basic_vars ,cb =result 
                print ("\n[OK] Constraint RHS value changed successfully!")
            else :
                print ("\n[!] Could not change constraint RHS value")
        else :
            print ("Invalid constraint choice.")

    elif option ==2 :
        print (f"\n{'='*80 }")
        print ("CHANGE MULTIPLE CONSTRAINT RHS VALUES")
        print ('='*80 )

        print (f"\nOriginal problem has {m } constraints")
        print ("\nCurrent original RHS values (b vector):")
        for i in range (m ):
            print (f"  b{i +1 } = {problem ['rhs'][i ]:.4g}")

        print (f"\nEnter new values for all {m } constraints:")
        new_b_vector =[]
        for i in range (m ):
            new_val =get_float_input (f"  Enter new b{i +1 }: ")
            new_b_vector .append (new_val )

        result =apply_multiple_rhs_changes (problem ,table ,basic_vars ,var_names ,cj ,cb ,new_b_vector )

        if result [0 ]is not None :
            table ,basic_vars ,cb =result 
            print ("\n[OK] Multiple constraint RHS values changed successfully!")
        else :
            print ("\n[!] Could not change constraint RHS values")

    elif option ==3 :
        print (f"\nOriginal problem constraints: 1 to {m }")
        resource_choice =get_int_input (f"\nWhich constraint (1-{m }): ")

        if 1 <=resource_choice <=m :
            find_rhs_feasibility_range (table ,basic_vars ,var_names ,cj ,cb ,problem ,resource_choice -1 )
        else :
            print ("Invalid constraint choice.")

    elif option ==4 :
        print (f"\nOriginal problem constraints: 1 to {m }")
        resource_choice =get_int_input (f"\nWhich constraint (1-{m }): ")

        if 1 <=resource_choice <=m :
            find_shadow_price_via_dual (problem ,table ,basic_vars ,var_names ,cj ,cb ,resource_choice -1 )
        else :
            print ("Invalid constraint choice.")

    elif option ==5 :
        print ("\n"+"="*80 )
        print ("FINDING FEASIBILITY RANGES FOR ALL CONSTRAINTS")
        print ("="*80 )

        for i in range (m ):
            input (f"\nPress Enter to find range for constraint {i +1 }...")
            find_rhs_feasibility_range (table ,basic_vars ,var_names ,cj ,cb ,problem ,i )

    elif option ==6 :
        print ("\n"+"="*80 )
        print ("FINDING SHADOW PRICES FOR ALL CONSTRAINTS")
        print ("="*80 )

        for i in range (m ):
            input (f"\nPress Enter to find shadow price for constraint {i +1 }...")
            find_shadow_price_via_dual (problem ,table ,basic_vars ,var_names ,cj ,cb ,i )

    else :
        print ("Invalid option.")

    return table ,basic_vars ,cb 

def sensitivity_case3_change_nonbasic_column (problem ,table ,basic_vars ,var_names ,cj ,cb ,var_index ,new_column ):

    print (f"\n{'='*80 }")
    print (f"CASE 3a: CHANGE IN NON-BASIC VARIABLE COLUMN ({var_names [var_index ]})")
    print ('='*80 )

    m =len (table )
    n =len (var_names )

    print (f"\nVariable {var_names [var_index ]} is NON-BASIC (value = 0)")
    print ("Since B^-1 doesn't change, only this column needs to be updated.")

    B_inv =calculate_b_inverse (table ,basic_vars ,var_names ,problem )

    if B_inv is None :
        print ("\n[!] Error: Could not calculate B inverse")
        return None ,None ,None ,None 

    print_matrix (B_inv ,"B^-1 (Inverse of Basis Matrix)")

    old_column =[table [i ][var_index ]for i in range (m )]
    print (f"\nOld column for {var_names [var_index ]} in tableau:")
    for i in range (m ):
        print (f"  Row {i +1 }: {old_column [i ]:.4g}")

    print (f"\nNew original A column for {var_names [var_index ]}:")
    for i in range (m ):
        print (f"  a{i +1 }{var_index +1 } = {new_column [i ]:.4g}")

    print (f"\n{'='*80 }")
    print ("CALCULATING NEW COLUMN = B^-1 x A_new")
    print ('='*80 )

    new_tableau_column =matrix_multiply (B_inv ,new_column )

    print (f"\nNew tableau column for {var_names [var_index ]}:")
    for i in range (m ):
        print (f"  Row {i +1 }: {new_tableau_column [i ]:.4g}")

    for i in range (m ):
        problem ['constraints'][i ][var_index ]=new_column [i ]

    new_table =[row [:]for row in table ]
    for i in range (m ):
        new_table [i ][var_index ]=new_tableau_column [i ]

    old_zj =sum (cb [i ]*old_column [i ]for i in range (m ))
    new_zj =sum (cb [i ]*new_tableau_column [i ]for i in range (m ))
    old_zj_cj =old_zj -cj [var_index ]
    new_zj_cj =new_zj -cj [var_index ]

    print (f"\n{'='*80 }")
    print ("CALCULATING NEW Zj-Cj")
    print ('='*80 )
    print (f"\nOld Zj for {var_names [var_index ]}: {old_zj :.4g}")
    print (f"New Zj for {var_names [var_index ]}: {new_zj :.4g}")
    print (f"Cj for {var_names [var_index ]}: {cj [var_index ]:.4g}")
    print (f"\nOld Zj-Cj: {old_zj_cj :.4g}")
    print (f"New Zj-Cj: {new_zj_cj :.4g}")

    print (f"\n{'='*80 }")
    print ("UPDATED SIMPLEX TABLE")
    print ('='*80 )
    print_simplex_table (new_table ,basic_vars ,var_names ,cj ,cb ,iteration =0 )

    print (f"\n{'='*80 }")
    print ("OPTIMALITY CHECK")
    print ('='*80 )

    all_zj_cj =[]
    for j in range (n ):
        zj_j =sum (cb [i ]*new_table [i ][j ]for i in range (m ))
        all_zj_cj .append (zj_j -cj [j ])

    is_optimal =all (val >=-1e-9 for val in all_zj_cj )

    if is_optimal :
        print (f"\nAll Zj-Cj >= 0")
        print ("SOLUTION REMAINS OPTIMAL!")

        profit =sum (cb [i ]*new_table [i ][-1 ]for i in range (m ))
        print (f"\nOptimal Value Z = {profit :.4g}")

        return new_table ,basic_vars ,cj ,cb 
    else :
        print (f"\nZj-Cj for {var_names [var_index ]} = {new_zj_cj :.4g} < 0")
        print ("SOLUTION IS NO LONGER OPTIMAL!")
        print ("\nApplying Simplex Method to restore optimality...")

        input ("\nPress Enter to continue with Simplex...")

        return continue_simplex_for_sensitivity (new_table ,basic_vars ,var_names ,cj ,cb ,problem )

def sensitivity_case3_change_basic_column (problem ,table ,basic_vars ,var_names ,cj ,cb ,var_index ,new_column ):

    print (f"\n{'='*80 }")
    print (f"CASE 3b: CHANGE IN BASIC VARIABLE COLUMN ({var_names [var_index ]})")
    print ('='*80 )

    m =len (table )
    n =len (var_names )

    print (f"\nVariable {var_names [var_index ]} is BASIC")
    print ("Since this column is part of basis B, B^-1 changes!")
    print ("Almost entire tableau needs recalculation.")

    basic_row =basic_vars .index (var_names [var_index ])
    print (f"\n{var_names [var_index ]} is in row {basic_row +1 } of the basis")

    print (f"\nUpdating constraint matrix with new column for {var_names [var_index ]}:")
    print (f"Old column: {[problem ['constraints'][i ][var_index ]for i in range (m )]}")
    print (f"New column: {new_column }")

    for i in range (m ):
        problem ['constraints'][i ][var_index ]=new_column [i ]

    print (f"\n{'='*80 }")
    print ("STEP 1: BUILD NEW BASIS MATRIX B")
    print ('='*80 )

    print ("\nExtracting basis columns from updated constraint matrix:")
    B =[]
    basis_col_indices =[]
    for bv in basic_vars :
        if bv in var_names :
            col_idx =var_names .index (bv )
            basis_col_indices .append (col_idx )
            print (f"  {bv } -> column {col_idx +1 } (x{col_idx +1 })")

    for i in range (m ):
        row =[]
        for col_idx in basis_col_indices :
            if col_idx <problem ['num_vars']:
                row .append (problem ['constraints'][i ][col_idx ])
            else :
                slack_idx =col_idx -problem ['num_vars']
                if i ==slack_idx :
                    row .append (1.0 )
                else :
                    row .append (0.0 )
        B .append (row )

    print ("\nNew Basis Matrix B:")
    print_matrix (B ,"B (New Basis Matrix)")

    print (f"\n{'='*80 }")
    print ("STEP 2: CALCULATE NEW B^-1")
    print ('='*80 )

    B_inv_new =matrix_inverse (B )

    if B_inv_new is None :
        print (f"\n[!] ERROR: New basis matrix is singular!")
        print (f"    The new column cannot form a valid basis.")
        return None ,None ,None ,None 

    print_matrix (B_inv_new ,"B^-1 (New Inverse of Basis Matrix)")

    print (f"\n{'='*80 }")
    print ("STEP 3: RECALCULATE ENTIRE TABLEAU")
    print ('='*80 )
    print ("\nUsing formula: Tableau column j = B^-1 × A_j")
    print ("             RHS (X_B) = B^-1 × b")

    new_table =[[0.0 for _ in range (n +1 )]for _ in range (m )]

    print ("\nRecalculating each column:")
    for j in range (n ):
        if j <problem ['num_vars']:
            A_j =[problem ['constraints'][i ][j ]for i in range (m )]
        else :
            slack_idx =j -problem ['num_vars']
            A_j =[1.0 if i ==slack_idx else 0.0 for i in range (m )]

        tableau_col =matrix_multiply (B_inv_new ,A_j )

        print (f"  Column {j +1 } ({var_names [j ]}): ", end ="")
        if j in basis_col_indices and var_names [j ]in basic_vars :
            print ("[BASIC - should be unit vector]")
        else :
            print ("[NON-BASIC]")

        for i in range (m ):
            new_table [i ][j ]=tableau_col [i ]

    print ("\nRecalculating RHS (X_B = B^-1 × b):")
    b =[problem ['rhs'][i ]for i in range (m )]
    X_B =matrix_multiply (B_inv_new ,b )

    for i in range (m ):
        new_table [i ][-1 ]=X_B [i ]
        print (f"  {basic_vars [i ]} = {X_B [i ]:.4g}")

    print (f"\n{'='*80 }")
    print ("UPDATED SIMPLEX TABLE")
    print ('='*80 )
    print_simplex_table (new_table ,basic_vars ,var_names ,cj ,cb ,iteration =0 )

    print (f"\n{'='*80 }")
    print ("FEASIBILITY CHECK")
    print ('='*80 )

    is_feasible =True 
    for i in range (m ):
        if new_table [i ][-1 ]<-1e-9 :
            is_feasible =False 
            print (f"  {basic_vars [i ]} = {new_table [i ][-1 ]:.4g} < 0  [INFEASIBLE]")
        else :
            print (f"  {basic_vars [i ]} = {new_table [i ][-1 ]:.4g} >= 0  [OK]")

    if not is_feasible :
        print ("\nSOLUTION IS INFEASIBLE! Applying Dual Simplex...")
        input ("\nPress Enter to continue with Dual Simplex...")
        return apply_dual_simplex_to_table (new_table ,basic_vars ,var_names ,cj ,cb ,problem )

    print (f"\n{'='*80 }")
    print ("OPTIMALITY CHECK")
    print ('='*80 )

    all_zj_cj =[]
    for j in range (n ):
        zj_j =sum (cb [i ]*new_table [i ][j ]for i in range (m ))
        all_zj_cj .append (zj_j -cj [j ])

    is_optimal =all (val >=-1e-9 for val in all_zj_cj )

    if is_optimal :
        print (f"\nAll Zj-Cj >= 0")
        print ("SOLUTION IS OPTIMAL!")

        profit =sum (cb [i ]*new_table [i ][-1 ]for i in range (m ))
        print (f"\nOptimal Value Z = {profit :.4g}")

        return new_table ,basic_vars ,cj ,cb 
    else :
        print ("\nSome Zj-Cj < 0, SOLUTION IS NOT OPTIMAL!")
        print ("Applying Simplex Method to restore optimality...")

        input ("\nPress Enter to continue with Simplex...")
        return continue_simplex_for_sensitivity (new_table ,basic_vars ,var_names ,cj ,cb ,problem )

def sensitivity_case3_change_all_coefficients (problem ,table ,basic_vars ,var_names ,cj ,cb ,new_A_matrix ):

    print (f"\n{'='*80 }")
    print ("CASE 3: CHANGE IN MULTIPLE COEFFICIENTS OF A MATRIX")
    print ('='*80 )

    m =len (table )
    n =problem ['num_vars']

    print ("\nOriginal A matrix:")
    for i in range (m ):
        row_str ="  ["
        for j in range (n ):
            row_str +=f"{problem ['constraints'][i ][j ]:8.4g}"
        row_str +=" ]"
        print (row_str )

    print ("\nNew A matrix:")
    for i in range (m ):
        row_str ="  ["
        for j in range (n ):
            row_str +=f"{new_A_matrix [i ][j ]:8.4g}"
        row_str +=" ]"
        print (row_str )

    old_B_inv =calculate_b_inverse (table ,basic_vars ,var_names ,problem )

    if old_B_inv is None :
        print ("\n[!] Error: Could not calculate B inverse")
        return None ,None ,None ,None 

    print_matrix (old_B_inv ,"B^-1 (From Current Optimal Table)")

    for i in range (m ):
        for j in range (n ):
            problem ['constraints'][i ][j ]=new_A_matrix [i ][j ]

    basic_changed =False 
    for bv in basic_vars :
        if bv in var_names :
            idx =var_names .index (bv )
            if idx <n :
                basic_changed =True 
                break 

    if basic_changed :
        print ("\n[!] One or more BASIC variable columns changed!")
        print ("    Need to re-solve the problem or use advanced update methods.")
        print ("\n    For simplicity, we'll recalculate using B^-1 x A_new")

    print (f"\n{'='*80 }")
    print ("RECALCULATING TABLEAU COLUMNS")
    print ('='*80 )

    new_table =[row [:]for row in table ]

    for j in range (n ):
        new_A_col =[new_A_matrix [i ][j ]for i in range (m )]

        new_tableau_col =matrix_multiply (old_B_inv ,new_A_col )

        print (f"\nColumn {var_names [j ]}:")
        print (f"  A_new: {[f'{x :.4g}'for x in new_A_col ]}")
        print (f"  B^-1 x A_new: {[f'{x :.4g}'for x in new_tableau_col ]}")

        for i in range (m ):
            new_table [i ][j ]=new_tableau_col [i ]

    print (f"\n{'='*80 }")
    print ("UPDATED SIMPLEX TABLE")
    print ('='*80 )
    print_simplex_table (new_table ,basic_vars ,var_names ,cj ,cb ,iteration =0 )

    print (f"\n{'='*80 }")
    print ("FEASIBILITY CHECK")
    print ('='*80 )

    is_feasible =True 
    for i in range (m ):
        if new_table [i ][-1 ]<-1e-9 :
            is_feasible =False 
            print (f"  {basic_vars [i ]} = {new_table [i ][-1 ]:.4g} < 0  [INFEASIBLE]")
        else :
            print (f"  {basic_vars [i ]} = {new_table [i ][-1 ]:.4g} >= 0  [OK]")

    if not is_feasible :
        print ("\nSOLUTION IS INFEASIBLE! Applying Dual Simplex...")
        input ("\nPress Enter to continue with Dual Simplex...")
        return apply_dual_simplex_to_table (new_table ,basic_vars ,var_names ,cj ,cb ,problem )

    print (f"\n{'='*80 }")
    print ("OPTIMALITY CHECK")
    print ('='*80 )

    num_vars =len (var_names )
    all_zj_cj =[]
    for j in range (num_vars ):
        zj_j =sum (cb [i ]*new_table [i ][j ]for i in range (m ))
        all_zj_cj .append (zj_j -cj [j ])
        if all_zj_cj [-1 ]<-1e-9 :
            print (f"  {var_names [j ]}: Zj-Cj = {all_zj_cj [-1 ]:.4g} < 0")

    is_optimal =all (val >=-1e-9 for val in all_zj_cj )

    if is_optimal :
        print (f"\nAll Zj-Cj >= 0")
        print ("SOLUTION IS OPTIMAL!")

        profit =sum (cb [i ]*new_table [i ][-1 ]for i in range (m ))
        print (f"\nOptimal Value Z = {profit :.4g}")

        return new_table ,basic_vars ,cj ,cb 
    else :
        print ("\nSome Zj-Cj < 0, SOLUTION IS NOT OPTIMAL!")
        print ("Applying Simplex Method to restore optimality...")

        input ("\nPress Enter to continue with Simplex...")
        return continue_simplex_for_sensitivity (new_table ,basic_vars ,var_names ,cj ,cb ,problem )

def continue_simplex_for_sensitivity (table ,basic_vars ,var_names ,cj ,cb ,problem ):

    print (f"\n{'='*80 }")
    print ("CONTINUING SIMPLEX METHOD")
    print ('='*80 )

    m =len (table )
    n =len (var_names )
    iteration =1 

    while True :
        zj =[sum (cb [i ]*table [i ][j ]for i in range (m ))for j in range (n )]
        zj_cj =[zj [j ]-cj [j ]for j in range (n )]

        if all (val >=-1e-9 for val in zj_cj ):
            print (f"\n{'='*80 }")
            print (f"ITERATION {iteration } - OPTIMAL SOLUTION FOUND")
            print ('='*80 )
            print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration )

            profit =sum (cb [i ]*table [i ][-1 ]for i in range (m ))
            print (f"\nOptimal Value Z = {profit :.4g}")

            print ("\nOptimal Solution:")
            for i ,bv in enumerate (basic_vars ):
                print (f"  {bv } = {table [i ][-1 ]:.4g}")

            return table ,basic_vars ,cj ,cb 

        print (f"\n{'='*80 }")
        print (f"ITERATION {iteration }")
        print ('='*80 )

        min_zj_cj =min (zj_cj )
        pivot_col =zj_cj .index (min_zj_cj )

        print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration ,pivot_col =pivot_col )

        print (f"\nEntering Variable: {var_names [pivot_col ]} (Zj-Cj = {min_zj_cj :.4g})")

        ratios =[]
        min_ratio =float ('inf')
        pivot_row =-1 

        for i in range (m ):
            if table [i ][pivot_col ]>1e-9 :
                ratio =table [i ][-1 ]/table [i ][pivot_col ]
                ratios .append ((i ,ratio ))
                if ratio <min_ratio :
                    min_ratio =ratio 
                    pivot_row =i 

        if pivot_row ==-1 :
            print ("\n[!] Problem is unbounded!")
            return None ,None ,None ,None 

        print (f"Leaving Variable: {basic_vars [pivot_row ]} (ratio = {min_ratio :.4g})")

        input ("\n>>> Press Enter to perform pivot operation...")

        table ,basic_vars ,cb =perform_pivot_operation (table ,pivot_row ,pivot_col ,basic_vars ,var_names ,cb ,cj )

        iteration +=1 

        if iteration >50 :
            print ("\n[!] Maximum iterations reached")
            break 

    return table ,basic_vars ,cj ,cb 

def sensitivity_analysis_case3_menu (problem ,table ,basic_vars ,var_names ,cj ,cb ):

    print ("\n"+"="*80 )
    print ("CASE 3: CHANGE IN COEFFICIENT MATRIX A")
    print ("="*80 )

    m =len (table )
    n =problem ['num_vars']

    print ("\nCurrent A matrix (original constraint coefficients):")
    for i in range (m ):
        row_str =f"  Constraint {i +1 }: ["
        for j in range (n ):
            row_str +=f"{problem ['constraints'][i ][j ]:8.4g}"
        row_str +=" ]"
        print (row_str )

    print ("\nOptions:")
    print ("1. Change a single column (one variable's coefficients)")
    print ("2. Change entire A matrix (all coefficients)")
    print ("3. Back to main menu")

    option =get_int_input ("\nEnter choice (1-3): ")

    if option ==3 :
        return table ,basic_vars ,cj ,cb 

    if option ==1 :
        print (f"\nAvailable variables: {', '.join ([f'{j +1 }. {var_names [j ]}'for j in range (n )])}")
        var_choice =get_int_input (f"\nWhich variable's column to change (1-{n }): ")

        if 1 <=var_choice <=n :
            var_idx =var_choice -1 

            print (f"\nCurrent column for {var_names [var_idx ]}:")
            for i in range (m ):
                print (f"  a{i +1 }{var_idx +1 } = {problem ['constraints'][i ][var_idx ]:.4g}")

            print (f"\nEnter new coefficients for {var_names [var_idx ]}:")
            new_column =[]
            for i in range (m ):
                val =get_float_input (f"  Enter new a{i +1 }{var_idx +1 }: ")
                new_column .append (val )

            is_basic =var_names [var_idx ]in basic_vars 

            if is_basic :
                result =sensitivity_case3_change_basic_column (
                problem ,table ,basic_vars ,var_names ,cj ,cb ,var_idx ,new_column )
            else :
                result =sensitivity_case3_change_nonbasic_column (
                problem ,table ,basic_vars ,var_names ,cj ,cb ,var_idx ,new_column )

            if result [0 ]is not None :
                table ,basic_vars ,cj ,cb =result 
                print ("\n[OK] Coefficient change applied successfully!")
            else :
                print ("\n[!] Could not apply coefficient change")
        else :
            print ("Invalid variable choice.")

    elif option ==2 :
        print (f"\nEnter new A matrix ({m } rows x {n } columns):")
        new_A_matrix =[]
        for i in range (m ):
            print (f"\nConstraint {i +1 }:")
            row =[]
            for j in range (n ):
                val =get_float_input (f"  Enter new a{i +1 }{j +1 }: ")
                row .append (val )
            new_A_matrix .append (row )

        result =sensitivity_case3_change_all_coefficients (
        problem ,table ,basic_vars ,var_names ,cj ,cb ,new_A_matrix )

        if result [0 ]is not None :
            table ,basic_vars ,cj ,cb =result 
            print ("\n[OK] All coefficients changed successfully!")
        else :
            print ("\n[!] Could not apply coefficient changes")

    return table ,basic_vars ,cj ,cb 

def sensitivity_case4_add_variable (problem ,table ,basic_vars ,var_names ,cj ,cb ,new_var_coeff ,new_var_obj ):

    print (f"\n{'='*80 }")
    print ("CASE 4: ADDITION OF A NEW VARIABLE")
    print ('='*80 )

    m =len (table )
    n =len (var_names )
    original_n =problem ['num_vars']

    new_var_name =f"x{original_n +1 }"

    print (f"\nAdding new variable: {new_var_name }")
    print (f"Objective coefficient: c{original_n +1 } = {new_var_obj }")
    print (f"Constraint coefficients: {new_var_coeff }")

    B_inv =calculate_b_inverse (table ,basic_vars ,var_names ,problem )

    if B_inv is None :
        print ("\n[!] Error: Could not calculate B inverse")
        return None ,None ,None ,None ,None 

    print_matrix (B_inv ,"B^-1 (From Current Optimal Table)")

    print (f"\n{'='*80 }")
    print (f"CALCULATING NEW COLUMN FOR {new_var_name }")
    print ('='*80 )

    print (f"\nNew column = B^-1 x A_{new_var_name }")

    new_tableau_column =matrix_multiply (B_inv ,new_var_coeff )

    print (f"\nOriginal A column for {new_var_name }: {[f'{x :.4g}'for x in new_var_coeff ]}")
    print (f"New tableau column: {[f'{x :.4g}'for x in new_tableau_column ]}")

    zj_new =sum (cb [i ]*new_tableau_column [i ]for i in range (m ))
    zj_cj_new =zj_new -new_var_obj 

    print (f"\n{'='*80 }")
    print (f"CALCULATING Zj-Cj FOR {new_var_name }")
    print ('='*80 )
    print (f"\nZj = Σ(Cb x column) = ",end ="")
    terms =[f"({cb [i ]:.4g} x {new_tableau_column [i ]:.4g})"for i in range (m )]
    print (" + ".join (terms ))
    print (f"Zj = {zj_new :.4g}")
    print (f"\nCj = {new_var_obj :.4g}")
    print (f"\nZj - Cj = {zj_new :.4g} - {new_var_obj :.4g} = {zj_cj_new :.4g}")

    new_table =[]
    for i in range (m ):
        new_row =table [i ][:-1 ]+[new_tableau_column [i ]]+[table [i ][-1 ]]
        new_table .append (new_row )

    new_var_names =var_names [:-1 ]+[new_var_name ]+[var_names [-1 ]]if var_names [-1 ].startswith ('s')else var_names +[new_var_name ]

    insert_pos =original_n 
    new_var_names =list (var_names )
    new_var_names .insert (insert_pos ,new_var_name )

    new_cj =list (cj )
    new_cj .insert (insert_pos ,new_var_obj )

    new_table =[]
    for i in range (m ):
        new_row =list (table [i ][:insert_pos ])+[new_tableau_column [i ]]+list (table [i ][insert_pos :])
        new_table .append (new_row )

    problem ['num_vars']=original_n +1 
    problem ['obj_coef'].append (new_var_obj )
    for i in range (m ):
        problem ['constraints'][i ].append (new_var_coeff [i ])

    print (f"\n{'='*80 }")
    print ("UPDATED SIMPLEX TABLE WITH NEW VARIABLE")
    print ('='*80 )
    print_simplex_table (new_table ,basic_vars ,new_var_names ,new_cj ,cb ,iteration =0 )

    print (f"\n{'='*80 }")
    print ("OPTIMALITY CHECK")
    print ('='*80 )

    if zj_cj_new >=-1e-9 :
        print (f"\nZj-Cj for {new_var_name } = {zj_cj_new :.4g} >= 0")
        print ("SOLUTION REMAINS OPTIMAL!")
        print (f"\n{new_var_name } will not enter the basis (it's not profitable)")

        profit =sum (cb [i ]*new_table [i ][-1 ]for i in range (m ))
        print (f"\nOptimal Value Z = {profit :.4g} (unchanged)")

        return new_table ,basic_vars ,new_var_names ,new_cj ,cb 
    else :
        print (f"\nZj-Cj for {new_var_name } = {zj_cj_new :.4g} < 0")
        print (f"SOLUTION IS NO LONGER OPTIMAL!")
        print (f"\n{new_var_name } should enter the basis (it's profitable)")
        print ("Applying Simplex Method to find new optimum...")

        input ("\nPress Enter to continue with Simplex...")

        result =continue_simplex_for_sensitivity (new_table ,basic_vars ,new_var_names ,new_cj ,cb ,problem )
        if result [0 ]is not None :
            return result [0 ],result [1 ],new_var_names ,result [2 ],result [3 ]
        return None ,None ,None ,None ,None 

def sensitivity_analysis_case4_menu (problem ,table ,basic_vars ,var_names ,cj ,cb ):

    print ("\n"+"="*80 )
    print ("CASE 4: ADDITION OF A NEW VARIABLE")
    print ("="*80 )

    m =len (table )
    n =problem ['num_vars']

    print (f"\nCurrent problem has {n } variables: {', '.join ([f'x{i +1 }'for i in range (n )])}")
    print (f"Adding new variable: x{n +1 }")

    new_var_obj =get_float_input (f"\nEnter objective coefficient c{n +1 }: ")

    print (f"\nEnter constraint coefficients for x{n +1 }:")
    new_var_coeff =[]
    for i in range (m ):
        val =get_float_input (f"  Enter a{i +1 }{n +1 } (coefficient in constraint {i +1 }): ")
        new_var_coeff .append (val )

    result =sensitivity_case4_add_variable (problem ,table ,basic_vars ,var_names ,cj ,cb ,new_var_coeff ,new_var_obj )

    if result [0 ]is not None :
        table ,basic_vars ,var_names ,cj ,cb =result 
        print ("\n[OK] New variable added successfully!")
    else :
        print ("\n[!] Could not add new variable")

    return table ,basic_vars ,var_names ,cj ,cb 

def sensitivity_case5_add_constraint (problem ,table ,basic_vars ,var_names ,cj ,cb ,new_constraint_coeffs ,new_rhs ,constraint_type ):

    print (f"\n{'='*80 }")
    print ("CASE 5: ADDITION OF A NEW CONSTRAINT")
    print ('='*80 )

    m =len (table )
    n =problem ['num_vars']

    print (f"\nNew constraint:")
    terms =[]
    for j in range (n ):
        if new_constraint_coeffs [j ]!=0 :
            terms .append (f"{new_constraint_coeffs [j ]}x{j +1 }")
    constraint_str =" + ".join (terms )if terms else "0"

    if constraint_type ==1 :
        constraint_str +=f" <= {new_rhs }"
    elif constraint_type ==2 :
        constraint_str +=f" = {new_rhs }"
    else :
        constraint_str +=f" >= {new_rhs }"

    print (f"  {constraint_str }")

    print (f"\n{'='*80 }")
    print ("STEP 1: CHECK IF CURRENT SOLUTION SATISFIES NEW CONSTRAINT")
    print ('='*80 )

    current_solution ={}
    for i ,bv in enumerate (basic_vars ):
        current_solution [bv ]=table [i ][-1 ]

    lhs_value =0 
    print ("\nCurrent optimal solution:")
    for j in range (n ):
        var_name =f"x{j +1 }"
        if var_name in current_solution :
            val =current_solution [var_name ]
        else :
            val =0 
        print (f"  {var_name } = {val :.4g}")
        lhs_value +=new_constraint_coeffs [j ]*val 

    print (f"\nEvaluating new constraint with current solution:")
    print (f"  LHS = ",end ="")
    terms =[]
    for j in range (n ):
        var_name =f"x{j +1 }"
        if var_name in current_solution :
            val =current_solution [var_name ]
        else :
            val =0 
        if new_constraint_coeffs [j ]!=0 :
            terms .append (f"({new_constraint_coeffs [j ]} x {val :.4g})")
    print (" + ".join (terms )if terms else "0")
    print (f"  LHS = {lhs_value :.4g}")
    print (f"  RHS = {new_rhs :.4g}")

    satisfied =False 
    if constraint_type ==1 :
        satisfied =lhs_value <=new_rhs +1e-9 
        print (f"\n  Check: {lhs_value :.4g} <= {new_rhs :.4g}?")
    elif constraint_type ==2 :
        satisfied =abs (lhs_value -new_rhs )<1e-9 
        print (f"\n  Check: {lhs_value :.4g} = {new_rhs :.4g}?")
    else :
        satisfied =lhs_value >=new_rhs -1e-9 
        print (f"\n  Check: {lhs_value :.4g} >= {new_rhs :.4g}?")

    if satisfied :
        print (f"\n{'='*80 }")
        print ("RESULT: CONSTRAINT IS ALREADY SATISFIED!")
        print ('='*80 )
        print ("\nThe current optimal solution satisfies the new constraint.")
        print ("NO NEED TO ADD THIS CONSTRAINT - optimal solution unchanged!")

        profit =sum (cb [i ]*table [i ][-1 ]for i in range (m ))
        print (f"\nOptimal Value Z = {profit :.4g} (unchanged)")

        return table ,basic_vars ,var_names ,cj ,cb 

    if constraint_type ==2 :
        print (f"\n{'='*80 }")
        print ("HANDLING EQUALITY CONSTRAINT")
        print ('='*80 )
        print ("\nEquality constraint = can be split into <= and >=")
        print ("Checking which one is violated...")

        if lhs_value >new_rhs :
            print (f"\nLHS ({lhs_value :.4g}) > RHS ({new_rhs :.4g})")
            print ("The <= version is violated. Adding as <= constraint.")
            constraint_type =1 
        else :
            print (f"\nLHS ({lhs_value :.4g}) < RHS ({new_rhs :.4g})")
            print ("The >= version is violated. Adding as >= constraint.")
            constraint_type =3 

    print (f"\n{'='*80 }")
    print ("STEP 2: ADD NEW CONSTRAINT TO TABLEAU")
    print ('='*80 )

    print ("\nSince constraint is not satisfied, we must add it to the tableau.")

    B_inv =calculate_b_inverse (table ,basic_vars ,var_names ,problem )

    if B_inv is None :
        print ("\n[!] Error: Could not calculate B inverse")
        return None ,None ,None ,None ,None 

    print_matrix (B_inv ,"B^-1 (From Current Optimal Table)")

    num_total_vars =len (var_names )
    extended_coeffs =[0 ]*num_total_vars 

    for j in range (n ):
        extended_coeffs [j ]=new_constraint_coeffs [j ]

    print (f"\nTransforming new constraint using current tableau...")

    new_row =extended_coeffs [:]
    new_rhs_transformed =new_rhs 

    for idx ,bv in enumerate (basic_vars ):
        if bv in var_names :
            bv_col =var_names .index (bv )
            if bv_col <n :
                coeff_in_new =new_constraint_coeffs [bv_col ]
                if abs (coeff_in_new )>1e-9 :
                    print (f"\n  {bv } is basic in row {idx +1 }")
                    print (f"  Coefficient of {bv } in new constraint: {coeff_in_new :.4g}")
                    print (f"  Subtracting {coeff_in_new :.4g} x Row {idx +1 }")

                    for j in range (num_total_vars ):
                        new_row [j ]-=coeff_in_new *table [idx ][j ]
                    new_rhs_transformed -=coeff_in_new *table [idx ][-1 ]

    print (f"\nTransformed new constraint row:")
    print (f"  Coefficients: {[f'{x :.4g}'for x in new_row ]}")
    print (f"  RHS: {new_rhs_transformed :.4g}")

    if constraint_type ==1 :
        new_slack_name =f"s{m +1 }"
        new_row .append (1 )
        print (f"\nAdding slack variable {new_slack_name } with coefficient +1")
        new_row .append (new_rhs_transformed )
    else :
        new_slack_name =f"s{m +1 }"
        print (f"\nFor >= constraint not satisfied, multiply by -1 for dual simplex:")
        print (f"  Old: ... >= {new_rhs_transformed :.4g}")
        print (f"  New: ... <= {-new_rhs_transformed :.4g}")
        new_row =[-x for x in new_row ]
        new_rhs_transformed =-new_rhs_transformed 
        new_row .append (1 )
        print (f"\nAdding slack variable {new_slack_name } with coefficient +1")
        new_row .append (new_rhs_transformed )
        print (f"  (RHS is now {new_rhs_transformed :.4g}, will be negative -> dual simplex needed)")

    new_table =[]
    for i in range (m ):
        old_row =table [i ][:-1 ]+[0 ]+[table [i ][-1 ]]
        new_table .append (old_row )

    new_table .append (new_row )

    new_basic_vars =basic_vars +[new_slack_name ]

    new_var_names =list (var_names [:-1 ])+[new_slack_name ]+[var_names [-1 ]]if len (var_names )>n else list (var_names )+[new_slack_name ]
    new_var_names =list (var_names )+[new_slack_name ]

    new_cj =list (cj )+[0 ]

    new_cb =list (cb )+[0 ]

    problem ['num_constraints']=m +1 
    problem ['constraints'].append (new_constraint_coeffs +[0 ]*(len (var_names )-n ))
    problem ['rhs'].append (new_rhs )
    problem ['constraint_types'].append (constraint_type )

    print (f"\n{'='*80 }")
    print ("TABLEAU WITH NEW CONSTRAINT ADDED")
    print ('='*80 )
    print_simplex_table (new_table ,new_basic_vars ,new_var_names ,new_cj ,new_cb ,iteration =0 )

    print (f"\n{'='*80 }")
    print ("STEP 3: CHECK FEASIBILITY")
    print ('='*80 )

    is_feasible =True 
    infeasible_row =-1 

    for i in range (m +1 ):
        if new_table [i ][-1 ]<-1e-9 :
            is_feasible =False 
            infeasible_row =i 
            print (f"  {new_basic_vars [i ]} = {new_table [i ][-1 ]:.4g} < 0  [INFEASIBLE]")
        else :
            print (f"  {new_basic_vars [i ]} = {new_table [i ][-1 ]:.4g} >= 0  [OK]")

    if is_feasible :
        print (f"\n{'='*80 }")
        print ("SOLUTION IS FEASIBLE!")
        print ('='*80 )

        num_vars =len (new_var_names )
        all_zj_cj =[]
        for j in range (num_vars ):
            zj_j =sum (new_cb [i ]*new_table [i ][j ]for i in range (m +1 ))
            all_zj_cj .append (zj_j -new_cj [j ])

        is_optimal =all (val >=-1e-9 for val in all_zj_cj )

        if is_optimal :
            print ("\nAll Zj-Cj >= 0, SOLUTION IS OPTIMAL!")
            profit =sum (new_cb [i ]*new_table [i ][-1 ]for i in range (m +1 ))
            print (f"\nOptimal Value Z = {profit :.4g}")
            return new_table ,new_basic_vars ,new_var_names ,new_cj ,new_cb 
        else :
            print ("\nSome Zj-Cj < 0, need to continue simplex...")
            input ("\nPress Enter to continue with Simplex...")
            return continue_simplex_for_sensitivity (new_table ,new_basic_vars ,new_var_names ,new_cj ,new_cb ,problem )
    else :
        print (f"\n{'='*80 }")
        print ("SOLUTION IS INFEASIBLE!")
        print ('='*80 )
        print ("\nApplying DUAL SIMPLEX METHOD to restore feasibility...")

        input ("\nPress Enter to continue with Dual Simplex...")

        result =apply_dual_simplex_to_table (new_table ,new_basic_vars ,new_var_names ,new_cj ,new_cb ,problem )

        if result [0 ]is not None :
            return result [0 ],result [1 ],new_var_names ,new_cj ,result [2 ]
        return None ,None ,None ,None ,None 

def sensitivity_analysis_case5_menu (problem ,table ,basic_vars ,var_names ,cj ,cb ):

    print ("\n"+"="*80 )
    print ("CASE 5: ADDITION OF A NEW CONSTRAINT")
    print ("="*80 )

    m =len (table )
    n =problem ['num_vars']

    print (f"\nCurrent problem has {m } constraints")
    print (f"Adding constraint {m +1 }")

    print ("\nConstraint type:")
    print ("  1. <= (less than or equal)")
    print ("  2. = (equality)")
    print ("  3. >= (greater than or equal)")
    constraint_type =get_int_input ("\nEnter type (1-3): ")

    if constraint_type not in [1 ,2 ,3 ]:
        print ("Invalid constraint type.")
        return table ,basic_vars ,var_names ,cj ,cb 

    print (f"\nEnter coefficients for new constraint:")
    new_coeffs =[]
    for j in range (n ):
        val =get_float_input (f"  Enter coefficient for x{j +1 }: ")
        new_coeffs .append (val )

    new_rhs =get_float_input (f"\nEnter RHS value: ")

    result =sensitivity_case5_add_constraint (problem ,table ,basic_vars ,var_names ,cj ,cb ,new_coeffs ,new_rhs ,constraint_type )

    if result [0 ]is not None :
        table ,basic_vars ,var_names ,cj ,cb =result 
        print ("\n[OK] New constraint processed successfully!")
    else :
        print ("\n"+"="*80 )
        print ("PROBLEM BECAME INFEASIBLE")
        print ("="*80 )
        print ("\nThe new constraint is incompatible with the existing constraints.")
        print ("No feasible solution exists that satisfies all constraints simultaneously.")
        print ("\n[!] Constraint cannot be added - problem remains at previous optimal solution")

    return table ,basic_vars ,var_names ,cj ,cb 

def sensitivity_analysis_menu (problem ,table ,basic_vars ,var_names ,cj ,cb ,is_optimal ):

    print ("\n"+"="*80 )
    print ("   SENSITIVITY ANALYSIS")
    print ("="*80 )

    if not is_optimal :
        print ("\n[!] WARNING: Current solution is not optimal.")
        print ("    Sensitivity analysis requires an optimal solution.")
        print ("    Solving problem first...")
        input ("\nPress Enter to solve...")

        optimal_value =solve_simplex (problem )
        if optimal_value is None :
            print ("\nCould not find optimal solution. Cannot perform sensitivity analysis.")
            return 

        print ("\n[!] Please run sensitivity analysis from menu option 11 after solving.")
        return 

    print ("\nCurrent solution is OPTIMAL. Ready for sensitivity analysis.")

    while True :
        print ("\n"+"-"*80 )
        print ("SENSITIVITY ANALYSIS CASES")
        print ("-"*80 )
        print ("1. Case 1: Change in Objective Function Coefficients (Cj)")
        print ("2. Case 2: Change in RHS / Resources (bi)")
        print ("3. Case 3: Change in Coefficient Matrix (aij)")
        print ("4. Case 4: Addition of a New Variable")
        print ("5. Case 5: Addition of a New Constraint")
        print ("6. Back to Main Menu")
        print ("-"*80 )

        case_choice =get_int_input ("\nEnter choice (1-6): ")

        if case_choice ==6 :
            return table ,basic_vars ,var_names ,cj ,cb 

        if case_choice ==1 :
            print ("\n"+"="*80 )
            print ("CASE 1: CHANGE IN OBJECTIVE FUNCTION COEFFICIENTS")
            print ("="*80 )

            print ("\nOptions:")
            print ("1. Find range for a coefficient (where solution remains optimal)")
            print ("2. Change a specific coefficient value")
            print ("3. Find ranges for all coefficients")

            option =get_int_input ("\nEnter choice (1-3): ")

            if option ==1 :
                print (f"\nAvailable variables: {', '.join ([f'{i +1 }. {var_names [i ]}'for i in range (problem ['num_vars'])])}")
                var_choice =get_int_input (f"\nWhich variable coefficient (1-{problem ['num_vars']}): ")

                if 1 <=var_choice <=problem ['num_vars']:
                    find_objective_coefficient_range (table ,basic_vars ,var_names ,cj ,cb ,var_choice -1 ,problem ['is_max'])
                else :
                    print ("Invalid variable choice.")

            elif option ==2 :
                print (f"\nAvailable variables: {', '.join ([f'{i +1 }. {var_names [i ]}'for i in range (problem ['num_vars'])])}")
                var_choice =get_int_input (f"\nWhich variable coefficient (1-{problem ['num_vars']}): ")

                if 1 <=var_choice <=problem ['num_vars']:
                    print (f"\nCurrent coefficient of {var_names [var_choice -1 ]}: {cj [var_choice -1 ]}")
                    new_value =float (input (f"Enter new coefficient value: "))

                    still_optimal ,new_cj ,new_cb =apply_objective_coefficient_change (
                    problem ,table ,basic_vars ,var_names ,cj ,cb ,var_choice -1 ,new_value )

                    if not still_optimal :
                        print ("\n[!] Continuing from current basis with Simplex Method...")

                        optimal_value ,new_table ,new_basic_vars ,new_var_names ,final_cj ,final_cb =continue_simplex_from_table (
                        table ,basic_vars ,var_names ,new_cj ,new_cb ,problem ,start_iteration =0 )

                        if optimal_value is not None :
                            table =new_table 
                            basic_vars =new_basic_vars 
                            var_names =new_var_names 
                            cj =final_cj 
                            cb =final_cb 
                            print (f"\nNew optimal solution found with Z = {optimal_value }")
                        else :
                            print ("\nCould not find new optimal solution.")
                    else :
                        cj =new_cj 
                        cb =new_cb 

                else :
                    print ("Invalid variable choice.")

            elif option ==3 :
                print ("\n"+"="*80 )
                print ("FINDING RANGES FOR ALL OBJECTIVE FUNCTION COEFFICIENTS")
                print ("="*80 )

                for i in range (problem ['num_vars']):
                    input (f"\nPress Enter to find range for {var_names [i ]}...")
                    find_objective_coefficient_range (table ,basic_vars ,var_names ,cj ,cb ,i ,problem ['is_max'])

        elif case_choice ==2 :
            table ,basic_vars ,cb =sensitivity_analysis_case2_menu (problem ,table ,basic_vars ,var_names ,cj ,cb )

        elif case_choice ==3 :
            table ,basic_vars ,cj ,cb =sensitivity_analysis_case3_menu (problem ,table ,basic_vars ,var_names ,cj ,cb )

        elif case_choice ==4 :
            table ,basic_vars ,var_names ,cj ,cb =sensitivity_analysis_case4_menu (problem ,table ,basic_vars ,var_names ,cj ,cb )

        elif case_choice ==5 :
            table ,basic_vars ,var_names ,cj ,cb =sensitivity_analysis_case5_menu (problem ,table ,basic_vars ,var_names ,cj ,cb )

        else :
            print ("Invalid choice.")

def solve_and_prepare_sensitivity (problem ,var_prefix ='x'):

    print ("\n"+"#"*80 )
    print ("SOLVING PROBLEM FOR SENSITIVITY ANALYSIS")
    print ("#"*80 )

    table ,basic_vars ,var_names ,cj ,cb =setup_simplex_table (problem ,var_prefix )

    iteration =0 

    while True :
        num_vars =len (var_names )
        zj =calculate_zj (table ,cb ,num_vars )
        zj_cj =calculate_zj_cj (zj ,cj ,None )

        if check_optimality (zj_cj ):
            print (f"\n{'='*80 }")
            print (f"ITERATION {iteration }")
            print ('='*80 )
            zj_final ,zj_cj_final =print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration )

            if not check_rhs_feasibility (table ):
                print ("\n[!] Solution is infeasible. Cannot perform sensitivity analysis.")
                return None ,None ,None ,None ,None ,False 

            solution =extract_solution (table ,basic_vars ,var_names ,problem ['is_max'])
            print_solution (solution ,var_names ,zj_final ,problem ['is_max'],problem ['num_vars'])

            print ("\n"+"="*80 )
            print ("OPTIMAL SOLUTION FOUND!")
            print ("Ready for sensitivity analysis.")
            print ("="*80 )

            return table ,basic_vars ,var_names ,cj ,cb ,True 

        pivot_col ,min_zj_cj =find_pivot_column (zj_cj ,var_names )

        if pivot_col ==-1 :
            break 

        zj ,zj_cj =print_simplex_table (table ,basic_vars ,var_names ,cj ,cb ,iteration ,pivot_col =pivot_col )

        print (f"\nEntering Variable: {var_names [pivot_col ]} (most negative Zj-Cj = {print_fraction (min_zj_cj )})")

        if check_unbounded (table ,pivot_col ):
            print ("\n[!] Problem is unbounded. Cannot perform sensitivity analysis.")
            return None ,None ,None ,None ,None ,False 

        pivot_row ,min_ratio ,ratios =find_pivot_row (table ,pivot_col ,basic_vars )

        if pivot_row ==-1 :
            print ("\n[!] No valid pivot row. Cannot continue.")
            return None ,None ,None ,None ,None ,False 

        print (f"\nLeaving Variable: {basic_vars [pivot_row ]} (minimum ratio = {print_fraction (min_ratio )})")

        input ("\n>>> Press Enter to perform pivot operation...")

        table ,basic_vars ,cb =perform_pivot_operation (table ,pivot_row ,pivot_col ,basic_vars ,var_names ,cb ,cj )

        iteration +=1 

    return None ,None ,None ,None ,None ,False 

def solve_lp_relaxation (problem ,bounds =None ):

    import copy 
    prob =copy .deepcopy (problem )

    if 'obj_coef'not in prob and 'objective'in prob :
        prob ['obj_coef']=prob ['objective']

    if bounds :
        for var_idx ,(lb ,ub )in bounds .items ():
            if lb is not None :
                new_constraint =[0 ]*prob ['num_vars']
                new_constraint [var_idx ]=1 
                prob ['constraints'].append (new_constraint )
                prob ['rhs'].append (lb )
                prob ['constraint_types'].append (2 )
                prob ['num_constraints']+=1 
            if ub is not None :
                new_constraint =[0 ]*prob ['num_vars']
                new_constraint [var_idx ]=1 
                prob ['constraints'].append (new_constraint )
                prob ['rhs'].append (ub )
                prob ['constraint_types'].append (1 )
                prob ['num_constraints']+=1 

    for i in range (prob ['num_constraints']):
        if prob ['rhs'][i ]<0 :
            prob ['constraints'][i ]=[-x for x in prob ['constraints'][i ]]
            prob ['rhs'][i ]=-prob ['rhs'][i ]
            if prob ['constraint_types'][i ]==1 :
                prob ['constraint_types'][i ]=2 
            elif prob ['constraint_types'][i ]==2 :
                prob ['constraint_types'][i ]=1 

    needs_big_m =any (ct !=1 for ct in prob ['constraint_types'])

    try :
        if needs_big_m :
            table ,basic_vars ,var_names ,cj ,cb ,M =setup_big_m_table (prob ,M =10000 )
        else :
            table ,basic_vars ,var_names ,cj ,cb =setup_simplex_table (prob )
            M =None 

        m =len (table )
        n =len (var_names )
        iteration =0 
        max_iterations =100 

        while iteration <max_iterations :
            zj =calculate_zj (table ,cb ,n )
            zj_cj =calculate_zj_cj (zj ,cj ,M )

            if check_optimality (zj_cj ):
                solution ={}
                for j in range (prob ['num_vars']):
                    var_name =f"x{j +1 }"
                    if var_name in basic_vars :
                        row =basic_vars .index (var_name )
                        solution [var_name ]=table [row ][-1 ]
                    else :
                        solution [var_name ]=0 

                if needs_big_m :
                    for bv in basic_vars :
                        if bv .startswith ('A'):
                            return None ,None ,False 

                optimal_value =sum (cb [i ]*table [i ][-1 ]for i in range (m ))
                if not prob ['is_max']:
                    optimal_value =-optimal_value 

                return optimal_value ,solution ,True 

            if prob ['is_max']:
                min_val =min (zj_cj )
                pivot_col =zj_cj .index (min_val )
            else :
                max_val =max (zj_cj )
                pivot_col =zj_cj .index (max_val )

            min_ratio =float ('inf')
            pivot_row =-1 
            for i in range (m ):
                if table [i ][pivot_col ]>1e-9 :
                    ratio =table [i ][-1 ]/table [i ][pivot_col ]
                    if ratio >=0 and ratio <min_ratio :
                        min_ratio =ratio 
                        pivot_row =i 

            if pivot_row ==-1 :
                return None ,None ,False 

            table ,basic_vars ,cb =perform_pivot_operation (table ,pivot_row ,pivot_col ,basic_vars ,var_names ,cb ,cj )
            iteration +=1 

        return None ,None ,False 

    except Exception as e :
        return None ,None ,False 

def is_integer_solution (solution ,tolerance =1e-6 ):

    for var ,val in solution .items ():
        if var .startswith ('x'):
            if abs (val -round (val ))>tolerance :
                return False 
    return True 

def find_branching_variable (solution ,tolerance =1e-6 ):

    for var ,val in sorted (solution .items ()):
        if var .startswith ('x'):
            if abs (val -round (val ))>tolerance :
                return var ,val 
    return None ,None 

class BranchAndBoundNode :

    node_count =0 

    def __init__ (self ,bounds ,parent =None ,branch_var =None ,branch_type =None ):
        BranchAndBoundNode .node_count +=1 
        self .id =BranchAndBoundNode .node_count 
        self .bounds =bounds .copy ()if bounds else {}
        self .parent =parent 
        self .branch_var =branch_var 
        self .branch_type =branch_type 
        self .optimal_value =None 
        self .solution =None 
        self .status ="pending"
        self .children =[]

def solve_ilp_branch_and_bound (problem ):

    import math 

    print ("\n"+"#"*80 )
    print ("   INTEGER LINEAR PROGRAMMING - BRANCH AND BOUND METHOD")
    print ("#"*80 )

    BranchAndBoundNode .node_count =0 

    print ("\n"+"="*80 )
    print ("PROBLEM FORMULATION")
    print ("="*80 )

    obj_type ="Maximize"if problem ['is_max']else "Minimize"
    n =problem ['num_vars']
    m =problem ['num_constraints']

    print (f"\n{obj_type } Z = ",end ="")
    terms =[f"{problem ['obj_coef'][j ]}x{j +1 }"for j in range (n )if problem ['obj_coef'][j ]!=0 ]
    print (" + ".join (terms ))

    print ("\nSubject to:")
    for i in range (m ):
        terms =[f"{problem ['constraints'][i ][j ]}x{j +1 }"for j in range (n )if problem ['constraints'][i ][j ]!=0 ]
        constraint_str =" + ".join (terms )if terms else "0"

        ct =problem ['constraint_types'][i ]
        if ct ==1 :
            constraint_str +=f" <= {problem ['rhs'][i ]}"
        elif ct ==2 :
            constraint_str +=f" = {problem ['rhs'][i ]}"
        else :
            constraint_str +=f" >= {problem ['rhs'][i ]}"
        print (f"  {constraint_str }")

    print (f"\n  x1, x2, ..., x{n } >= 0 and INTEGER")

    print ("\n"+"="*80 )
    print ("BRANCH AND BOUND ALGORITHM")
    print ("="*80 )
    print ("\nSteps:")
    print ("1. Solve LP relaxation (ignore integer constraints)")
    print ("2. If solution is integer, we're done")
    print ("3. Otherwise, pick a non-integer variable to branch")
    print ("4. Create two subproblems: x <= floor(val) and x >= ceil(val)")
    print ("5. Use bounds to prune subproblems")
    print ("6. Repeat until optimal integer solution found")

    best_solution =None 
    best_value =float ('-inf')if problem ['is_max']else float ('inf')

    root =BranchAndBoundNode ({})
    nodes =[root ]
    all_nodes =[root ]

    iteration =0 
    max_nodes =100 

    print ("\n"+"="*80 )
    print ("STEP 1: SOLVE LP RELAXATION (ROOT NODE)")
    print ("="*80 )

    while nodes and iteration <max_nodes :
        iteration +=1 
        current =nodes .pop (0 )

        print (f"\n{'='*80 }")
        print (f"NODE {current .id }"+(f" (Branch: {current .branch_var } {current .branch_type })"if current .branch_var else " (ROOT)"))
        print ('='*80 )

        bounds_infeasible =False 
        if current .bounds :
            print ("\nBounds for this node:")
            for var_idx ,(lb ,ub )in current .bounds .items ():
                var_name =f"x{var_idx +1 }"
                if lb is not None and ub is not None :
                    print (f"  {lb } <= {var_name } <= {ub }")
                    if lb >ub +1e-6 :
                        bounds_infeasible =True 
                elif lb is not None :
                    print (f"  {var_name } >= {lb }")
                elif ub is not None :
                    print (f"  {var_name } <= {ub }")

            if bounds_infeasible :
                current .status ="infeasible"
                print ("\n  X INFEASIBLE: Conflicting bounds (lb > ub) - Node pruned")
                continue 

        print ("\nSolving LP relaxation...")
        opt_val ,solution ,feasible =solve_lp_relaxation (problem ,current .bounds )

        if not feasible or opt_val is None :
            current .status ="infeasible"
            print ("\n  X INFEASIBLE or UNBOUNDED - Node pruned")
            continue 

        current .optimal_value =opt_val 
        current .solution =solution 

        print (f"\nLP Relaxation Solution:")
        for var in sorted (solution .keys ()):
            if var .startswith ('x'):
                print (f"  {var } = {solution [var ]:.4f}")
        print (f"\n  Z = {opt_val :.4f}")

        if problem ['is_max']:
            if opt_val <=best_value :
                current .status ="pruned"
                print (f"\n  X PRUNED: Z = {opt_val :.4f} <= Best = {best_value :.4f}")
                continue 
        else :
            if opt_val >=best_value :
                current .status ="pruned"
                print (f"\n  X PRUNED: Z = {opt_val :.4f} >= Best = {best_value :.4f}")
                continue 

        if is_integer_solution (solution ):
            current .status ="optimal"
            print ("\n  OK INTEGER SOLUTION FOUND!")

            if problem ['is_max']:
                if opt_val >best_value :
                    best_value =opt_val 
                    best_solution =solution .copy ()
                    print (f"  OK NEW BEST: Z = {best_value :.4f}")
            else :
                if opt_val <best_value :
                    best_value =opt_val 
                    best_solution =solution .copy ()
                    print (f"  OK NEW BEST: Z = {best_value :.4f}")
            continue 

        branch_var ,branch_val =find_branching_variable (solution )

        if branch_var is None :
            continue 

        var_idx =int (branch_var [1 :])-1 
        floor_val =math .floor (branch_val )
        ceil_val =math .ceil (branch_val )

        print (f"\n  X Non-integer: {branch_var } = {branch_val :.4f}")
        print (f"\n  BRANCHING on {branch_var }:")
        print (f"    Left branch:  {branch_var } <= {floor_val }")
        print (f"    Right branch: {branch_var } >= {ceil_val }")

        current .status ="branched"

        left_bounds =current .bounds .copy ()
        left_feasible =True 
        if var_idx in left_bounds :
            lb ,ub =left_bounds [var_idx ]
            new_ub =min (ub ,floor_val )if ub is not None else floor_val 
            if lb is not None and lb >new_ub :
                left_feasible =False 
            left_bounds [var_idx ]=(lb ,new_ub )
        else :
            left_bounds [var_idx ]=(None ,floor_val )

        if left_feasible :
            left_child =BranchAndBoundNode (left_bounds ,current ,branch_var ,f"<= {floor_val }")
            current .children .append (left_child )
            all_nodes .append (left_child )
            nodes .append (left_child )

        right_bounds =current .bounds .copy ()
        right_feasible =True 
        if var_idx in right_bounds :
            lb ,ub =right_bounds [var_idx ]
            new_lb =max (lb ,ceil_val )if lb is not None else ceil_val 
            if ub is not None and new_lb >ub :
                right_feasible =False 
            right_bounds [var_idx ]=(new_lb ,ub )
        else :
            right_bounds [var_idx ]=(ceil_val ,None )

        if right_feasible :
            right_child =BranchAndBoundNode (right_bounds ,current ,branch_var ,f">= {ceil_val }")
            current .children .append (right_child )
            all_nodes .append (right_child )
            nodes .append (right_child )

        input ("\n>>> Press Enter to continue to next node...")

    if iteration >=max_nodes :
        print (f"\n>>> Node limit ({max_nodes }) reached. Stopping search.")

    print ("\n"+"="*80 )
    print ("BRANCH AND BOUND TREE")
    print ("="*80 )

    def print_tree (node ,prefix ="",is_last =True ):
        connector ="+-- "if is_last else "+-- "
        branch_info =f" ({node .branch_var } {node .branch_type })"if node .branch_var else ""
        status_sym ={"optimal":"OK","infeasible":"X","pruned":"X","branched":"->","pending":"?"}

        if node .optimal_value is not None :
            print (f"{prefix }{connector }Node {node .id }{branch_info }: Z={node .optimal_value :.2f} [{status_sym .get (node .status ,'?')} {node .status }]")
        else :
            print (f"{prefix }{connector }Node {node .id }{branch_info }: [{status_sym .get (node .status ,'?')} {node .status }]")

        new_prefix =prefix +("    "if is_last else "|   ")
        for i ,child in enumerate (node .children ):
            print_tree (child ,new_prefix ,i ==len (node .children )-1 )

    print ()
    print_tree (root ,"",True )

    print ("\n"+"="*80 )
    print ("OPTIMAL INTEGER SOLUTION")
    print ("="*80 )

    if best_solution :
        print ("\nSolution:")
        for var in sorted (best_solution .keys ()):
            if var .startswith ('x'):
                print (f"  {var } = {int (round (best_solution [var ]))}")
        print (f"\nOptimal Value Z = {best_value :.4f}")

        print ("\n"+"-"*40 )
        print ("VERIFICATION")
        print ("-"*40 )
        obj_val =sum (problem ['obj_coef'][j ]*round (best_solution [f"x{j +1 }"])for j in range (n ))
        print (f"Z = ",end ="")
        terms =[f"({problem ['obj_coef'][j ]} x {int (round (best_solution [f'x{j +1 }']))})"for j in range (n )]
        print (" + ".join (terms ))
        print (f"Z = {obj_val }")

        print ("\nConstraint Check:")
        all_satisfied =True 
        for i in range (m ):
            lhs =sum (problem ['constraints'][i ][j ]*round (best_solution [f"x{j +1 }"])for j in range (n ))
            ct =problem ['constraint_types'][i ]
            rhs =problem ['rhs'][i ]

            if ct ==1 :
                satisfied =lhs <=rhs 
                op ="<="
            elif ct ==2 :
                satisfied =abs (lhs -rhs )<1e-6 
                op ="="
            else :
                satisfied =lhs >=rhs 
                op =">="

            status ="OK"if satisfied else "X"
            print (f"  Constraint {i +1 }: {lhs :.0f} {op } {rhs } {status }")
            all_satisfied =all_satisfied and satisfied 

        if all_satisfied :
            print ("\nOK All constraints satisfied!")
    else :
        print ("\nNo feasible integer solution found.")

    return best_solution ,best_value 

def ilp_menu ():

    print ("\n"+"="*80 )
    print ("INTEGER LINEAR PROGRAMMING (BRANCH AND BOUND)")
    print ("="*80 )

    print ("\nInput method:")
    print ("1. Manual Input")
    print ("2. Load from File (problem.txt)")

    choice =get_int_input ("\nEnter choice (1-2): ")

    if choice ==1 :
        problem =input_problem ()
    elif choice ==2 :
        problem =read_problem_from_file ('problem.txt')
        if problem is None :
            print ("Failed to load problem from file.")
            return 
    else :
        print ("Invalid choice.")
        return 

    input ("\nPress Enter to solve using Branch and Bound...")
    solve_ilp_branch_and_bound (problem )

def solve_tsp_branch_and_bound (dist_matrix ,city_names =None ):

    import copy 

    n =len (dist_matrix )
    INF =float ('inf')

    if city_names is None :
        city_names =[str (i +1 )for i in range (n )]

    print ("\n"+"#"*80 )
    print ("   TRAVELLING SALESMAN PROBLEM - BRANCH AND BOUND")
    print ("#"*80 )

    print ("\n"+"="*80 )
    print ("DISTANCE/COST MATRIX")
    print ("="*80 )

    header ="     "+"".join ([f"{city_names [j ]:>8}"for j in range (n )])
    print (header )
    print ("-"*len (header ))
    for i in range (n ):
        row_str =f"{city_names [i ]:>4} "
        for j in range (n ):
            if dist_matrix [i ][j ]==INF :
                row_str +=f"{'INF':>8}"
            else :
                row_str +=f"{dist_matrix [i ][j ]:>8.2f}"
        print (row_str )

    print ("\n"+"="*80 )
    print ("BRANCH AND BOUND METHOD FOR TSP")
    print ("="*80 )
    print ("\nSteps:")
    print ("1. Reduce the matrix (subtract row min, then column min)")
    print ("2. Calculate lower bound = sum of reductions")
    print ("3. Branch on edge with maximum regret")
    print ("4. Create two subproblems: include edge vs exclude edge")
    print ("5. Prune nodes with bound >= best solution")
    print ("6. Continue until complete tour found")

    def reduce_matrix (matrix ):

        m =len (matrix )
        mat =[row [:]for row in matrix ]
        reduction =0 

        row_mins =[]
        for i in range (m ):
            finite_vals =[val for val in mat [i ]if val !=INF ]
            if finite_vals :
                row_min =min (finite_vals )
            else :
                row_min =0 
            row_mins .append (row_min )
            if row_min >0 :
                for j in range (m ):
                    if mat [i ][j ]!=INF :
                        mat [i ][j ]-=row_min 
                reduction +=row_min 

        col_mins =[]
        for j in range (m ):
            finite_vals =[mat [i ][j ]for i in range (m )if mat [i ][j ]!=INF ]
            if finite_vals :
                col_min =min (finite_vals )
            else :
                col_min =0 
            col_mins .append (col_min )
            if col_min >0 :
                for i in range (m ):
                    if mat [i ][j ]!=INF :
                        mat [i ][j ]-=col_min 
                reduction +=col_min 

        return mat ,reduction ,row_mins ,col_mins 

    def print_matrix_reduction (matrix ,title ,row_mins =None ,col_mins =None ):

        m =len (matrix )
        print (f"\n{title }")

        header ="     "+"".join ([f"{j +1 :>8}"for j in range (m )])
        if col_mins :
            header +="  Row Min"
        print (header )
        print ("-"*len (header ))

        for i in range (m ):
            row_str =f"{i +1 :>4} "
            for j in range (m ):
                if matrix [i ][j ]==INF :
                    row_str +=f"{'INF':>8}"
                else :
                    row_str +=f"{matrix [i ][j ]:>8.2f}"
            if row_mins :
                row_str +=f"  [{row_mins [i ]:.2f}]"
            print (row_str )

        if col_mins :
            col_str ="Min: "
            for j in range (m ):
                col_str +=f"[{col_mins [j ]:.2f}]  "
            print (col_str )

    def calculate_regret (matrix ,i ,j ):

        m =len (matrix )
        row_vals =[matrix [i ][k ]for k in range (m )if k !=j and matrix [i ][k ]!=INF ]
        if row_vals :
            row_min =min (row_vals )
        else :
            row_min =0 
        col_vals =[matrix [k ][j ]for k in range (m )if k !=i and matrix [k ][j ]!=INF ]
        if col_vals :
            col_min =min (col_vals )
        else :
            col_min =0 
        return row_min +col_min 

    class TSPNode :
        node_count =0 

        def __init__ (self ,matrix ,path ,cost ,level ,parent =None ):
            TSPNode .node_count +=1 
            self .id =TSPNode .node_count 
            self .matrix =[row [:]for row in matrix ]
            self .path =path [:]
            self .cost =cost 
            self .level =level 
            self .parent =parent 

    TSPNode .node_count =0 

    print ("\n"+"="*80 )
    print ("STEP 1: INITIAL MATRIX REDUCTION")
    print ("="*80 )

    initial_matrix =[[dist_matrix [i ][j ]if i !=j else INF for j in range (n )]for i in range (n )]

    print_matrix_reduction (initial_matrix ,"Original Matrix (diagonal = INF)")

    reduced_matrix ,initial_reduction ,row_mins ,col_mins =reduce_matrix (initial_matrix )

    print (f"\nRow Minimums: {row_mins }")
    print (f"Column Minimums: {col_mins }")
    print (f"\nTotal Reduction = {' + '.join ([f'{r :.2f}'for r in row_mins if r >0 ])} + {' + '.join ([f'{c :.2f}'for c in col_mins if c >0 ])}")
    print (f"Total Reduction = {initial_reduction :.2f}")

    print_matrix_reduction (reduced_matrix ,"Reduced Matrix")

    print (f"\nLower Bound at Root = {initial_reduction :.2f}")

    root =TSPNode (reduced_matrix ,[0 ],initial_reduction ,0 )
    nodes =[root ]
    best_tour =None 
    best_cost =INF 

    iteration =0 

    while nodes :
        iteration +=1 

        nodes .sort (key =lambda x :x .cost )
        current =nodes .pop (0 )

        if current .cost >=best_cost :
            print (f"\n>>> Node {current .id } pruned: cost {current .cost :.2f} >= best {best_cost :.2f}")
            continue 

        if current .level ==n -1 :
            last_city =current .path [-1 ]
            return_cost =dist_matrix [last_city ][0 ]

            tour =current .path +[0 ]
            actual_tour_cost =sum (dist_matrix [tour [i ]][tour [i +1 ]]for i in range (len (tour )-1 ))

            if actual_tour_cost <best_cost :
                best_cost =actual_tour_cost 
                best_tour =tour 
                print (f"\n>>> Complete tour found! Actual Cost = {actual_tour_cost :.2f}")
            continue 

        print (f"\n{'='*80 }")
        print (f"ITERATION {iteration }: NODE {current .id }")
        print (f"{'='*80 }")
        print (f"Current Path: {' -> '.join ([city_names [c ]for c in current .path ])}")
        print (f"Current Bound: {current .cost :.2f}")

        last_city =current .path [-1 ]

        print (f"\nFinding best city to visit from {city_names [last_city ]}...")

        best_regret =-1 
        best_next =-1 

        for j in range (n ):
            if j not in current .path and current .matrix [last_city ][j ]!=INF :
                regret =calculate_regret (current .matrix ,last_city ,j )
                print (f"  City {city_names [j ]}: cost = {current .matrix [last_city ][j ]:.2f}, regret = {regret :.2f}")

                if regret >best_regret or best_next ==-1 :
                    best_regret =regret 
                    best_next =j 

        if best_next ==-1 :
            continue 

        print (f"\nBranching to city {city_names [best_next ]}")

        new_matrix =[row [:]for row in current .matrix ]

        for k in range (n ):
            new_matrix [last_city ][k ]=INF 
            new_matrix [k ][best_next ]=INF 

        new_matrix [best_next ][0 ]=INF 

        reduced_new ,reduction ,_ ,_ =reduce_matrix (new_matrix )
        new_cost =current .cost +current .matrix [last_city ][best_next ]+reduction 

        print (f"Edge cost: {current .matrix [last_city ][best_next ]:.2f}")
        print (f"Additional reduction: {reduction :.2f}")
        print (f"New bound: {new_cost :.2f}")

        new_path =current .path +[best_next ]
        child =TSPNode (reduced_new ,new_path ,new_cost ,current .level +1 ,current )

        if new_cost <best_cost :
            nodes .append (child )
        else :
            print (f"  Node pruned (bound >= best)")

        input ("\n>>> Press Enter to continue...")

    print ("\n"+"="*80 )
    print ("OPTIMAL TOUR")
    print ("="*80 )

    if best_tour :
        actual_cost =0 
        for i in range (len (best_tour )-1 ):
            actual_cost +=dist_matrix [best_tour [i ]][best_tour [i +1 ]]

        print ("\nTour: ",end ="")
        print (" -> ".join ([city_names [c ]for c in best_tour ]))
        print (f"\nOptimal Cost = {actual_cost :.2f}")

        print ("\n"+"-"*40 )
        print ("TOUR BREAKDOWN")
        print ("-"*40 )
        for i in range (len (best_tour )-1 ):
            from_city =best_tour [i ]
            to_city =best_tour [i +1 ]
            cost =dist_matrix [from_city ][to_city ]
            print (f"  {city_names [from_city ]} -> {city_names [to_city ]}: {cost :.2f}")
        print (f"  {'='*30 }")
        print (f"  Total: {actual_cost :.2f}")
    else :
        print ("\nNo feasible tour found.")

    return best_tour ,best_cost 

def parse_distance_matrix (filename ):

    try :
        with open (filename ,'r',encoding ='utf-8-sig')as f :
            lines =f .readlines ()

        if not lines :
            print ("Error: File is empty")
            return None 

        n =len (lines )
        dist_matrix =[]
        INF =float ('inf')

        for i ,line in enumerate (lines ):
            values =line .strip ().split ()
            if len (values )!=n :
                print (f"Error: Row {i } has {len (values )} values, expected {n }")
                return None 

            row =[]
            for val in values :
                if val .lower ()in ['inf','-1']:
                    row .append (INF )
                else :
                    try :
                        row .append (float (val ))
                    except ValueError :
                        print (f"Error: Invalid value '{val }' in matrix")
                        return None 
            dist_matrix .append (row )

        return dist_matrix 

    except FileNotFoundError :
        print (f"Error: File '{filename }' not found")
        return None 
    except Exception as e :
        print (f"Error reading file: {e }")
        return None 

def tsp_menu ():

    print ("\n"+"="*80 )
    print ("TRAVELLING SALESMAN PROBLEM")
    print ("="*80 )

    print ("\nInput method:")
    print ("1. Manual Input")
    print ("2. Load from File (problem.txt)")

    choice =get_int_input ("\nEnter choice (1-2): ")

    INF =float ('inf')

    if choice ==1 :
        n =get_int_input ("Enter number of cities: ")

        print ("\nEnter city names (or press Enter for numbers):")
        city_names =[]
        for i in range (n ):
            name =input (f"  City {i +1 } name: ").strip ()
            city_names .append (name if name else str (i +1 ))

        print (f"\nEnter distance matrix ({n }x{n }):")
        print ("Use 'inf' or -1 for no direct path, 0 for same city")

        dist_matrix =[]
        for i in range (n ):
            row =[]
            for j in range (n ):
                if i ==j :
                    row .append (INF )
                else :
                    val =input (f"  Distance from {city_names [i ]} to {city_names [j ]}: ").strip ()
                    if val .lower ()=='inf'or val =='-1':
                        row .append (INF )
                    else :
                        row .append (float (val ))
            dist_matrix .append (row )

    elif choice ==2 :
        print ("\nLoading distance matrix from 'problem.txt'...")
        dist_matrix =parse_distance_matrix ('problem.txt')
        if dist_matrix is None :
            print ("Failed to load distance matrix from file.")
            print ("\nExpected format:")
            print ("  Space-separated square matrix")
            print ("  Use 'inf' or '-1' for no direct path")
            print ("\nExample:")
            print ("  inf 10 15 20")
            print ("  10 inf 35 25")
            print ("  15 35 inf 30")
            print ("  20 25 30 inf")
            return 

        n =len (dist_matrix )
        print (f"\nLoaded {n }x{n } distance matrix")

        city_names =[]
        for i in range (n ):
            name =input (f"  City {i +1 } name (or press Enter): ").strip ()
            city_names .append (name if name else str (i +1 ))

    else :
        print ("Invalid choice.")
        return 

    input ("\nPress Enter to solve TSP...")
    solve_tsp_branch_and_bound (dist_matrix ,city_names )

def solve_01_knapsack (weights ,values ,capacity ,item_names =None ):

    n =len (weights )

    if item_names is None :
        item_names =[f"Item {i +1 }"for i in range (n )]

    print ("\n"+"#"*80 )
    print ("   0/1 KNAPSACK PROBLEM - DYNAMIC PROGRAMMING")
    print ("#"*80 )

    print ("\n"+"="*80 )
    print ("PROBLEM DATA")
    print ("="*80 )
    print (f"\nKnapsack Capacity: {capacity }")
    print (f"\nItems:")
    print (f"{'Item':<15} {'Weight':<10} {'Value':<10} {'Value/Weight':<12}")
    print ("-"*47 )
    for i in range (n ):
        ratio =values [i ]/weights [i ]if weights [i ]>0 else float ('inf')
        print (f"{item_names [i ]:<15} {weights [i ]:<10} {values [i ]:<10} {ratio :<12.2f}")

    print ("\n"+"="*80 )
    print ("DYNAMIC PROGRAMMING APPROACH")
    print ("="*80 )
    print ("\nRecurrence Relation:")
    print ("  V[i][w] = max(V[i-1][w], V[i-1][w-wi] + vi)  if wi <= w")
    print ("  V[i][w] = V[i-1][w]                          if wi > w")
    print ("\nWhere:")
    print ("  V[i][w] = max value using items 1..i with capacity w")
    print ("  wi = weight of item i")
    print ("  vi = value of item i")

    V =[[0 for _ in range (capacity +1 )]for _ in range (n +1 )]

    print ("\n"+"="*80 )
    print ("BUILDING DP TABLE")
    print ("="*80 )

    for i in range (1 ,n +1 ):
        item_idx =i -1 
        wi =weights [item_idx ]
        vi =values [item_idx ]

        print (f"\n{'-'*60 }")
        print (f"Processing {item_names [item_idx ]} (weight={wi }, value={vi })")
        print (f"{'-'*60 }")

        for w in range (capacity +1 ):
            if wi >w :
                V [i ][w ]=V [i -1 ][w ]
                if w <=10 or w ==capacity :
                    print ("  V[{}][{}] = V[{}][{}] = {} (item too heavy)".format (i ,w ,i -1 ,w ,V [i ][w ]))
            else :
                exclude =V [i -1 ][w ]
                include =V [i -1 ][w -wi ]+vi 
                V [i ][w ]=max (exclude ,include )

                if w <=10 or w ==capacity :
                    print ("  V[{}][{}] = max(V[{}][{}], V[{}][{}] + {})".format (i ,w ,i -1 ,w ,i -1 ,w -wi ,vi ))
                    print (f"         = max({exclude }, {V [i -1 ][w -wi ]} + {vi })")
                    print (f"         = max({exclude }, {include }) = {V [i ][w ]}")

    print ("\n"+"="*80 )
    print ("DP TABLE V[i][w]")
    print ("="*80 )

    header ="Item\\Cap "
    cols_to_show =list (range (min (11 ,capacity +1 )))
    if capacity >10 :
        cols_to_show .append (capacity )

    for w in cols_to_show :
        header +=f"{w :>6}"
    print (header )
    print ("-"*len (header ))

    for i in range (n +1 ):
        if i ==0 :
            row_str =f"{'None':<9}"
        else :
            row_str =f"{item_names [i -1 ][:8 ]:<9}"

        for w in cols_to_show :
            row_str +=f"{V [i ][w ]:>6}"
        print (row_str )

    print ("\n"+"="*80 )
    print ("BACKTRACKING TO FIND SELECTED ITEMS")
    print ("="*80 )

    selected =[]
    w =capacity 

    print (f"\nStarting from V[{n }][{capacity }] = {V [n ][capacity ]}")

    for i in range (n ,0 ,-1 ):
        if V [i ][w ]!=V [i -1 ][w ]:
            item_idx =i -1 
            selected .append (item_idx )
            print ("\n  V[{}][{}] = {} != V[{}][{}] = {}".format (i ,w ,V [i ][w ],i -1 ,w ,V [i -1 ][w ]))
            print (f"  -> {item_names [item_idx ]} is SELECTED")
            print (f"  -> Remaining capacity: {w } - {weights [item_idx ]} = {w -weights [item_idx ]}")
            w -=weights [item_idx ]
        else :
            print ("\n  V[{}][{}] = {} = V[{}][{}]".format (i ,w ,V [i ][w ],i -1 ,w ))
            print (f"  -> {item_names [i -1 ]} is NOT selected")

    selected .reverse ()

    print ("\n"+"="*80 )
    print ("OPTIMAL SOLUTION")
    print ("="*80 )

    total_weight =sum (weights [i ]for i in selected )
    total_value =sum (values [i ]for i in selected )

    print (f"\nSelected Items:")
    print (f"{'Item':<15} {'Weight':<10} {'Value':<10}")
    print ("-"*35 )
    for i in selected :
        print (f"{item_names [i ]:<15} {weights [i ]:<10} {values [i ]:<10}")
    print ("-"*35 )
    print (f"{'TOTAL':<15} {total_weight :<10} {total_value :<10}")

    print (f"\nMaximum Value = {total_value }")
    print (f"Total Weight = {total_weight } (Capacity = {capacity })")

    return total_value ,selected 

def solve_unbounded_knapsack (weights ,values ,capacity ,item_names =None ):

    n =len (weights )

    if item_names is None :
        item_names =[f"Item {i +1 }"for i in range (n )]

    print ("\n"+"#"*80 )
    print ("   UNBOUNDED KNAPSACK - DYNAMIC PROGRAMMING")
    print ("#"*80 )

    print ("\n"+"="*80 )
    print ("PROBLEM DATA")
    print ("="*80 )
    print (f"\nKnapsack Capacity: {capacity }")
    print (f"\nItems (unlimited quantity):")
    print (f"{'Item':<15} {'Weight':<10} {'Value':<10} {'Value/Weight':<12}")
    print ("-"*47 )
    for i in range (n ):
        ratio =values [i ]/weights [i ]if weights [i ]>0 else float ('inf')
        print (f"{item_names [i ]:<15} {weights [i ]:<10} {values [i ]:<10} {ratio :<12.2f}")

    print ("\n"+"="*80 )
    print ("DYNAMIC PROGRAMMING APPROACH")
    print ("="*80 )
    print ("\nRecurrence Relation:")
    print ("  V[w] = max(V[w], V[w-wi] + vi) for all items i where wi <= w")
    print ("\nWhere:")
    print ("  V[w] = max value achievable with capacity w")
    print ("  Can use each item unlimited times")

    V =[0 ]*(capacity +1 )
    item_used =[[] for _ in range (capacity +1 )]

    print ("\n"+"="*80 )
    print ("BUILDING DP TABLE")
    print ("="*80 )

    for w in range (1 ,capacity +1 ):
        for i in range (n ):
            if weights [i ]<=w :
                new_value =V [w -weights [i ]]+values [i ]
                if new_value >V [w ]:
                    V [w ]=new_value 
                    item_used [w ]=item_used [w -weights [i ]]+[i ]
                    if w <=10 or w ==capacity :
                        print (f"  V[{w }] updated to {V [w ]} by adding {item_names [i ]}")

    print ("\n"+"="*80 )
    print ("DP VALUES")
    print ("="*80 )
    print (f"\n{'Capacity':<10} {'Max Value':<10}")
    print ("-"*20 )
    for w in range (0 ,min (11 ,capacity +1 )):
        print (f"{w :<10} {V [w ]:<10}")
    if capacity >10 :
        print ("...")
        print (f"{capacity :<10} {V [capacity ]:<10}")

    from collections import Counter 
    item_counts =Counter (item_used [capacity ])

    print ("\n"+"="*80 )
    print ("OPTIMAL SOLUTION")
    print ("="*80 )

    total_weight =sum (item_counts [i ]*weights [i ]for i in item_counts )
    total_value =V [capacity ]

    print (f"\nSelected Items:")
    print (f"{'Item':<15} {'Quantity':<10} {'Weight':<10} {'Value':<10}")
    print ("-"*45 )
    for i in sorted (item_counts .keys ()):
        qty =item_counts [i ]
        w =qty *weights [i ]
        v =qty *values [i ]
        print (f"{item_names [i ]:<15} {qty :<10} {w :<10} {v :<10}")
    print ("-"*45 )
    print (f"{'TOTAL':<15} {'':<10} {total_weight :<10} {total_value :<10}")

    print (f"\nMaximum Value = {total_value }")
    print (f"Total Weight = {total_weight } (Capacity = {capacity })")

    return total_value ,item_counts 

def parse_knapsack_problem (filename ='problem.txt'):

    try :
        with open (filename ,'r',encoding ='utf-8-sig')as f :
            lines =[line .strip ()for line in f .readlines ()if line .strip ()]

        if not lines :
            print (f"Error: File '{filename }' is empty")
            return None 

        capacity =int (lines [0 ])

        weights =[]
        values =[]
        item_names =[]

        for i ,line in enumerate (lines [1 :],start =1 ):
            parts =line .split ()
            if len (parts )==2 :
                weights .append (int (parts [0 ]))
                values .append (int (parts [1 ]))
                item_names .append (f"Item {i }")
            elif len (parts )==3 :
                weights .append (int (parts [0 ]))
                values .append (int (parts [1 ]))
                item_names .append (parts [2 ])
            else :
                print (f"Error: Invalid format on line {i +1 }: {line }")
                return None 

        if not weights :
            print ("Error: No items found in file")
            return None 

        return {
            'capacity':capacity ,
            'weights':weights ,
            'values':values ,
            'item_names':item_names ,
            'n':len (weights )
        }

    except FileNotFoundError :
        print (f"Error: File '{filename }' not found")
        return None 
    except ValueError as e :
        print (f"Error parsing file: {e }")
        return None 
    except Exception as e :
        print (f"Error reading file: {e }")
        return None 

def knapsack_menu ():

    print ("\n"+"="*80 )
    print ("KNAPSACK PROBLEM")
    print ("="*80 )

    print ("\nSelect type:")
    print ("1. 0/1 Knapsack (Dynamic Programming)")
    print ("2. Unbounded Knapsack (Dynamic Programming)")

    type_choice =get_int_input ("\nEnter choice (1-2): ")

    print ("\nInput method:")
    print ("1. Manual Input")
    print ("2. Load from File (problem.txt)")

    input_choice =get_int_input ("\nEnter choice (1-2): ")

    if input_choice ==1 :
        n =get_int_input ("Enter number of items: ")
        capacity =get_int_input ("Enter knapsack capacity: ")

        weights =[]
        values =[]
        item_names =[]

        for i in range (n ):
            name =input (f"Enter name for item {i +1 } (or press Enter): ").strip ()
            item_names .append (name if name else f"Item {i +1 }")
            weights .append (get_int_input (f"  Weight of {item_names [i ]}: "))
            values .append (get_int_input (f"  Value of {item_names [i ]}: "))

    elif input_choice ==2 :
        print ("\nLoading knapsack problem from 'problem.txt'...")
        problem =parse_knapsack_problem ('problem.txt')
        if problem is None :
            print ("Failed to load problem from file.")
            print ("\nExpected format:")
            print ("  Line 1: Capacity")
            print ("  Line 2+: Weight Value [ItemName]")
            print ("\nExample:")
            print ("  50")
            print ("  10 60 Item1")
            print ("  20 100 Item2")
            print ("  30 120 Item3")
            return 

        capacity =problem ['capacity']
        weights =problem ['weights']
        values =problem ['values']
        item_names =problem ['item_names']
        n =problem ['n']

        print (f"\nLoaded {n } items with capacity {capacity }")
        print ("\nItems loaded:")
        for i in range (n ):
            print (f"  {item_names [i ]}: Weight={weights [i ]}, Value={values [i ]}")

    else :
        print ("Invalid choice.")
        return 

    input ("\nPress Enter to solve...")

    if type_choice ==1 :
        solve_01_knapsack (weights ,values ,capacity ,item_names )
    elif type_choice ==2 :
        solve_unbounded_knapsack (weights ,values ,capacity ,item_names )
    else :
        print ("Invalid knapsack type.")

def dijkstra_shortest_path (dist_matrix ,start ,end ,node_names =None ):

    n =len (dist_matrix )
    INF =float ('inf')

    if node_names is None :
        node_names =[str (i )for i in range (n )]

    distances =[INF ]*n 
    distances [start ]=0 
    visited =[False ]*n 
    parent =[-1 ]*n 

    print ("\n"+"#"*80 )
    print ("   SHORTEST PATH - DIJKSTRA'S ALGORITHM")
    print ("#"*80 )

    print ("\n"+"="*80 )
    print ("PROBLEM")
    print ("="*80 )
    print (f"\nFind shortest path from {node_names [start ]} to {node_names [end ]}")

    print ("\n"+"="*80 )
    print ("DISTANCE MATRIX")
    print ("="*80 )

    max_name_len =max (len (name )for name in node_names )
    header =" "*(max_name_len +2 )+"".join ([f"{node_names [j ]:<8}"for j in range (n )])
    print ("\n"+header )
    print ("-"*len (header ))
    for i in range (n ):
        row_str =f"{node_names [i ]:<{max_name_len +2}}"
        for j in range (n ):
            val =dist_matrix [i ][j ]
            if val ==INF :
                row_str +="inf     "
            else :
                row_str +=f"{val :<8.1f}"
        print (row_str )

    print ("\n"+"="*80 )
    print ("DIJKSTRA'S ALGORITHM EXECUTION")
    print ("="*80 )

    for iteration in range (n ):
        min_dist =INF 
        u =-1 
        for i in range (n ):
            if not visited [i ]and distances [i ]<min_dist :
                min_dist =distances [i ]
                u =i 

        if u ==-1 or min_dist ==INF :
            break 

        visited [u ]=True 

        print (f"\nIteration {iteration +1 }:")
        print (f"  Select node {node_names [u ]} with distance {distances [u ]}")

        for v in range (n ):
            if not visited [v ]and dist_matrix [u ][v ]!=INF :
                new_dist =distances [u ]+dist_matrix [u ][v ]
                if new_dist <distances [v ]:
                    old_dist =distances [v ]
                    distances [v ]=new_dist 
                    parent [v ]=u 
                    print (f"    Update {node_names [v ]}: {old_dist } -> {new_dist } via {node_names [u ]}")

    print ("\n"+"="*80 )
    print ("SHORTEST PATH RESULT")
    print ("="*80 )

    if distances [end ]==INF :
        print (f"\nNo path exists from {node_names [start ]} to {node_names [end ]}")
        return INF ,[] 

    path =[]
    current =end 
    while current !=-1 :
        path .append (current )
        current =parent [current ]
    path .reverse ()

    print (f"\nPath: {' -> '.join ([node_names [i ]for i in path ])}")
    print (f"Total Distance: {distances [end ]}")

    print ("\nPath Details:")
    for i in range (len (path )-1 ):
        u ,v =path [i ],path [i +1 ]
        print (f"  {node_names [u ]} -> {node_names [v ]}: {dist_matrix [u ][v ]}")

    return distances [end ],path 

def solve_min_cost_path (grid ):

    rows =len (grid )
    cols =len (grid [0 ])

    print ("\n"+"#"*80 )
    print ("   MINIMUM COST PATH - RECURSIVE METHOD")
    print ("#"*80 )

    print ("\n"+"="*80 )
    print ("PROBLEM")
    print ("="*80 )
    print ("\nFind minimum cost path from top-left (0,0) to bottom-right")
    print ("Can only move RIGHT or DOWN")

    print ("\n"+"="*80 )
    print ("COST GRID")
    print ("="*80 )

    max_width =max (len (str (grid [i ][j ]))for i in range (rows )for j in range (cols ))

    print ("\n    "+"".join ([f"Col {j :<{max_width +2 }}"for j in range (cols )]))
    print ("    "+"-"*(cols *(max_width +4 )))
    for i in range (rows ):
        row_str =f"Row {i } | "
        for j in range (cols ):
            row_str +=f"{grid [i ][j ]:<{max_width +4 }}"
        print (row_str )

    print ("\n"+"="*80 )
    print ("RECURSIVE APPROACH WITH MEMOIZATION")
    print ("="*80 )
    print ("\nRecurrence Relation:")
    print ("  minCost(i, j) = grid[i][j] + min(minCost(i+1, j), minCost(i, j+1))")
    print ("\nBase Cases:")
    print ("  minCost(rows-1, cols-1) = grid[rows-1][cols-1]  (destination)")
    print ("  If out of bounds: return infinity")

    memo ={}
    call_log =[]
    call_tree =[]

    def min_cost_recursive (i ,j ,depth =0 ,prefix ="",is_last =True ):

        indent ="  "*depth 
        call_id =len (call_log )+1 

        call_info =f"{indent }Call #{call_id }: minCost({i }, {j })"

        if i >=rows or j >=cols :
            call_log .append (f"{call_info } -> INF (out of bounds)")
            tree_node =f"{prefix }({'`-- 'if is_last else '|-- '}minCost({i },{j }) = INF (out of bounds)"
            call_tree .append (tree_node )
            return float ('inf')

        if i ==rows -1 and j ==cols -1 :
            result =grid [i ][j ]
            call_log .append (f"{call_info } -> {result } (destination)")
            tree_node =f"{prefix }({'`-- 'if is_last else '|-- '}minCost({i },{j }) = {result } (BASE: destination)"
            call_tree .append (tree_node )
            return result 

        if (i ,j )in memo :
            call_log .append (f"{call_info } -> {memo [(i ,j )]} (from memo)")
            tree_node =f"{prefix }({'`-- 'if is_last else '|-- '}minCost({i },{j }) = {memo [(i ,j )]} (MEMO)"
            call_tree .append (tree_node )
            return memo [(i ,j )]

        call_log .append (f"{call_info }")
        tree_node =f"{prefix }({'`-- 'if is_last else '|-- '}minCost({i },{j })"
        call_tree .append (tree_node )

        new_prefix =prefix +("    "if is_last else "|   ")

        down =min_cost_recursive (i +1 ,j ,depth +1 ,new_prefix ,False )
        right =min_cost_recursive (i ,j +1 ,depth +1 ,new_prefix ,True )

        result =grid [i ][j ]+min (down ,right )
        memo [(i ,j )]=result 

        direction ="DOWN"if down <=right else "RIGHT"
        call_log .append (f"{indent }  -> minCost({i }, {j }) = {grid [i ][j ]} + min({down }, {right }) = {result } [go {direction }]")
        call_tree .append (f"{new_prefix }    => {grid [i ][j ]} + min({down }, {right }) = {result }")

        return result 

    print ("\n"+"="*80 )
    print ("RECURSIVE CALL TREE")
    print ("="*80 )

    optimal_cost =min_cost_recursive (0 ,0 ,0 ,"",True )

    print ("\nTree Structure:")
    for node in call_tree :
        print (node )

    print ("\n"+"="*80 )
    print ("RECURSIVE CALL TRACE (DETAILED)")
    print ("="*80 )

    print ()
    for log in call_log :
        print (log )

    print ("\n"+"="*80 )
    print ("BUILDING OPTIMAL PATH")
    print ("="*80 )

    path =[(0 ,0 )]
    i ,j =0 ,0 

    print (f"\nStarting at ({i }, {j }) with cost {grid [i ][j ]}")

    while i <rows -1 or j <cols -1 :
        if i ==rows -1 :
            j +=1 
            print (f"  -> Move RIGHT to ({i }, {j }), cost = {grid [i ][j ]}")
        elif j ==cols -1 :
            i +=1 
            print (f"  -> Move DOWN to ({i }, {j }), cost = {grid [i ][j ]}")
        else :
            down_cost =memo .get ((i +1 ,j ),float ('inf'))
            right_cost =memo .get ((i ,j +1 ),float ('inf'))

            if down_cost <=right_cost :
                i +=1 
                print (f"  -> Move DOWN to ({i }, {j }), cost = {grid [i ][j ]} (down path cost: {down_cost }, right path cost: {right_cost })")
            else :
                j +=1 
                print (f"  -> Move RIGHT to ({i }, {j }), cost = {grid [i ][j ]} (down path cost: {down_cost }, right path cost: {right_cost })")

        path .append ((i ,j ))

    print ("\n"+"="*80 )
    print ("PATH VISUALIZATION")
    print ("="*80 )

    path_set =set (path )

    print ("\n(* marks the optimal path)")
    print ()
    for i in range (rows ):
        row_str =""
        for j in range (cols ):
            if (i ,j )in path_set :
                row_str +=f"[{grid [i ][j ]:>2}]* "
            else :
                row_str +=f" {grid [i ][j ]:>2}   "
        print (row_str )

    print ("\n"+"="*80 )
    print ("OPTIMAL SOLUTION")
    print ("="*80 )

    print (f"\nOptimal Path: ",end ="")
    path_str =" -> ".join ([f"({i },{j })"for i ,j in path ])
    print (path_str )

    print (f"\nPath Cost Calculation:")
    costs =[grid [i ][j ]for i ,j in path ]
    print (f"  {' + '.join (map (str ,costs ))} = {sum (costs )}")

    print (f"\nMinimum Cost = {optimal_cost }")

    print ("\n"+"="*80 )
    print ("MEMOIZATION TABLE")
    print ("="*80 )

    print ("\nminCost[i][j] values:")
    print ("    "+"".join ([f"j={j :<6}"for j in range (cols )]))
    for i in range (rows ):
        row_str =f"i={i } "
        for j in range (cols ):
            if (i ,j )in memo :
                row_str +=f"{memo [(i ,j )]:<7}"
            else :
                row_str +=f"{'?':<7}"
        print (row_str )

    return optimal_cost ,path 

def min_cost_path_menu ():

    print ("\n"+"="*80 )
    print ("SHORTEST PATH PROBLEMS")
    print ("="*80 )

    print ("\nProblem type:")
    print ("1. Shortest Path between Two Nodes (Dijkstra)")
    print ("2. Visit All Nodes and Return (TSP from start node)")
    print ("3. Grid Path (Top-left to Bottom-right)")

    problem_type =get_int_input ("\nEnter choice (1-3): ")

    if problem_type ==1 or problem_type ==2 :

        print ("\nInput method:")
        print ("1. Manual Input")
        print ("2. Load from File (problem.txt)")

        choice =get_int_input ("\nEnter choice (1-2): ")

        INF =float ('inf')

        if choice ==1 :
            n =get_int_input ("Enter number of nodes: ")

            print ("\nEnter node names (or press Enter for numbers):")
            node_names =[]
            for i in range (n ):
                name =input (f"  Node {i +1 } name: ").strip ()
                node_names .append (name if name else str (i +1 ))

            print (f"\nEnter distance matrix ({n }x{n }):")
            print ("Use 'inf' or -1 for no direct path")

            dist_matrix =[]
            for i in range (n ):
                row =[]
                for j in range (n ):
                    if i ==j :
                        row .append (0 if problem_type ==1 else INF )
                    else :
                        val =input (f"  Distance from {node_names [i ]} to {node_names [j ]}: ").strip ()
                        if val .lower ()=='inf'or val =='-1':
                            row .append (INF )
                        else :
                            row .append (float (val ))
                dist_matrix .append (row )

        elif choice ==2 :
            print ("\nLoading distance matrix from 'problem.txt'...")
            dist_matrix =parse_distance_matrix ('problem.txt')
            if dist_matrix is None :
                print ("Failed to load distance matrix from file.")
                print ("\nExpected format:")
                print ("  Space-separated square matrix")
                print ("  Use 'inf' or '-1' for no direct path")
            
                return 

            n =len (dist_matrix )
            print (f"\nLoaded {n }x{n } distance matrix")

            node_names =[]
            for i in range (n ):
                name =input (f"  Node {i +1 } name (or press Enter): ").strip ()
                node_names .append (name if name else str (i +1 ))

        else :
            print ("Invalid choice.")
            return 

        if problem_type ==1 :
            print ("\nSelect starting node:")
            for i ,name in enumerate (node_names ):
                print (f"{i +1 }. {name }")
            start_idx =get_int_input (f"\nEnter choice (1-{len (node_names )}): ")-1 

            print ("\nSelect destination node:")
            for i ,name in enumerate (node_names ):
                if i !=start_idx :
                    print (f"{i +1 }. {name }")
            end_idx =get_int_input (f"\nEnter choice (1-{len (node_names )}): ")-1 

            if start_idx <0 or start_idx >=n or end_idx <0 or end_idx >=n :
                print ("Invalid node selection.")
                return 

            input ("\nPress Enter to find shortest path...")
            dijkstra_shortest_path (dist_matrix ,start_idx ,end_idx ,node_names )

        elif problem_type ==2 :
            print ("\nSelect starting node:")
            for i ,name in enumerate (node_names ):
                print (f"{i +1 }. {name }")
            start_idx =get_int_input (f"\nEnter choice (1-{len (node_names )}): ")-1 

            if start_idx <0 or start_idx >=n :
                print ("Invalid node selection.")
                return 

            print (f"\nSolving TSP starting from {node_names [start_idx ]}...")
            print ("(Visit all nodes and return to start)")

            input ("\nPress Enter to solve...")
            solve_tsp_branch_and_bound (dist_matrix ,node_names )

    elif problem_type ==3 :

        print ("\nInput method:")
        print ("1. Manual Input")
        print ("2. Load from File (problem.txt)")

        choice =get_int_input ("\nEnter choice (1-2): ")

        if choice ==1 :
            rows =get_int_input ("Enter number of rows: ")
            cols =get_int_input ("Enter number of columns: ")

            print (f"\nEnter the {rows }x{cols } grid:")
            grid =[]
            for i in range (rows ):
                row =[]
                for j in range (cols ):
                    val =get_int_input (f"  grid[{i }][{j }]: ")
                    row .append (val )
                grid .append (row )

        elif choice ==2 :
            print ("\nLoading grid from 'problem.txt'...")
            try :
                with open ('problem.txt','r',encoding ='utf-8-sig')as f :
                    lines =f .readlines ()
                grid =[]
                for line in lines :
                    row =[int (x )for x in line .strip ().split ()]
                    grid .append (row )

                if not grid :
                    print ("Error: File is empty")
                    return 

                rows =len (grid )
                cols =len (grid [0 ])
                if any (len (row )!=cols for row in grid ):
                    print ("Error: All rows must have same length")
                    return 

                print (f"\nLoaded {rows }x{cols } grid")
                print ("Grid:")
                for row in grid :
                    print (f"  {row }")

            except FileNotFoundError :
                print ("Error: File 'problem.txt' not found")
                return 
            except ValueError :
                print ("Error: Invalid grid format")
                return 
            except Exception as e :
                print (f"Error reading file: {e }")
                return 

        else :
            print ("Invalid choice.")
            return 

        input ("\nPress Enter to solve...")
        solve_min_cost_path (grid )

    else :
        print ("Invalid choice.")
        return

def main ():

    print ("\n"+"="*80 )
    print ("   OPERATIONS RESEARCH EXAM HELPER")
    print ("   Complete OR Problem Solver")
    print ("="*80 )

    while True :
        print ("\n"+"-"*50 )
        print ("MAIN MENU")
        print ("-"*50 )
        print ("\n--- LINEAR PROGRAMMING ---")
        print ("1.  Simplex Method (Manual Input)")
        print ("2.  Big M Method (Manual Input)")
        print ("3.  Dual Simplex Method")
        print ("4.  Auto-Detect Method (Manual Input)")
        print ("5.  Load from File (problem.txt)")
        print ("6.  Primal to Dual Conversion")
        print ("7.  Simplex with Matrix Method")

        print ("\n--- ASSIGNMENT & TRANSPORTATION ---")
        print ("8.  Assignment Problem (Hungarian Method)")
        print ("9.  Transportation Problem (MODI Method)")

        print ("\n--- SENSITIVITY ANALYSIS ---")
        print ("10. Sensitivity Analysis (Cases 1-5)")

        print ("\n--- INTEGER & COMBINATORIAL ---")
        print ("11. Integer Linear Programming (Branch & Bound)")
        print ("12. Travelling Salesman Problem (TSP)")
        print ("13. Knapsack Problem (0/1 & Unbounded)")
        print ("14. Shortest Path Problems (Dijkstra/Grid)")

        print ("\n--- EXIT ---")
        print ("15. Exit")
        print ("-"*50 )

        choice =get_int_input ("Enter your choice (1-15): ")

        if choice ==15 :
            print ("\nThank you for using OR Exam Helper. Good luck!")
            break 

        if choice not in range (1 ,15 ):
            print ("Invalid choice. Please try again.")
            continue 

        if choice ==11 :
            ilp_menu ()

            another =input ("\n\nDo you want to solve another problem? (y/n): ").lower ()
            if another !='y':
                print ("\nThank you for using OR Exam Helper. Good luck!")
                break 
            continue 

        if choice ==12 :
            tsp_menu ()

            another =input ("\n\nDo you want to solve another problem? (y/n): ").lower ()
            if another !='y':
                print ("\nThank you for using OR Exam Helper. Good luck!")
                break 
            continue 

        if choice ==13 :
            knapsack_menu ()

            another =input ("\n\nDo you want to solve another problem? (y/n): ").lower ()
            if another !='y':
                print ("\nThank you for using OR Exam Helper. Good luck!")
                break 
            continue 

        if choice ==14 :
            min_cost_path_menu ()

            another =input ("\n\nDo you want to solve another problem? (y/n): ").lower ()
            if another !='y':
                print ("\nThank you for using OR Exam Helper. Good luck!")
                break 
            continue 

        if choice ==10 :
            print ("\n"+"="*80 )
            print ("SENSITIVITY ANALYSIS")
            print ("="*80 )
            print ("\nThis requires solving an LP problem first.")
            print ("1. Manual Input")
            print ("2. Load from File (problem.txt)")

            sa_choice =get_int_input ("\nEnter choice (1-2): ")

            if sa_choice ==1 :
                problem =input_problem ()
            elif sa_choice ==2 :
                print ("\nLoading problem from 'problem.txt'...")
                problem =read_problem_from_file ('problem.txt')
                if problem is None :
                    print ("Failed to load problem from file.")
                    continue 
                print ("Problem loaded successfully!")
            else :
                print ("Invalid choice.")
                continue 

            table ,basic_vars ,var_names ,cj ,cb ,is_optimal =solve_and_prepare_sensitivity (problem )

            if is_optimal :
                result =sensitivity_analysis_menu (problem ,table ,basic_vars ,var_names ,cj ,cb ,is_optimal )
                if result :
                    table ,basic_vars ,var_names ,cj ,cb =result 

            another =input ("\n\nDo you want to solve another problem? (y/n): ").lower ()
            if another !='y':
                print ("\nThank you for using OR Exam Helper. Good luck!")
                break 
            continue 

        if choice ==9 :
            solve_transportation_problem ()

            another =input ("\n\nDo you want to solve another problem? (y/n): ").lower ()
            if another !='y':
                print ("\nThank you for using OR Exam Helper. Good luck!")
                break 
            continue 

        if choice ==8 :
            solve_hungarian_method ()

            another =input ("\n\nDo you want to solve another problem? (y/n): ").lower ()
            if another !='y':
                print ("\nThank you for using OR Exam Helper. Good luck!")
                break 
            continue 

        if choice ==3 :
            print ("\n"+"="*80 )
            print ("DUAL SIMPLEX METHOD")
            print ("="*80 )
            print ("\n1. Manual Input")
            print ("2. Load from File (problem.txt)")
            ds_choice =get_int_input ("Enter choice (1-2): ")

            if ds_choice ==1 :
                problem =input_problem ()
            elif ds_choice ==2 :
                print ("\nLoading problem from 'problem.txt'...")
                problem =read_problem_from_file ('problem.txt')
                if problem is None :
                    print ("Failed to load problem from file.")
                    continue 
                print ("Problem loaded successfully!")
            else :
                print ("Invalid choice.")
                continue 

            print_problem_summary (problem )

            print ("\n[!] NOTE: Dual Simplex is used when:")
            print ("  - All Zj-Cj >= 0 (optimal indicators)")
            print ("  - But some RHS < 0 (infeasible solution)")
            print ("  - Common with >= constraints converted to standard form")

            confirm =input ("\nContinue with Dual Simplex? (y/n): ").lower ()
            if confirm !='y':
                continue 

            solve_dual_simplex (problem )

            another =input ("\n\nDo you want to solve another problem? (y/n): ").lower ()
            if another !='y':
                print ("\nThank you for using OR Exam Helper. Good luck!")
                break 
            continue 

        if choice ==6 :
            print ("\n"+"="*80 )
            print ("PRIMAL TO DUAL CONVERSION")
            print ("="*80 )
            print ("\n1. Manual Input")
            print ("2. Load from File (problem.txt)")
            dual_choice =get_int_input ("Enter choice (1-2): ")

            if dual_choice ==1 :
                problem =input_problem ()
            elif dual_choice ==2 :
                print ("\nLoading problem from 'problem.txt'...")
                problem =read_problem_from_file ('problem.txt')
                if problem is None :
                    print ("Failed to load problem from file.")
                    continue 
                print ("Problem loaded successfully!")
            else :
                print ("Invalid choice.")
                continue 

            print_problem_summary (problem )
            input ("\nPress Enter to convert to dual and solve...")
            convert_to_dual_and_solve (problem )

            another =input ("\n\nDo you want to solve another problem? (y/n): ").lower ()
            if another !='y':
                print ("\nThank you for using OR Exam Helper. Good luck!")
                break 
            continue 

        if choice ==7 :
            print ("\n"+"="*80 )
            print ("SIMPLEX WITH MATRIX METHOD")
            print ("="*80 )
            print ("\n1. Manual Input")
            print ("2. Load from File (problem.txt)")
            matrix_choice =get_int_input ("Enter choice (1-2): ")

            if matrix_choice ==1 :
                problem =input_problem ()
            elif matrix_choice ==2 :
                print ("\nLoading problem from 'problem.txt'...")
                problem =read_problem_from_file ('problem.txt')
                if problem is None :
                    print ("Failed to load problem from file.")
                    continue 
                print ("Problem loaded successfully!")
            else :
                print ("Invalid choice.")
                continue 

            print_problem_summary (problem )

            if any (ct !=1 for ct in problem ['constraint_types']):
                print ("\n[!] NOTE: Matrix method works best with standard form (all <= constraints).")
                print ("The problem will be converted to standard form automatically.")

            input ("\nPress Enter to solve using Matrix Method...")
            solve_simplex_matrix_method (problem )

            another =input ("\n\nDo you want to solve another problem? (y/n): ").lower ()
            if another !='y':
                print ("\nThank you for using OR Exam Helper. Good luck!")
                break 
            continue 

        if choice ==5 :
            print ("\nLoading problem from 'problem.txt'...")
            problem =read_problem_from_file ('problem.txt')
            if problem is None :
                print ("Failed to load problem from file.")
                continue 
            print ("Problem loaded successfully!")
        else :
            problem =input_problem ()

        print_problem_summary (problem )

        if choice !=5 :
            confirm =input ("\nIs this correct? (y/n): ").lower ()
            if confirm !='y':
                print ("Please re-enter the problem.")
                continue 
        else :
            input ("\nPress Enter to solve...")

        if choice ==1 :
            if any (ct !=1 for ct in problem ['constraint_types']):
                print ("\n[!] WARNING: Simplex method requires all constraints to be <= type.")
                print ("Consider using Big M method for >= or = constraints.")
                proceed =input ("Do you want to continue anyway? (y/n): ").lower ()
                if proceed !='y':
                    continue 
            solve_simplex (problem )

        elif choice ==2 :
            solve_big_m (problem )

        elif choice in [4 ,5 ]:
            method =detect_method (problem )
            if method =="SIMPLEX":
                print ("\n"+"*"*80 )
                print ("AUTO-DETECTION: All constraints are <= type.")
                print ("This problem will be solved using SIMPLEX METHOD.")
                print ("*"*80 )
                input ("\nPress Enter to continue...")
                solve_simplex (problem )
            else :
                print ("\n"+"*"*80 )
                print ("AUTO-DETECTION: Problem contains >= or = constraints.")
                print ("This problem will be solved using BIG M METHOD.")
                print ("*"*80 )
                input ("\nPress Enter to continue...")
                solve_big_m (problem )

        another =input ("\n\nDo you want to solve another problem? (y/n): ").lower ()
        if another !='y':
            print ("\nThank you for using OR Exam Helper. Good luck!")
            break 

if __name__ =="__main__":
    main ()