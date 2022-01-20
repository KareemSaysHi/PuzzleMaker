import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import keyboard
import time

class AssemblerDisplay():
    def __init__(self, assemblies):
        self.assemblies = assemblies #list of assemble matricies, [[[]]] <- each one
        self.colorlist = ["red", "orange", "yellow"]
    
    def transform3d(self, assemblematrix): #makes 3x3 into 3x3x3 with empty x areas
        return np.append(np.array([assemblematrix]), np.array([[[0, 0, 0],[0, 0, 0],[0, 0, 0]], [[0, 0, 0],[0, 0, 0],[0, 0, 0]]]), axis=0) 
    
    def colorData(self, assemblematrix3d): #need to run transform3d beforehand        
        shape = np.shape(assemblematrix3d) 

        colors = np.empty([shape[0], shape[1], shape[2]], dtype=object)
        for x in range (0, shape[0]):
            for y in range (0, shape[1]):
                for z in range (0, shape[2]):
                    state_matrix_data = assemblematrix3d[x][y][z]
                    if state_matrix_data != 0:
                        colors[x][y][z] = self.colorlist[state_matrix_data-1]

        return colors



    def displayAssemblies(self):
        counter = 0
        plt.ion() #make plot interactive
        voxelplot = plt.figure()
        ax = voxelplot.add_subplot((111), projection='3d') #makes subplot

        ax.grid(True) #just formatting

        ax.set_xlim3d([0, 3]) #still formatting
        ax.set_ylim3d([0, 3])
        ax.set_zlim3d([0, 3])

        ax.set_xticks([0, 1, 2, 3]) #stillll formatting
        ax.set_yticks([0, 1, 2, 3])
        ax.set_zticks([0, 1, 2, 3])
        ax.set_box_aspect((1, 1, 1))
        
        update = True

        while True:
        #add a line here to iterate through the different matricies
            if keyboard.is_pressed('left'):
                counter -= 1
                if counter < 0: #wrap around
                    counter += len(self.assemblies)
                update = True
            if keyboard.is_pressed('right'):
                counter += 1
                if counter >= len(self.assemblies): #wrap around
                    counter -= len(self.assemblies)
                update = True
            
            if update:
                assemblematrix = self.assemblies[counter]
                assemblematrix3d = self.transform3d(assemblematrix)
                colors = self.colorData(assemblematrix3d)
                ax.voxels(assemblematrix3d, facecolors = colors) #makes voxel plot with data
                plt.title("Assembly " + str(counter+1) + " out of " + str(len(self.assemblies)))

                ax.grid(True) #just formatting again

                ax.set_xlim3d([0, 3]) #still formatting
                ax.set_ylim3d([0, 3])
                ax.set_zlim3d([0, 3])

                ax.set_xticks([0, 1, 2, 3]) #stillll formatting
                ax.set_yticks([0, 1, 2, 3])
                ax.set_zticks([0, 1, 2, 3])
                ax.set_box_aspect((1, 1, 1))

                voxelplot.canvas.draw()
                voxelplot.canvas.flush_events()
                plt.cla()
                update = False


                



