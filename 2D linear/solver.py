import numpy as np

class Solver:
    
    def __init__(self):
        self.pieces = np.array([])
        self.grid_size_x = 3
        self.grid_size_y = 3


    def set_problem(self, input_pieces):
        self.pieces = input_pieces
        self.pieces = self.order_pieces()
    
    def get_ordered_pieces_list(self):
        return self.pieces
        
    def check_assemblies(self):
        empty_grid = np.zeros((self.grid_size_x, self.grid_size_y), dtype=int)
        empty_assembly_path = np.array([]) #three-dimensional array
        results = self.recursive_assembly(empty_grid, 0, empty_assembly_path)
        return results[0], results[1] #do the assembly

    
    #tested, works
    def order_pieces(self): #sorts the pieces in order from largest to smallest (for assembly efficiency)
        ordered_list = np.array([])
        for piece in self.pieces:
            if len(ordered_list) == 0:
                ordered_list = np.array([piece]) #sticks the first piece in 
            else:
                for i in ordered_list:
                    print(piece.get_size())
                    print(i.get_size())
                    if piece.get_size() > i.get_size(): #put the new piece where it belongs into the list
                        np.insert(ordered_list, i, piece, axis = 0) 
                        break
                else: #if it's smaller than everything else, just stick it to the end
                    ordered_list = np.append(ordered_list, [piece])
            print(ordered_list)
        return ordered_list
       
    
    def recursive_assembly(self, current_grid, current_piece_index, assembly_path):
        
        empty_grid = np.zeros((self.grid_size_x, self.grid_size_y), dtype=int)

        running_assembly_count = 0 #this is the assembly count for this node on the tree, going down
        running_assembly_list = np.array([])

        print ("-----------------------------------") 
        print ("working on piece " + str(current_piece_index))
        
        print("grid size")
        print (self.grid_size_y) 

        print("piece y length")
        print (self.pieces[current_piece_index].get_y_length())

        print ("piece x length")
        print(self.pieces[current_piece_index].get_x_length())

        for rotation in range (0, 4):
            if (current_piece_index != 0 and self.pieces[current_piece_index].get_symmetry_matrix()[rotation] == 0) or (current_piece_index == 0 and rotation == 0): #this is two cases: if we're on the first piece, we don't want to rotate it since it's the reference, and then if it's not the first one then just follow the symmetry matrix
                rotated_piece = self.pieces[current_piece_index].get_rotated(rotation) #gives an instance of the rotated piece by 90*rotation degrees
                print("this piece has been rotated " + str(rotation*90) + " degrees counterclockwise and now has shape")
                print (rotated_piece.get_shape())
        
                for y in range (0, 1 + self.grid_size_y - rotated_piece.get_y_length()): #positioning top left corner of piece in y, you need the one since 3-3=0, one place
                    for x in range (0, 1 + self.grid_size_x - rotated_piece.get_x_length()): #positiong top left corner of piece in x
                        
                        print("putting piece in position")
                        print([x, y])

                        new_grid = np.zeros((self.grid_size_x, self.grid_size_y), dtype=int) #the one we will be editing, adding a new piece to

                        #then this is "standard" stuff
                        for p_y in range (0, rotated_piece.get_y_length()):
                            for p_x in range (0, rotated_piece.get_x_length()): #this is for loop purgatory :P
                                print(p_x)
                                print(p_y)
                                new_grid[y+p_y][x+p_x] = rotated_piece.get_shape()[p_y][p_x] #put piece into empty array
                        
                        print("I am inputting the piece in like this")
                        print(new_grid)

                        print("Here is the truth grid between the current grid and the new grid")
                        print (np.logical_and(new_grid, current_grid))

                        if np.array_equal((np.logical_and(new_grid, current_grid)), empty_grid): #if the piece fits into our "current grid"
                            try:
                                current_assembly_path = np.append(assembly_path, [[x, y, rotation*90]], axis=0) #add position to assembly_path
                            except: #if assembly_path is empty, it will throw an error:
                                current_assembly_path = np.array([[x, y, rotation*90]])
                            
                            print ("this is the current assembly_path")
                            print (current_assembly_path)

                            if current_piece_index == len(self.pieces) - 1: #beacuse of zero indexing, was that the last piece?
                                running_assembly_count += 1 #add to assembly count
                                print ("running assembly count is now")
                                print(running_assembly_count)

                                print("running assembly list before appending")
                                print(running_assembly_list)

                                try:
                                    running_assembly_list = np.append(running_assembly_list, [current_assembly_path], axis=0) #add complete path to assembly list
                                except: #if running assembly list is empty, it will throw an error:
                                    running_assembly_list = np.array([current_assembly_path])
                                
                                print("running assembly list after appending")
                                print(running_assembly_list)
                            
                            else: #if that wasn't the last piece:
                                current_grid = np.logical_or(new_grid, current_grid) #update current grid by putting piece in
                                print(current_grid)

                                next_level_up = self.recursive_assembly(current_grid, current_piece_index + 1, current_assembly_path)

                                running_assembly_count += next_level_up[0] #add to running assembly count
                                print("this is the running assembly list")
                                print(running_assembly_list)

                                try:
                                    running_assembly_list = np.append(running_assembly_list, next_level_up[1], axis=0) #add to running assembly list
                                except: #if running assembly list is empty, it will throw an error:
                                    running_assembly_list = np.array(next_level_up[1])

        
        return running_assembly_count, running_assembly_list

    def disassemble(self, piece_list, assembly_list): #import piece list from order list method, import assembly list from check assembly method
        for i in range (0, len(piece_list)):
            print(piece_list[i].get_disassemble_matrix(3, 3, assembly_list[i]))

''' how do i want to do this:

- setup disassemble:
    - import an assembly, the same format as the assembler
    - for each piece, make a movement matrix, of grid size + (grid size on both sides), so in the case of 3x3 i want a 9x9 on both sides
    - place piece in corresponding part it's 9x9 matrix




'''
