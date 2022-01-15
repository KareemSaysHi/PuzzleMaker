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
        
    def is_overlapping(self, disassemble_matricies):
        empty_grid = np.zeros((3*self.grid_size_x, 3*self.grid_size_y), dtype=int)
        truth_matrix = np.zeros((3*self.grid_size_x, 3*self.grid_size_y), dtype=int)
        for i in range (0, len(disassemble_matricies)): #iterate through combinations of diassemble_matricies
            for j in range (i+1, len(disassemble_matricies)):
                truth_matrix = np.logical_and(disassemble_matricies[i], disassemble_matricies[j])
                if not np.array_equal(truth_matrix, empty_grid): #if two pieces overlap
                    return True #then say they do
        return False

    def make_state_matrix(self, disassemble_matricies):

        '''makes a grid that looks something like this:
        [0 0 0 0 0 0 0 0 0]
        [0 0 0 0 0 0 0 0 0]
        [0 0 1 1 1 0 3 3 0]
        [0 0 0 1 0 0 0 3 0]
        [0 0 0 1 0 2 2 0 0]
        [0 0 0 0 0 2 0 0 0]
        [0 0 4 0 0 2 0 0 0]
        [0 0 4 4 4 0 0 0 0]
        [0 0 0 0 4 0 0 0 0]''' 

        state_grid = np.zeros((3*self.grid_size_x, 3*self.grid_size_y), dtype=int)
        for piece_index in range (0, len(disassemble_matricies)):
            for y in range (0, 3*self.grid_size_y):
                for x in range (0, 3*self.grid_size_x):
                    if disassemble_matricies[piece_index][y][x] != 0:
                        state_grid[y][x] = piece_index + 1 #using + 1 because 0 needs to be empty
        return state_grid
        
    def is_piece_removed(self, disassemble_matrix):
        for y in range (self.grid_size_y, 2*self.grid_size_y):
            for x in range (self.grid_size_x, 2*self.grid_size_x):
                if disassemble_matrix[y][x] != 0:
                    return False
        return True

    def disassemble(self, ordered_piece_list, assembly_list): #import piece list from order list method, import assembly list from check assembly method

        #note: the first piece in orderd_piece_list will be fixed for now, only the other pieces will move
        disassemble_matricies = np.array([])
        for i in range (0, len(ordered_piece_list)):
            try:
                disassemble_matricies = np.append(disassemble_matricies, [ordered_piece_list[i].get_disassemble_matrix(self.grid_size_x, self.grid_size_y, assembly_list[i])], axis = 0) #add position to assembly_path
            except: #if disassemble path is empty:
                disassemble_matricies = np.array([ordered_piece_list[i].get_disassemble_matrix(3, 3, assembly_list[i])])
        
        current_state_matrix = self.make_state_matrix(disassemble_matricies)
        disassemble_path = np.array([current_state_matrix])
        solutions = self.recursive_disassembly(disassemble_matricies, disassemble_path)
        return solutions


    def recursive_disassembly(self, disassemble_matricies, disassemble_path):
        complete_disassemblies = []

        '''to note for np.roll: 
        doing np.roll(array, 1, axis = 1) rolls everything one to the right
        np.roll(array, -1, axis=1) rolls all one to left
        np.roll(array, 1, axis=0) rolls all down
        and np.roll(array. -1, axis=0) rolls all up'''
        depth = len(disassemble_path)
        for piece_index in range (1, len(disassemble_matricies)): #starts with 1 to avoid moving the fixed piece
            #print(piece_index)
            for direction in [-1, 1]: #can be either -1 down and left, or 1 up and right
                for axis in [0, 1]: #can be 0, which is up and down, or 1, which is left and right
                    #print(disassemble_matricies)
                    moved_piece = np.roll(disassemble_matricies[piece_index], direction, axis=axis) #shifts the matrix
                    moved_disassemble_matricies = np.copy(disassemble_matricies) #creating moved_dissassemble_matricies and changing the moved piece
                    moved_disassemble_matricies[piece_index] = moved_piece
                    
                    
                    if not self.is_overlapping(moved_disassemble_matricies): #if the piece movement is valid:
                        #add the movement to the disassembly-path
                        current_state_matrix = self.make_state_matrix(moved_disassemble_matricies)

                        notrepeated = True #this is a variable that checks if this state has already been reached
                        for move in disassemble_path:
                            if np.array_equal(current_state_matrix, move): #if we've gotten to this position before:
                                notrepeated = False #we've already gotten to this state then


                        if notrepeated: #if this is a new state
                            disassemble_path = np.append(disassemble_path, [current_state_matrix], axis=0) #add it to the disassemble path                       
                            #now see if the piece is out:
                            if self.is_piece_removed(moved_piece): #there might be an issue if two pieces come out together, don't worry about it for now
                                moved_disassemble_matricies = np.delete(moved_disassemble_matricies, piece_index, axis=0) #delete the taken out matrix
                                if len(moved_disassemble_matricies) == 1: #everything is out
                                    return disassemble_path #this is the possible disassembly from this path
                            #and now recurse up
                            recursive_results = self.recursive_disassembly(moved_disassemble_matricies, disassemble_path)

                            #update the recursively building list
                            #print ("here are the recursive results")
                            #print (recursive_results)

                            if isinstance(recursive_results, list): #if you're returned a list of solutions
                                for wayout in recursive_results:
                                    complete_disassemblies.append(wayout)
                            else:
                                complete_disassemblies.append(recursive_results)
                            #print("here is the complete disassemblies")
                            #print (complete_disassemblies)
                            disassemble_path = np.delete(disassemble_path, -1, axis=0)

        return complete_disassemblies
        

''' how do i want to do this:

- setup disassemble:
    - import an assembly, the same format as the assembler
    - for each piece, make a movement matrix, of grid size + (grid size on both sides), so in the case of 3x3 i want a 9x9 on both sides
    - place piece in corresponding part it's 9x9 matrix




'''
#solve_check_orange()