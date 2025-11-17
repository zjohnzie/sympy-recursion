This library is a work in progress at the moment so DO. NOT. USE. (at the moment)

This library will enable users to find general solutions to homogenous, linear difference equations
whenever any symbolic representations exist, using the Sympy library. Additional functions will
enable the option to solve for specific IVP conditions of the inputted difference equation. 

Currently, all formatting for inputs are described in the comments of each function. 
But briefly, the solver_main function considers two principal arguments in the form of:
  1. The linear difference equation, represented currently as either a Sympy expression or as an array of the constant multiplicative terms. (Will show example later)
  2. The initial conditions, represented currently as an array of the constant values (will work on adding a dictionary if desired)

...where the output will be a sympy (or Latex if specified) expression that corresponds to either the general or specific solution to the equation.
