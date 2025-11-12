import sympy
import numpy as np

def euler_formula(theta):
    return sympy.cos(theta) + sympy.I*(sympy.sin(theta))



def ivp_calculation(ivp_input):
    if type(ivp_input) is list:
        
        ### IVP Input form being a matrix should be structured with the vector equation below satisfied:
        ### \vec{f} = A\vec{b}
        ### where f_{i} = c_{0}*term_{0}(i) + c_{1}*term_{1}(i) + ... + c_{n}*term_{n}(i)
        ### so that the constants, c_{j}, can be solved using row reduction and returned as a list
        
        arr = np.array(ivp_input)
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
    listFlag = False
    if isinstance(input_form, np.ndarray):
        arr = input_form
    elif isinstance(input_form, list): #idk how this would happen but including it anyways
        listFlag = True
        arr = np.array(input_form)

    if arr.size > 5:
        print("REC 1: Cannot find symbolic roots of any quintics (at least now)\n")
    else:
        print("REC 2: Will do calculations!\n")
        x, n = sympy.symbols('x n')
        expr = sympy.sympify(0)
            
        idx = 0
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
        

    return np.array([]),np.array([]), False 



def sym_recursion_solver_main(sequence, *args, **kwargs):
    print("We're doing this main baby!!!")
    sequence_proper, ivp_proper, proper_flag = recursion_format_processing(sequence)
    gen_solution = recursion_solver(sequence_proper)
    if proper_flag:
        if ivp_proper.size == 0:
            if sequence_proper.size == 0:
                print("MAIN 1: Your sequence is empty buddy!!")
                return sequence_proper
            else:
                return gen_solution
        else:
            # NEEDS WORK DONE ASAP!!!
            print("MAIN 3: CURRENTLY NOT WORKING OHMIGOSH IM SO SAWRRY")
            return ivp_calculation(ivp_proper)
    else:
        print("MAIN 2: Your sequence is not an accepted format!")
        
    
    
## Test Cases


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


