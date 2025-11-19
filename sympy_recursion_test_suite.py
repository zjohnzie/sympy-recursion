import sympy_recursion_main as srm


## Test Cases


print(f"{srm.recursion_format_processing([1,-2])}\n")

print(f"{srm.recursion_format_processing([1,0,1])}\n")

print(f"{srm.recursion_format_processing([1,5,2])}\n")

print(f"{srm.recursion_format_processing([[1,2,3],[0,0,1]])}\n")

str_test = "test"
print(f"{srm.recursion_format_processing(str_test)}\n")

srm.sym_recursion_solver_main([1,-2])

print(len([[1,-2],[0]]))
print(f"IVP solution is: {srm.sym_recursion_solver_main([[1,-2],[0]])}")

srm.sym_recursion_solver_main([1,0,1])

srm.sym_recursion_solver_main([1,5,2])

srm.sym_recursion_solver_main([1,-4,3])

srm.sym_recursion_solver_main([2,0,1,3,])

srm.sym_recursion_solver_main([0,1,1])

srm.sym_recursion_solver_main([1,0,2,2])

srm.sym_recursion_solver_main([1,-2,3,4,1])

srm.sym_recursion_solver_main([1,-2,3,4,1,1])

srm.sym_recursion_solver_main([1,0,0,0,1,2,4,0,5])

srm.ivp_calculation([1,1])

srm.ivp_calculation([[1],[2]])

srm.ivp_calculation([[1,0,1],[11,0,2],[1,1,1]])

#f0, f1, f2, f3, f4 = sympy.symbols('f0 f1 f2 f3 f4')

#sqrt5 = sympy.sqrt(5)

#ivp_calculation([[1,1,0,0,1,f0],[0,-sqrt5,1,1,1-(1+sqrt5)/2,f1],[0,-sqrt5,4,2,-(1+sqrt5)/2,f2],[0,-2*sqrt5,9,3,-2*(1+sqrt5)/2,f3],[0,-3*sqrt5,16,4,-1-3*(1+sqrt5)/2,f4]])

#sym_recursion_solver_main([[1,1,0,0,1,f0],[0,-sqrt5,1,1,1-(1+sqrt5)/2,f1],[0,-sqrt5,4,2,-(1+sqrt5)/2,f2],[0,-2*sqrt5,9,3,-2*(1+sqrt5)/2,f3],[0,-3*sqrt5,16,4,-1-3*(1+sqrt5)/2,f4]])
