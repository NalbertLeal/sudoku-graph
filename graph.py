import numpy as np
from copy import copy 

class Graph():
    def __init__(self, vertices_list=[]):
        self.vertices = np.array(vertices_list)
        self.edges = np.zeros(shape=(self.vertices.size, self.vertices.size))
        self.acceptable_colors = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    
        # variables to help to fill the edges matix
    
        sudoku_row_adj_bounds = [[0, 9], [9, 18], [18, 27], [27, 36], [36, 45], [45, 54], [54, 63], [63, 72], [72, 81]]
        sudoku_blocks = [
            [[0, 1, 2], [9, 10, 11], [18, 19, 20]],
            [[3, 4, 5], [12, 13, 14], [21, 22, 23]],
            [[6, 7, 8], [15, 16, 17], [24, 25, 26]],
            [[27, 28, 29], [36, 37, 38], [45, 46, 47]],
            [[30, 31, 32], [39, 40, 41], [48, 49, 50]],
            [[33, 34, 35], [42, 43, 44], [51, 52, 53]],
            [[54, 55, 56], [63, 64, 65], [72, 73, 74]],
            [[57, 58, 59], [66, 67, 68], [75, 76, 77]],
            [[60, 61, 62], [69, 70, 71], [78, 79, 80]],
        ]
        
        # now fill the edges matrix
        for i in range(0, self.edges.size):
            if i == 81:
                break
            # now we need to color the row adjacents of the vertice "i"
            # first we discover the vertices
            for row in sudoku_row_adj_bounds:
                if i >= row[0] and i < row[1]:
                    #  vertice "i" is in this line, so all the vertices
                    # with index between row[0] and row[1] are adjacents
                    # of "i"
                    for j in range(row[0], row[1]):
                        if i != j:
                            self.edges[i, j] = 1
            
            # now we need to color the columns adjacents of the vertice "i"
            for j in range(i, 81, 9):
                if i != j:
                    self.edges[i, j] = 1
            for j in range(i, 0, -9):
                if i != j:
                    self.edges[i, j] = 1
                    
            # now we need to color the sudoku blocks of adjacents of the vertice "i"
            is_this_block = False
            for block in sudoku_blocks:
                for block_row in block:
                    for index in block_row:
                        if index == i:
                            is_this_block = True
                            break
                    break
                if is_this_block:
                    for block_row in block:
                        for block_row in block:
                            for j in block_row:
                                if i != j:
                                    self.edges[i, j] = 1
                    break
                    

    def get_adjacents(self, vertice_index):
        """
          Using the self.edges return a np.array with the index of the 
        vertices that are adjacent of the "vertice_index" of the paramenter.
        """
        adjacents = []
        
        for j in range(0, self.vertices.size):
            if self.edges[vertice_index, j] == 1:
                adjacents.append(j)
        adjacents.sort()
        return np.array(adjacents)
    
    def adjacents_colors(self, vertice_index, local_vertices):
        """
          Receive the index of a vertice and return a np.array with the
        colors of the adjacents.
        """
        adjacents = self.get_adjacents(vertice_index)
        adjacents_colors = []
        for vertice in adjacents:
            if local_vertices[vertice] not in adjacents_colors:
                adjacents_colors.append(local_vertices[vertice])
        adjacents_colors.sort()
        adjacents_colors = [x for x in adjacents_colors if x != '0']
        return np.array(adjacents_colors)
    
    def vertice_degree(self, vertice_index, local_vertices):
        adjacents = self.adjacents_colors(vertice_index, local_vertices)
        return adjacents.size
    
    def incidence_degree(self, vertice_index, local_vertices):
        return self.vertice_degree(vertice_index, local_vertices)
    
    def vertice_saturation(self, vertice, local_vertices):
        return len(self.adjacents_colors(vertice, local_vertices))

    def greed(self):
        """
          Algorithm to color a graph in a greed way (almost brute force),
        in other words, this algorithm color te vertice with the fisrt 
        color that find.
        """
        vertices_number = self.vertices.size
        colors = copy(self.vertices)
        max_color_number = 9
        for vertice in range(0, vertices_number): # loop over all the vertices 
            if colors[vertice] != '0':
                continue
            ajd_colors_array = self.adjacents_colors(vertice, colors) # the colors of the adjacents
            expected_color = 1 # the counter of to the expected colors
            for adj_color in ajd_colors_array: # loop over the adjacents colors
                if adj_color != str(expected_color):
                    # if the expected color can be used to this vertice
                    colors[vertice] = str(expected_color) 
                    break
                else:
                    if expected_color == max_color_number:
                        return 'The vertice ' + str(vertice) + ' need more than 9 colors'
                        #raise Exception('The vertice ' + str(vertice) + ' need more than 9 colors')
                    expected_color += 1
        return colors
        
    def ldo(self):
        vertices_number = self.vertices.size
        colors = copy(self.vertices)
        colors_numbers = 1
        colored_vertices = 0
        while colored_vertices < vertices_number:
            max_degree = -1
            max_vertice = -1
            for vertice in range(0, vertices_number):
                vertice_color = colors[vertice]
                if vertice_color == '0': # vertice doesn't have color
                    vertice_degree = self.vertice_degree(vertice, colors)
                    if max_degree <= vertice_degree:
                        max_degree = vertice_degree
                        max_vertice = vertice
                    else:
                        if max_degree == vertice_degree:
                            if self.incidence_degree(vertice) == self.incidence_degree(max_degree):
                                max_degree = vertice_degree
                                max_vertice = vertice
            max_vertice_adjacent_colors = self.adjacents_colors(max_vertice, colors)
            expected_color = 1 # the counter of to the expected colors
            
            # colore o max_vertice com a menor cor disponivel
            to_color = [x for x in self.acceptable_colors if x not in max_vertice_adjacent_colors]
            if len(to_color) > 0:
                colors[max_vertice] = str(to_color[0])
            else:
                #  if don't have an color to this element, then append the result to the queue and then
                # raise an Exception to don't continue to loop over this element.
                return 'The LDO is locked in element ' + str(max_vertice)
                # raise Exception('The LDO is locked in element ' + str(max_vertice))
                    
            if colors[max_vertice] != '0':
                colored_vertices += 1
            if colors_numbers < expected_color:
                colors_numbers = expected_color
            if colors_numbers == 10:
                return 'Need more than 9 colors'
                # raise Exception('Need more than 9 colors')
        return colors
    
    def sdo(self):
        vertices_number = self.vertices.size
        colors = copy(self.vertices)
        colors_numbers = 1
        colored_vertices = 0
        while colored_vertices < vertices_number:
            bigest_saturation = -1
            most_satureted_vertice = -1
            for vertice in range(0, vertices_number):
                vertice_color = colors[vertice]
                if vertice_color == '0': # vertice doesn't have color
                    vertice_saturation = self.vertice_saturation(vertice, colors)
                    if bigest_saturation < vertice_saturation:
                        bigest_saturation = vertice_saturation
                        most_satureted_vertice = vertice
                    else:
                        if bigest_saturation == vertice_saturation:
                            if self.vertice_degree(vertice, colors) == self.vertice_degree(most_satureted_vertice, colors):
                                bigest_saturation = vertice_saturation
                                most_satureted_vertice = vertice
            # colore o max_vertice com a menor cor disponivel
            most_sat_vertice_adj_colors = self.adjacents_colors(most_satureted_vertice, colors)
            expected_color = 1 # the counter of to the expected colors
                    
            # colore o max_vertice com a menor cor disponivel
            to_color = [x for x in self.acceptable_colors if x not in most_sat_vertice_adj_colors]
            if len(to_color) > 0:
                colors[most_satureted_vertice] = str(to_color[0])
            else:
                #  if don't have an color to this element, then append the result to the queue and then
                # raise an Exception to don't continue to loop over this element.
                return 'The SDO is locked in element ' + str(most_satureted_vertice)
                # raise Exception('The SDO is locked in element ' + str(most_satureted_vertice))
            
            if colors[most_satureted_vertice] != '0':
                colored_vertices += 1
            if colors_numbers < expected_color:
                colors_numbers = expected_color
            if colors_numbers == 10:
                return 'Need more than 9 colors'
                # raise Exception('Need more than 9 colors')
        return colors

    def vertice_unssigned(self, row, col, vertices_colors):
        for i in range(0, len(vertices_colors)):
            for j in range(0, len(vertices_colors)):
                if str(vertices_colors[i][j]) == '0':
                    row[0] = i
                    col[0] = j
                    return False
        return True

    def is_safe(self, color, row, col, vertices_colors):
        for i in range(0, len(self.acceptable_colors)):
            if vertices_colors[row][i] == str(color):
                return False
        # try:
        for i in range(0, len(self.acceptable_colors)):
            if vertices_colors[i][col] == str(color):
                return False

        row_start = int(row/3)*3
        col_start = int(col/3)*3
        for i in range(row_start, row_start+3):
            for j in range(col_start, col_start+3):
                if vertices_colors[i][j] == str(color):
                    return False
        return True
        
        # except Exception as e:
        #     print(e)

    def __backtrack(self, vertices_colors):
        row = [0]
        col = [0]
        if self.vertice_unssigned(row, col, vertices_colors):
            return True
        row = row[0]
        col = col[0]
        for color in self.acceptable_colors:
            if self.is_safe(color, row, col, vertices_colors):
                vertices_colors[row][col] = str(color)
                if self.__backtrack(vertices_colors):
                    return True
                vertices_colors[row][col] = '0'
        return False

    def backtrack(self):
        temporary_vertices_list = []
        element_count = 0
        for i in range(0,9):
            temporary_vertices_list.append([])
            for j in range(0,9):
                temporary_vertices_list[i].append(self.vertices[element_count])
                element_count += 1
        vertices_colors = temporary_vertices_list

        if self.__backtrack(vertices_colors):
            return vertices_colors
        else:
            return "Backtrack failed"

    # def isColorSafe1(self, vertice_index, color, vertices_colors):
    #     adjacents_colors = self.adjacents_colors(vertice_index, vertices_colors)
    #     if color in adjacents_colors:
    #          return False
    #     else:
    #         return True

    # def __backtrack1(self, vertices_colors, vertice_index):
    #     if vertice_index == vertices_colors.size:
    #         return True
    #     vertice_color = vertices_colors[vertice_index]
    #     for color in self.acceptable_colors:
    #         if self.isColorSafe(vertice_index, color, vertices_colors):
    #             vertices_colors[vertice_index] = color
    #             if self.__backtrack(vertices_colors, vertice_index + 1):
    #                 return True
    #             vertices_colors[vertice_index] = '0'
                    
    # def backtrack1(self):
    #     vertices_colors = copy(self.vertices)
    #     if self.__backtrack(vertices_colors, 0):
    #         return vertices_colors
    #     else:
    #         return "Backtrack failed"
    #         # raise Exception("Backtrack failed")







    # def full_saturated(self, saturation):
    #     for element in saturation:
    #         if element != -1:
    #             return True
    #     return False
    
    # def verify_color(self, vertice_biggest_saturation, local_vertices, cor):
    #     for vertice in range(0, local_vertices.size):
    #         if self.edges[vertice_biggest_saturation][vertice] == 1 and local_vertices[vertice] == cor:
    #             return False
    #     return True
    
    # def get_bigest_saturation(self, saturation, local_vertices):
    #     count = 0
    #     temporary_count = 0
    #     after_loop = 0
    #     for i in range(0, local_vertices.size):
    #         if saturation[i] != -1 or local_vertices[i] == '0':
    #             temporary_count = 0
    #             for j in range(0, local_vertices.size):
    #                 if self.edges[i][j] == 1 and local_vertices[j] != '0':
    #                     temporary_count += 1
    #             if after_loop < temporary_count:
    #                 after = temporary_count
    #                 count = i
    #     saturation[count] = -1
    #     return count
    
    # def __dsatur_backtrack(self, local_vertices, vertice_index, saturation):
    #     print(vertice_index)
    #     if not self.full_saturated(saturation):
    #         return True
        
    #     vertice_biggest_saturation = self.get_bigest_saturation(saturation, local_vertices)
        
    #     if local_vertices[vertice_biggest_saturation]:
    #         saturation[vertice_biggest_saturation] = -1
    #         if self.__dsatur_backtrack(local_vertices, vertice_index + 1, saturation):
    #             return True
    #         else:
    #             return False
        
    #     for cor in self.acceptable_colors:
    #         if self.verify_color(vertice_biggest_saturation, local_vertices, cor):
    #             if local_vertices[vertice_biggest_saturation] == '0':
    #                 local_vertices[vertice_biggest_saturation] = cor
    #                 saturation[vertice_biggest_saturation] = -1
    #             if self.__dsatur_backtrack(local_vertices, vertice_index + 1, saturation):
    #                 return True
    #             local_vertices[vertice_biggest_saturation] = 0
        
    #     saturation[vertice_biggest_saturation] = 0
    #     return False
        
    # def dsatur_backtrack(self, queue):
    #     local_vertices = self.vertices
        
    #     # create the saturation array
    #     saturation = np.zeros((local_vertices.size,), dtype=np.int)
    #     for index in range(0, local_vertices.size):
    #         if not local_vertices[index] == '0': # has color
    #             saturation[index] = 0
    #         else:
    #             saturation[index] = -1
            
        
    #     if self.__dsatur_backtrack(local_vertices, 0, saturation):
    #         queue.append(local_vertices)
    #     else:
    #         raise Exception('The algorithm has stoped.')