import numpy as np

class Piece():
    def __init__(self):
        self.shape = np.array([[]])
    
    def set_shape(self, piece_shape):
        self.shape = piece_shape #.astype(bool) #note: the shape of a piece nust be a rectangle
        if self.shape.ndim < 2: #if the shape is less than 2d (usually caused by rotation):
            self.shape = np.atleast_2d(self.shape)

    def get_shape(self):
        return self.shape

    def get_x_length(self):
        return len(self.shape[0])
    
    def get_y_length(self):
        return len(self.shape)

    def get_size(self):
        return self.shape.size        

    def get_rotated(self, numrot):
        rotated_piece = self
        print("before actually rotating in get rotated function, self now looks like")
        print(self.shape)
        print("and rotated_piece looks like")
        print(rotated_piece.shape)
        print("*")
        rotated_piece.set_shape(np.rot90(self.shape, numrot))
        print("in get rotated function, self now looks like")
        print(self.shape)
        print("and rotated_piece looks like")
        print(rotated_piece.shape)
        return rotated_piece

    def get_symmetry_matrix(self): #there are four ways to orient a piece in 2D, so check if rotations make it the same:
        symmetry_matrix = np.array([0, 0, 0, 0])
        for i in range (0, 4):
            for j in range (0, i): #j always less than i
                print("shape when not rotated at all")
                print(self.shape)
                print("shape i when rotated " + str(i*90) + " degrees counterclockwise looks like this")
                print(self.get_rotated(i).shape)
                print("shape j when rotated " + str(j*90) + " degrees counterclockwise looks like this")
                print(self.get_rotated(j).shape)
                if np.array_equal((self.get_rotated(i)).get_shape(), (self.get_rotated(j)).get_shape()): #states i and j are equal, so we just never check i
                    symmetry_matrix[i] = 1
        return symmetry_matrix