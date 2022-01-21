import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import keyboard
import time

class DisassemblerDisplay():
    def __init__(self, disassemblies):
        self.disassemblies = disassemblies #list of assemble matricies, [[[]]] <- each one
        self.colorlist = ["red", "orange", "yellow", "green", "blue"]
    
    def transform3d(self, disassemblematrix): #makes 9x9 into 9x9x9 
        disassemblematrix3d = np.zeros((9, 9, 9), dtype=int)
        disassemblematrix3d[5] = disassemblematrix
        print(disassemblematrix3d)
        return disassemblematrix3d
    
    def colorData(self, disassemblematrix3d): #need to run transform3d beforehand        
        shape = np.shape(disassemblematrix3d) 

        colors = np.empty([shape[0], shape[1], shape[2]], dtype=object)
        for x in range (0, shape[0]):
            for y in range (0, shape[1]):
                for z in range (0, shape[2]):
                    state_matrix_data = disassemblematrix3d[x][y][z]
                    if state_matrix_data != 0:
                        colors[x][y][z] = self.colorlist[state_matrix_data-1]

        return colors



    def displayDisassemblies(self): 
        path = 0
        depth = 0
        plt.ion() #make plot interactive
        voxelplot = plt.figure()
        ax = voxelplot.add_subplot((111), projection='3d') #makes subplot

        ax.grid(True) #just formatting

        ax.set_xlim3d([0, 9]) #still formatting
        ax.set_ylim3d([0, 9])
        ax.set_zlim3d([0, 9])

        ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) #stillll formatting
        ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        ax.set_zticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        ax.set_box_aspect((1, 1, 1))
        
        update = True

        while True:
            if keyboard.is_pressed('left'): #up/down should go deeper in the diassembly, left/right should switch to different paths
                path -= 1
                depth = 0
                if path < 0: #don't go past
                    path = 0
                update = True
            if keyboard.is_pressed('right'):
                path += 1
                depth = 0
                if path >= len(self.disassemblies): #don't go past
                    path = len(self.disassemblies) - 1
                update = True
            if keyboard.is_pressed('up'):
                depth -= 1
                if depth < 0: #don't go past
                    depth = 0
                update = True
            if keyboard.is_pressed('down'):
                depth += 1
                if depth >= len(self.disassemblies[path]): #don't go past
                    depth = len(self.disassemblies[path]) - 1
                update = True
            
            if update:
                disassemblematrix = self.disassemblies[path][depth]
                disassemblematrix3d = self.transform3d(disassemblematrix)
                colors = self.colorData(disassemblematrix3d)
                ax.voxels(disassemblematrix3d, facecolors = colors) #makes voxel plot with data
                plt.title("Disassembly " + str(path+1) + " of " + str(len(self.disassemblies)) + ", depth " + str(depth+1))

                ax.grid(True) #just formatting

                ax.set_xlim3d([0, 9]) #still formatting
                ax.set_ylim3d([0, 9])
                ax.set_zlim3d([0, 9])

                ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) #stillll formatting
                ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
                ax.set_zticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
                ax.set_box_aspect((1, 1, 1))

                voxelplot.canvas.draw()
                voxelplot.canvas.flush_events()
                plt.cla()
                update = False


                



