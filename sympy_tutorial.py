import sympy
import numpy

def euler_formula(theta):
    return sympy.cos(theta) + sympy.I*(sympy.sin(theta))


x, y, f0, f1, f2, f3, f4 = sympy.symbols('x y f0 f1 f2 f3 f4')
expr = x + 2*y
print(expr)


print(x*expr)
expanded_expr = sympy.expand(x*expr)
print(expanded_expr)

print(sympy.factor(expanded_expr))

equation = sympy.Eq(x+1,4)

print(equation)

print(sympy.simplify(expanded_expr - x*expr))

expr2 = sympy.cos(x) + 1

print(expr2)

print(expr2.subs(x,sympy.pi/6))

sqrt5 = sympy.sqrt(5)

print(sqrt5)

matrix = sympy.Matrix([[1,1,0,0,1,0],[0,-sqrt5,1,1,1-(1+sqrt5)/2,1],[0,-sqrt5,4,2,-(1+sqrt5)/2,5],[0,-2*sqrt5,9,3,-2*(1+sqrt5)/2,14],[0,-3*sqrt5,16,4,-1-3*(1+sqrt5)/2,35]])

print(matrix)

print(matrix.rref())

matrix2 = sympy.Matrix([[1,1,0,0,1,f0],[0,-sqrt5,1,1,1-(1+sqrt5)/2,f1],[0,-sqrt5,4,2,-(1+sqrt5)/2,f2],[0,-2*sqrt5,9,3,-2*(1+sqrt5)/2,f3],[0,-3*sqrt5,16,4,-1-3*(1+sqrt5)/2,f4]])


print(matrix2.rref()[0].subs(f0,0).subs(f1,1).subs(f2,5).subs(f3,14).subs(f4,35))

print(matrix2.rref()[0].subs(f0,1).subs(f1,1).subs(f2,1).subs(f3,1).subs(f4,1))

print(sympy.factor(sympy.exp(2*sympy.pi*sympy.I/3)))

print(sympy.cos(2*sympy.pi/3) + sympy.I*(sympy.sin(2*sympy.pi/3)))

matrix_im = sympy.Matrix([[1,1,1,f0],[euler_formula(2*sympy.pi/3),euler_formula(4*sympy.pi/3),1,f1-sympy.Rational(2,3)],[euler_formula(4*sympy.pi/3),euler_formula(2*sympy.pi/3),1,f2-sympy.Rational(4,3)]])
print(matrix_im)

matrix_val = matrix_im.rref()[0].subs(f0,0).subs(f1,1).subs(f
rec_expr = matrix_val[0,3]*sympy.exp(2*sympy.pi*x/3) + matrix_val[1,3]*sympy.exp(4*sympy.pi*x/3) + matrix_val[2,3] + sympy.Rational(2,3)*x

print(rec_expr)
