from solver import Solver
from piece import Piece
import numpy as np

#note pieces are a 7x7 since 3x3 + 2 on each side

piecea = Piece()
piecea.set_shape(np.array([
    [1, 0, 0], 
    [1, 0, 0], 
    [1, 0, 0], 
    ]))

#print("my symmetry matrix looks like")
#print(piecea.get_symmetry_matrix())
    
pieceb = Piece()
pieceb.set_shape(np.array([
    [1, 1],
    [0, 1]
    ]))

#print(piecea.get_symmetry_matrix())

solve = Solver() #instantiate solver class
solve.set_problem([piecea, pieceb]) #set pieces

ordered_piece_list = solve.get_ordered_pieces_list()
assembly_list =  np.array([[0, 0, 0], [1, 1, 90]])
solutions = solve.disassemble(ordered_piece_list, assembly_list)
print(solutions)




#assembly_solutions = solve.check_assemblies()
#print("ok here's the solutions we got")
#print(assembly_solutions[0])
#print(assembly_solutions[1])
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

