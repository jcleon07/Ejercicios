import random
import numpy as np

class Estudiante:
    def __init__(self, postura, persusasion, tol):
        self.postura = postura
        self.persuasion = self.persuasion
        self.tol = tol
        self.state = None

    def tomar_palabra(self):
        if self.state == None:
            self.state = 1 
        else:
            self.state = None

class Modelo:
    def __init__(self, n):
        self.num_agents = n


