import mesa
import numpy as np
import time
import random


class CleanAgent(mesa.Agent):
    # An agent with fixed initial wealth.

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.count = 1
        
    def step(self):
        self.move()
        self.clean()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.count = self.count + 1
        print("Porcentaje de limpieza " + str(self.model.porcentaje_celdas_limpias()) + "% ----" + str(self.count))

    def clean(self):
        if self.model.isDirty(self.pos):
            self.model.setDirty(self.pos)
        pass
    

class CleanModel(mesa.Model):
    """A model with some number of agents."""

    

    def __init__(self, N, width, height, percent):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.celdas_suc = int(round((width * height) * percent))
        self.celdas_lim = (width * height) - self.celdas_suc
        self.dirty_matrix = np.zeros([width,height])
        
        countw = 0
        counth = 0
        var = 1
        countcs = self.celdas_suc
        for x in self.dirty_matrix:
            if width < countcs:
                while counth < height and var == 1:
                    countw = 0
                    while countw < width and var == 1:
                        if countcs > 0:
                            self.dirty_matrix[countw][counth] = 1
                            countw = countw + 1
                            countcs = countcs - 1
                        else:
                            var = 0  
                    counth = counth + 1            
            else:
                while countw < width and var == 1:
                    
                    if countcs > 0:
                        self.dirty_matrix[countw][counth] = 1
                        countw = countw + 1
                        countcs = countcs - 1
                        if countcs <= 0:
                            var = 0
                            pass
                    else:
                        var = 0 
        counth = 0
        countw = 0
        if width < height:
            while countw < width:
                np.random.shuffle(self.dirty_matrix[countw])
                countw = countw + 1
            self.printarray()
        else:
            while counth < height:
                np.random.shuffle(self.dirty_matrix[counth])
                counth = counth + 1
            self.printarray()

        self.width = width
        self.height = height
        
        for i in range(self.num_agents):
            a = CleanAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))

        
    
    def step(self):
        self.schedule.step()


    def isDirty(self, new_position):
        x, y = new_position
        if self.dirty_matrix[x][y] == 1:
            return True
        else:
            return False

    def setDirty(self, new_position):
        x, y = new_position
        self.celdas_suc = self.celdas_suc - 1
        self.celdas_lim = self.celdas_lim + 1
        self.dirty_matrix[x][y] = 0

    def printarray(self):
        print(self.dirty_matrix)

    def porcentaje_celdas_limpias(self):
        return (self.celdas_lim / (self.width*self.height))*100
        pass

    

    