### Dependencies
import sympy
import numpy as np
import re # may remove this...

def euler_formula(theta):
    return sympy.cos(theta) + sympy.I*(sympy.sin(theta))

def matrix_to_solution(matrix, *args, **kwargs):

    sol = sympy.sympify(0)

    if isinstance(matrix,list):
        matrix = np.array(matrix)
    print(f"Matrix shape is: {matrix.shape}")
    print(f"Matrix dimension is: {matrix.ndim}")
    if (matrix.ndim == 2 and (matrix.shape[0] == 1 or matrix.shape[1] == 1)) or matrix.ndim == 1:
            
        idx = 0
        for entry in matrix:

            c_temp = sympy.symbols('c' + str(idx))
            if not isinstance(entry, (sympy.Add, sympy.Mul)):
                if entry != None:
                    sol += c_temp * sympy.sympify(entry)
            else:
                sol += c_temp * entry
    else:
        # FIGURE OUT IF POSSIBLE TO GUARANTEE FINDING SOLUTION FROM IVP MATRIX!!!
        print(f"MAT 1: Not currently able to deal with full IVP matrices")
        return 

    return sol
        
        

def solution_to_matrix(gen_sol, *args, **kwargs):

    ### Takes in a given general solution in the form of a sympy expression
    ### And outputs a square matrix for solving a given set of initial values,
    ### where the i,j-th entry corresponds to the j-th term of the given solution
    ### without the generalized constant in front with the value of n substituted for i+1
    ###
    ### The rationale is that this matrix, A, satisfies:
    ### \vec{f} = A\vec{b}
    ### where f_{i} = c_{0}*term_{0}(i) + c_{1}*term_{1}(i) + ... + c_{n}*term_{n}(i)
    ### and b_{i} = c_{i}

    # Currently, this will only work on equations with less than 10 constants to be determined
    # Will need to rewrite with a new recursive function to deal with indices with more than 1 digit
    
    matrix = [None] * len(sympy.Add.make_args(gen_sol))
    print(sympy.Add.make_args(gen_sol))
    for term in sympy.Add.make_args(gen_sol):
        print(f"Current term is: {term}")
        cnst_term = sympy.sympify(0)
        for symbol in list(term.free_symbols):
            print(f"Current symbol is: {symbol}")
            idx_num = -1 # can this be moved outside of this loop?
            if str(symbol)[0] == 'c':
                if str(symbol)[1].isdigit():
                    idx_num = int(str(symbol)[1])
                elif str(symbol)[1] == '-' or str(symbol)[1] == '_':
                    if str(symbol)[2].isdigit():
                        idx_num = int(str(symbol)[2])
                    elif str(symbol)[2] == '{':
                        if str(symbol)[3].isdigit():
                            idx_num = int(str(symbol)[3]) # this method fails to check that the notation for the constant term is closed on the right side with a curly brace
                        else:
                            print("MTX 1: Your IVP constants don't have proper numerical indices!")
                    else:
                        print("MTX 2: Your notation does not follow either latex or the accepted notation of c_n")
                else:
                    print("MTX 3: The next following character after \'c\' should be a number, \'-\', or \'_\'!")

            if idx_num >= 0:
                cnst_term = symbol
                print("DO STUFF IM TIRED") # TO ADD AFTER RESTING !!!
                break
            
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
                
    if not args:
        # Convert list to matrix starting from n=0 to n=N
        general_mat = matrix
        return general_mat
    else:
        # Do specific code for given IVP input
        specific_mat = matrix
        return specific_mat
            
                
def ivp_calculation(matrix,ivp_input=[]):
    
    ### IVP Input form being a matrix should be structured with the vector equation below satisfied:
    ### \vec{f} = A\vec{b}
    ### where f_{i} = c_{0}*term_{0}(i) + c_{1}*term_{1}(i) + ... + c_{n}*term_{n}(i)
    ### so that the constants, c_{j}, can be solved using row reduction and returned as a list

    npFlag = False


    if isinstance(matrix, np.ndarray):
        arr = matrix
        npFlag = True
        
    if npFlag:
        if arr.ndim > 2:
            print("IVP 1: This is a 3-dimensional or higher tensor! This is not the correct data form!\n")
            return
        elif arr.ndim == 1:
            print("IVP 2: this is not a matrix bruh\n")
            return
            
        elif arr.shape[0] == 1 or arr.shape[1] == 1:
            print("IVP 3: bruh this is a vector, not an effin matrix")
            print("ill deal with this later as an assumed form of [f0, f1, ...] k?\n")
            return
        else:
            print("IVP 4: :?\n")
        if arr.matrix.shape[1] == len(ivp_input):
            arr = np.hstack((arr,np.array(ivp_input)))
        else:
            print(f"IVP 7: Your initial values don't have the proper number to determine a unique solution")
            # Work on adding support for ivp input that follows the structure of a dictionary for a given indexed value
        sp_matrix = sympy.Matrix(arr)
        print(f"IVP 5: Original matrix is: {sp_matrix}")
        sp_matrix = sp_matrix.rref()[0]
        print(f"Solved matrix is: {sp_matrix}")
        print('\n')

        constants = []
        for idx in range(sp_matrix.rows):
            row = sp_matrix.row(idx)
            print(row)
            if list(row).count(0) == len(row)-2 and row[idx] != 0:
                constants.append(row[-1]/row[idx])
            else:
                print("IVP 6: Your constants are not linearly independent from at least how you've sent them to me!")

        print(constants)
                

        return constants

        

def recursion_solver(input_form):
    sol_eq = sympy.sympify(0)
    print(sol_eq)
    
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
        print(f"Array is: {arr}")
        print(f"Nonzero entries are: {np.nonzero(arr)}")
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
                c_temp = sympy.symbols('c' + str(idx))
                c_temp2 = sympy.symbols('c' + str(idx+1))
                a = sympy.re(root)
                b = sympy.im(root)
                sol_eq += c_temp*sympy.cos(n*sympy.acos(a/sympy.sqrt(a**2 + b**2))) + c_temp2*sympy.sin(n*sympy.Abs(sympy.asin(b/sympy.sqrt(a**2 + b**2))))
                idx += 2
            else:
                c_temp = sympy.symbols('c' + str(idx))
                sol_eq += c_temp*(root**n)
                idx += 1

            print('\n')

    print(sol_eq)
    print('\n')
    return sol_eq



def recursion_format_processing(input_form, *args, **kwargs):
    
    ### Vector format for recursion solving should be a row vector
    ### with the i-th entry corresponding to the constant multiple of the f_{n-i} term of the recursive sequence equation 
    ### The FINAL output will be a symbolic expression corresponding to the general real solution to the homogenous equation
    ###
    ### If a specific solution is desired over the general solution,
    ### the vector format will require two row vectors where the second vector should have 
    ### specified values corresponding to the value of f_{0}, f_{1}, and so on.
    ###
    ### String format should either be text corresponding to latex or sympy code
    ###
    ### Sympy format ignores variables not of the form of "f_{n-k}" or "f(n-k)" or "f_n-k"
    ### where f can be any string of characters that are either first encountered
    ### or are the 
    ### Sympy format could also work independently of the choice of symbols for your variables
    ### and just read left-to-right interpreting the i-th encountered variable as the f_{n-i} term
    # Could implement sympy ignore_name flag in parameters for this
    # Can work on seeing if a given set of initial conditions are sufficient to specify an entire solution
    # as this seems plausible under certain structures of the sequence relation

    print(type(input_form))
    ivp_arr = []
    if isinstance(input_form, list):
        if len(input_form) == 2:
            if isinstance(input_form[0], list):
                ivp_arr = np.array(input_form[1])
                input_form = np.array(input_form[0])
                print(f"Your list is now proper with the sequence: {input_form} and the IVPs of: {ivp_arr}")
                return input_form, ivp_arr, True

        if all(isinstance(item, (int, float)) for item in input_form):
            input_form = np.array(input_form)
                

    if isinstance(input_form, np.ndarray):
        if input_form.ndim == 1:
            print(f"This input has the following vector: {input_form}\n")
            return input_form, np.array([]), True
        elif input_form.ndim == 2:
            # PROBABLY NEED TO ADD A CHECK FOR PROPER SHAPE OF THESE VECTORS!!!
            print(f"The input has the following two vectors: {input_form[0]} and {input_form[1]}\n")
            return input_form[0], input_form[1], True
        elif input_form.ndim > 2:
            print("PROC 1: Your input has too many input rows in your numpy array\n")
            
    elif isinstance(input_form, str):
        print("PROC 2: Working on text inputs bud!!!\n")

    elif isinstance(input_form, sympy.Add):
        print("PROC 3: Working on sympy inputs PAL\n")
        # need to test variety of sympy expression concepts as even 2*f0 is not consideredof the class "Add"
        
    print("PROC 4: Improper format for inputs given, returning empty lists/arrays")
    print(f"Length of improper array is {len(input_form)}")
    return np.array([]),np.array([]), False 



def sym_recursion_solver_main(sequence, *args, **kwargs):
    print("\nWe're doing this main baby!!!")
    print(f"Current sequence is: {sequence}")
    sequence_proper, ivp_seq_proper, proper_flag = recursion_format_processing(sequence)
    if proper_flag:
        gen_expression = recursion_solver(sequence_proper)
        if ivp_seq_proper.size == 0:
            if sequence_proper.size == 0:
                print("MAIN 1: Your sequence is empty buddy!!")
                return sequence_proper
            else:
                print(f"Matrix representation is: {solution_to_matrix(gen_expression)}")
                expr_check = matrix_to_solution(solution_to_matrix(gen_expression))
                print(f"Expression check gives: {expr_check}")
                #print(f"Expression check diff gives: {expr_check - sequence}")
                return gen_expression
        else:
            # NEEDS WORK DONE ASAP!!!
            print("MAIN 3: CURRENTLY NOT WORKING OHMIGOSH IM SO SAWRRY")
            print(f"Specific solution *should* be: {ivp_calculation([gen_expression,ivp_seq_proper])}")
    else:
        print("MAIN 2: Your sequence is not an accepted format!")
        
    
    
## Test Cases
'''

print(f"{recursion_format_processing([1,-2])}\n")

print(f"{recursion_format_processing([1,0,1])}\n")

print(f"{recursion_format_processing([1,5,2])}\n")

print(f"{recursion_format_processing([[1,2,3],[0,0,1]])}\n")

str_test = "test"
print(f"{recursion_format_processing(str_test)}\n")

sym_recursion_solver_main([1,-2])

print(len([[1,-2],[0]]))
print(f"IVP solution is: {sym_recursion_solver_main([[1,-2],[0]])}")

sym_recursion_solver_main([1,0,1])

sym_recursion_solver_main([1,5,2])

sym_recursion_solver_main([1,-4,3])

sym_recursion_solver_main([2,0,1,3,])

sym_recursion_solver_main([0,1,1])

sym_recursion_solver_main([1,0,2,2])

sym_recursion_solver_main([1,-2,3,4,1])

sym_recursion_solver_main([1,-2,3,4,1,1])

sym_recursion_solver_main([1,0,0,0,1,2,4,0,5])

ivp_calculation([1,1])

ivp_calculation([[1],[2]])

ivp_calculation([[1,0,1],[11,0,2],[1,1,1]])

f0, f1, f2, f3, f4 = sympy.symbols('f0 f1 f2 f3 f4')

sqrt5 = sympy.sqrt(5)

ivp_calculation([[1,1,0,0,1,f0],[0,-sqrt5,1,1,1-(1+sqrt5)/2,f1],[0,-sqrt5,4,2,-(1+sqrt5)/2,f2],[0,-2*sqrt5,9,3,-2*(1+sqrt5)/2,f3],[0,-3*sqrt5,16,4,-1-3*(1+sqrt5)/2,f4]])

sym_recursion_solver_main([[1,1,0,0,1,f0],[0,-sqrt5,1,1,1-(1+sqrt5)/2,f1],[0,-sqrt5,4,2,-(1+sqrt5)/2,f2],[0,-2*sqrt5,9,3,-2*(1+sqrt5)/2,f3],[0,-3*sqrt5,16,4,-1-3*(1+sqrt5)/2,f4]])

'''
