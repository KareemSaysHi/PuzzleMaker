from solver import Solver
from piece import Piece
import numpy as np

#note pieces are a 7x7 since 3x3 + 2 on each side

piecea = Piece()
piecea.set_shape(np.array([
    [1, 0, 1], 
    [1, 0, 1], 
    [1, 0, 1], 
    ]))

print("my symmetry matrix looks like this")
print(piecea.get_symmetry_matrix())
    
pieceb = Piece()
pieceb.set_shape(np.array([
    [1, 1]
    ]))

#print(piecea.get_symmetry_matrix())

solve = Solver() #instantiate solver class
solve.set_problem([piecea, pieceb]) #set pieces

assembly_solutions = solve.check_assemblies()
print("aaaaaaaaaaaaaaaaaaa")
print(assembly_solutions[0])
print(assembly_solutions[1])
#solve.solve_problem() #actually solve the problem

''' 
to do:
- make a checker that checks num of solutions
- make a linear solver

'''

'''
planning the assembly checker:
- choose first piece, put it arbitrarely
- choose second piece, rotate it around, see if it fits
'''

