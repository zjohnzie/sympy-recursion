import sympy
import numpy as np

def euler_formula(theta):
    return sympy.cos(theta) + sympy.I*(sympy.sin(theta))

def ivp_calculation(ivp_input):
    if type(ivp_input) is list:
        arr = np.array(ivp_input)
        if arr.ndim > 2:
            print("This is a 3-dimensional or higher tensor! This is not the correct data form!\n")
            return
        elif arr.ndim == 1:
            print("this is not a matrix bruh\n")
            return
            
        elif arr.shape[0] == 1 or arr.shape[1] == 1:
            print("bruh this is a vector, not an effin matrix")
            print("ill deal with this later as an assumed form of [f0, f1, ...] k?\n")
            return
        else:
            print(":?\n")
        matrix = sympy.Matrix(arr)
        print(f"Original matrix is: {matrix}")
        matrix = matrix.rref()[0]
        print(f"Solved matrix is: {matrix}")
        print('\n')

        return matrix # TO BE CHANGED; NEED TO FIGURE OUT PROPER/BETTER FORM FOR IVP INPUTS AND OUTPUTS
        


def recursion_calculation(input_form):
    sol_eq = sympy.sympify(0)
    print(sol_eq)
    if type(input_form) is list:
        print(input_form)
        print(str(len(input_form)) + " is the length of the list")
        print(str(input_form.count(0)) + " is the number of zeroes")

        if len(input_form) > 5:
            print("Cannot find symbolic roots of any quintics (at least now)\n")
        else:
            print("Will do calculations!\n")
            x, n = sympy.symbols('x n')
            expr = sympy.sympify(0)
            idx = 0

            arr = np.array(input_form)
            add_cnst = np.nonzero(arr)[0][-1]
                
            for coef in input_form:
            #f_temp = sympy.symbols('f' + str(idx))
                expr += coef*(x**(-idx+add_cnst))
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



## Test Cases
recursion_calculation([1,-2])

recursion_calculation([1,0,1])

recursion_calculation([1,5,2])

recursion_calculation([1,-4,3])

recursion_calculation([2,0,1,3,])

recursion_calculation([0,1,1])

recursion_calculation([1,0,2,2])

recursion_calculation([1,-2,3,4,1])

recursion_calculation([1,-2,3,4,1,1])

recursion_calculation([1,0,0,0,1,2,4,0,5])

ivp_calculation([1,1])

ivp_calculation([[1],[2]])

ivp_calculation([[1,0,1],[11,0,2],[1,1,1]])

f0, f1, f2, f3, f4 = sympy.symbols('f0 f1 f2 f3 f4')

sqrt5 = sympy.sqrt(5)

ivp_calculation([[1,1,0,0,1,f0],[0,-sqrt5,1,1,1-(1+sqrt5)/2,f1],[0,-sqrt5,4,2,-(1+sqrt5)/2,f2],[0,-2*sqrt5,9,3,-2*(1+sqrt5)/2,f3],[0,-3*sqrt5,16,4,-1-3*(1+sqrt5)/2,f4]])


