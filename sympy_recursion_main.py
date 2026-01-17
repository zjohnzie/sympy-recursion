### Dependencies
import sympy
import numpy as np
import re # may remove this...


def euler_formula(theta):
    return sympy.cos(theta) + sympy.I*(sympy.sin(theta))


def matrix_to_solution(matrix, *args, **kwargs):
    """
    Takes in a matrix (either as a list or a numpy array)
    and outputs a sympy expression corresponding to a homogenous linear difference equation
    i think?
    """
    sol = sympy.sympify(0)

    if isinstance(matrix,list):
        if all(isinstance(item, (int, float)) for item in matrix):
            matrix = np.array(matrix)
    #print(f"Matrix shape is: {matrix.shape}")
    #print(f"Matrix dimension is: {matrix.ndim}")
    if (matrix.ndim == 2 and (matrix.shape[0] == 1 or matrix.shape[1] == 1)) or matrix.ndim == 1:
            
        idx = 0
        for entry in matrix:

            c_temp = sympy.symbols("c" + str(idx))
            if not isinstance(entry, (sympy.Add, sympy.Mul)):
                if entry != None:
                    sol += c_temp * sympy.sympify(entry)
                    idx += 1
            else:
                sol += c_temp * entry
    else:
        # FIGURE OUT IF POSSIBLE TO GUARANTEE FINDING SOLUTION FROM IVP MATRIX!!!
        print(f"MAT 1: Not currently able to deal with full IVP matrices")
        return 

    return sol


def expression_to_sequence(sym_expr, *args, **kwargs):
    """
    Takes a sympy expression as input and outputs a list representation of the expression
    Currently just ignores any constant terms but could be updated to print a warning message
    """
    if isinstance(sym_expr, sympy.Add):
        seq = [0]
        seq_var_char = ""
        for term in sympy.Add.make_args(sym_expr):
            #print(f"Current term is: {term}")
            #print(f"List of symbols in this term are: {list(term.free_symbols)}")
            idx = -1
            var_count = 0
            if isinstance(term, sympy.Mul) or isinstance(term, sympy.Symbol):
                term_coefs = sympy.sympify(1)
                for term2 in sympy.Mul.make_args(term):
                    #print(f"Current factor is: {term2}")
                    if isinstance(term2, sympy.Symbol):
                        #print(f" Current factor, {term2}, is a symbol!")
                        term2_str = str(term2)
                        if term2_str[0].isalpha() and len(term2_str) >= 2:
                            if seq_var_char == "" or seq_var_char == term2_str[0]:
                                if var_count <= 0:
                                    var_count += 1
                                    if term2_str[1:].isdecimal():
                                        idx = int(term2_str[1:])
                                    elif term2_str[0].isalpha() and term2_str[1] in "-_":
                                        if term2_str[2] == "{" and term2_str[-1] == "}":
                                            if term2_str[3:-2].isdecimal():
                                                idx = int(term2_str[3:-2])
                                        elif term2_str[2:].isdecimal():
                                            idx = int(term2_str[2:])
                                        else:
                                            print(f"EXPR 3: Erroneous notation for index of {term2} symbol")
                                            term_coefs *= term2
                                    if seq_var_char == "":
                                        seq_var_char = term2_str[0]
                                else:
                                    print(f"EXPR 4: {term} is a nonlinear difference term or is abusing notation!")
                                    term_coefs *= term2
                        else:
                            term_coefs *= term2
                    else:
                        term_coefs *= term2
                if idx >= 0:
                    if idx > len(seq)-1:
                        sub_seq = [0] * (idx - (len(seq)-1))
                        seq.extend(sub_seq)
                    seq[idx] = term_coefs
                            
                            

            else:
                print(f" Current term, {term}, is not a linear product!")
        return seq
            
    else:
        print(f"EXPR 1: Input is either not of the form of a proper homogenous linear difference equation or is not a sympy expression at all!")
        return []


def solution_to_matrix(gen_sol, *args, **kwargs):

    """
     NEEDS REWRITE BADLY!!!
     Takes in a given general solution in the form of a sympy expression
     And outputs a square matrix for solving a given set of initial values,
     where the i,j-th entry corresponds to the j-th term of the given solution
     without the generalized constant in front with the value of n substituted for i+1
    
     The rationale is that this matrix, A, satisfies:
     \vec{f} = A\vec{b}
     where f_{i} = c_{0}*term_{0}(i) + c_{1}*term_{1}(i) + ... + c_{n}*term_{n}(i)
     and b_{i} = c_{i}

    """
    try:
        sol_seq = expression_to_sequence(gen_sol)
        print(sol_seq)
        vector = [0] * len(sol_seq)
        matrix = [vector] * len(sol_seq)
        print(matrix)
        matrix = sympy.Matrix(matrix)
        print(matrix)
        print(sol_seq[0].free_symbols)
        n = sympy.symbols("n")
        #print(sol_seq[2].subs(n, 2))
        for idx1 in range(len(sol_seq)):
            idx2 = 0
            for term in sol_seq:
                print(idx1)
                print(term)
                matrix[idx1, idx2] = term.subs(n, idx1)
                idx2 += 1
        print(matrix)
        

        '''
            if term/cnst_term == term.subs(cnst_term,1): #checks linearity
                if matrix[idx_num] == None:
                    matrix[idx_num] = term/cnst_term
                elif isinstance(matrix[idx_num],int):
                    matrix[idx_num] += term/cnst_term
                elif isinstance(matrix[idx_num],sympy.Add):
                    matrix[idx_num] += term/cnst_term
                else:
                    print("MTX 4: wtf kinda matrix you making")
                    return
        '''
                    
        if not args:
            general_mat = matrix
            return general_mat
        else:
            if isinstance(args, (list, tuple)):
                arg_check = args
                if len(args) == 1:
                    arg_check = args[0]
                    print(f"\n HERES CHECKING THE ARGUMENT: {arg_check}\n")
                if all(isinstance(arg, (int, float)) for arg in arg_check):
                    if len(arg_check) == len(sol_seq):
                        specific_mat = matrix.col_insert(len(sol_seq), sympy.Matrix(arg_check))
                        return specific_mat
                    else:
                        print("SOL 1: Your IVP input isn't the same length as the number of constants to determine!")
                else:
                    print("SOL 2: Your IVP input isn't a matrix or list of integers!")
            else:
                print("SOL 3: Your IVP input is not of the appropriate data type")
            return matrix
    except Exception as e:
        print(f"SOL 1: {e}")
            
                
def ivp_calculation(matrix,ivp_input=[]):
    """
     IVP Input form being a matrix should be structured with the vector equation below satisfied:
     \vec{f} = A\vec{b}
     where f_{i} = c_{0}*term_{0}(i) + c_{1}*term_{1}(i) + ... + c_{n}*term_{n}(i)
     so that the constants, c_{j}, can be solved using row reduction and returned as a list
    """
    sympyFlag = False


    if isinstance(matrix, np.ndarray):
        arr = sympy.Matrix(matrix)
        sympyFlag = True
    elif isinstance(matrix, sympy.Matrix):
        arr = matrix
        sympyFlag = True
    else:
        try:
            arr = sympy.Matrix(matrix)
            sympyFlag = True
        except Exception as e:
            print(f"IVP 8: {e}")
        
    if sympyFlag:
        if len(sympy.shape(arr)) > 2:
            print("IVP 1: This is a 3-dimensional or higher tensor! This is not the correct data form!\n")
            return
        elif len(sympy.shape(arr)) == 1:
            print("IVP 2: this is not a matrix bruh\n")
            return
            
        elif sympy.shape(arr)[0] == 1 or sympy.shape(arr)[1] == 1:
            print("IVP 3: bruh this is a vector, not an effin matrix")
            print("ill deal with this later as an assumed form of [f0, f1, ...] k?\n")
            return
        else:
            print("IVP 4: :?\n")
        if sympy.shape(arr)[1] == len(ivp_input) and sympy.shape(arr)[0] == sympy.shape(arr)[1]:
            arr.col_insert(len(ivp_input), sympy.Matrix(ivp_input))
        else:
            print(f"IVP 7: Your initial values don't have the proper number to determine a unique solution")
            # Work on adding support for ivp input that follows the structure of a dictionary for a given indexed value
        if (len(ivp_input) == 0 and (abs(sympy.shape(arr)[0] - sympy.shape(arr)[1]) == 1)):           
            
            print(f"IVP 5: Original matrix is: {arr}")
            solved_matrix = arr.rref()[0]
            print(f"Solved matrix is: {solved_matrix}")
            print("\n")

            constants = []
            for idx in range(solved_matrix.rows):
                row = solved_matrix.row(idx)
                print(row)
                if list(row).count(0) == len(row)-2 and row[idx] != 0:
                    constants.append(row[-1]/row[idx])
                else:
                    print("IVP 6: Your constants are not linearly independent from at least how you've sent them to me!")

        print(constants)
                

        return constants
  

def recursion_solver(input_form):
    sol_eq = sympy.sympify(0)
    #print(sol_eq)
    
    if isinstance(input_form, np.ndarray):
        arr = input_form
    elif isinstance(input_form, list): #idk how this would happen but including it anyways
        arr = np.array(input_form)

    if arr.size > 5:
        print("REC 1: Cannot find symbolic roots of any quintics (at least now)\n")
    else:
        print("REC 2: Will do calculations!\n")
        x, n = sympy.symbols('x n')
        expr = sympy.sympify(0)
            
        idx = 0
        #print(f"Array is: {arr}")
        #print(f"Nonzero entries are: {np.nonzero(arr)}")
        nz_arr = np.nonzero(arr)
        if len(nz_arr[0]) > 0:
            add_cnst = np.nonzero(arr)[0][-1]
                
        for coef in input_form:
            expr += coef*(x**(-idx+add_cnst)) #This needs an explanation imo
            idx += 1

        imRootFlag = False
        idx = 0
        for root in sympy.roots(expr):
            if imRootFlag:
                imRootFlag = False
                continue
            if not root.is_real:
                imRootFlag = True
                c_temp = sympy.symbols("c" + str(idx))
                c_temp2 = sympy.symbols("c" + str(idx+1))
                a = sympy.re(root)
                b = sympy.im(root)
                sol_eq += c_temp*sympy.cos(n*sympy.acos(a/sympy.sqrt(a**2 + b**2))) + c_temp2*sympy.sin(n*sympy.Abs(sympy.asin(b/sympy.sqrt(a**2 + b**2))))
                idx += 2
            else:
                c_temp = sympy.symbols("c" + str(idx))
                sol_eq += c_temp*(root**n)
                idx += 1

            #print("\n")

    #print(sol_eq)
    #print("\n")
    return sol_eq


def recursion_format_processing(input_form, *args, **kwargs):
    """
     Vector format for recursion solving should be a row vector
     with the i-th entry corresponding to the constant multiple of the f_{n-i} term of the recursive sequence equation 
     The FINAL output will be a symbolic expression corresponding to the general real solution to the homogenous equation
    
     If a specific solution is desired over the general solution,
     the vector format will require two row vectors where the second vector should have 
     specified values corresponding to the value of f_{0}, f_{1}, and so on.
    
     String format should either be text corresponding to latex or sympy code
    
     Sympy format ignores variables not of the form of "f_{n-k}" or "f(n-k)" or "f_n-k"
     where f can be any string of characters that are either first encountered
     or are the 
     Sympy format could also work independently of the choice of symbols for your variables
     and just read left-to-right interpreting the i-th encountered variable as the f_{n-i} term
    """
    # Could implement sympy ignore_name flag in parameters for this
    # Can work on seeing if a given set of initial conditions are sufficient to specify an entire solution
    # as this seems plausible under certain structures of the sequence relation

    #print(type(input_form))
    ivp_arr = []
    if isinstance(input_form, list):
        if len(input_form) == 2:
            if isinstance(input_form[0], list):
                if isinstance(input_form[1], list):
                    if (all(isinstance(item, (int, float))) for item in input_form[0]):
                        if (all(isinstance(item, (int, float))) for item in input_form[1]):
                            ivp_arr = np.array(input_form[1])
                            input_form = np.array(input_form[0])
                            #print(f"Your list is now proper with the sequence: {input_form} and the IVPs of: {ivp_arr}")
                            return input_form, ivp_arr, True
                        else:
                            print(f"PROC 5: Your input list does not have the proper structure in index 1 for a IVP array")
                            return np.array([]), np.array([]), False
                    else:
                        print(f"PROC 6: Your input list does not have the proper structure in index 0 for a symbolic sequence")
                        return np.array([]), np.array([]), False

        if all(isinstance(item, (int, float)) for item in input_form):
            input_form = np.array(input_form)
        else:
            print(f"PROC 7: Your input list is neither in the proper form of a list, having just numbers or two proper nested lists for IVP array and symbolic sequence list")
            return np.array([]), np.array([]), False

    if isinstance(input_form, np.ndarray):
        if input_form.ndim == 1:
            #print(f"This input has the following vector: {input_form}\n")
            return input_form, np.array([]), True
        elif input_form.ndim == 2:
            # PROBABLY NEED TO ADD A CHECK FOR PROPER SHAPE OF THESE VECTORS!!!
            #print(f"The input has the following two vectors: {input_form[0]} and {input_form[1]}\n")
            return input_form[0], input_form[1], True
        elif input_form.ndim > 2:
            print("PROC 1: Your input has too many input rows in your numpy array\n")
            
    elif isinstance(input_form, str):
        input_form = sympy.parsing.sympy_parser.parse_expr(input_form)
        print(input_form)
        input_form = expression_to_sequence(input_form)
        return np.array(input_form), np.array([]), True
        
    elif isinstance(input_form, sympy.Expr):
        input_form = expression_to_sequence(input_form)
        return np.array(input_form), np.array([]), True
        
    print("PROC 4: Improper format for inputs given, returning empty lists/arrays")
    print(f"Length of improper array is {len(input_form)}")
    return np.array([]),np.array([]), False 


def sym_recursion_solver_main(sequence, *args, **kwargs):
    """
        Insert docstrings here
    """
    try:
        print("\n~~~\nWe're doing this main baby!!!\n~~~")
        #print(f"Current sequence is: {sequence}")
        sequence_proper, ivp_seq_proper, proper_flag = recursion_format_processing(sequence)
        if proper_flag:
            gen_expression = recursion_solver(sequence_proper)
            if ivp_seq_proper.size == 0:
                if sequence_proper.size == 0:
                    print("MAIN 1: Your sequence is empty buddy!!")
                    return sequence_proper
                else:
                    #print(f"Matrix representation is: {solution_to_matrix(gen_expression)}")
                    #expr_check = matrix_to_solution(solution_to_matrix(gen_expression))
                    #print(f"Expression check gives: {expr_check}")
                    #print(f"Expression check diff gives: {expr_check - sequence}")
                    return gen_expression
            else:
                # NEEDS WORK DONE ASAP!!!
                print("MAIN 3: CURRENTLY NOT WORKING OHMIGOSH IM SO SAWRRY")
                print(f"Specific solution *should* be: {ivp_calculation([gen_expression,ivp_seq_proper])}")
        else:
            print("MAIN 2: Your sequence is not an accepted format!")
    except Exception as err:
        print(f"MAIN 4: Your sequence was unable to be solved due to the following error: {err}")
        
