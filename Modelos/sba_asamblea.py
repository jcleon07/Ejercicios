import random
import numpy as np

class Estudiante:
    def __init__(self, postura, persuasion, tol):
        self.postura = postura
        self.persuasion = persuasion
        self.tol = tol
        self.state = None

    def tomar_palabra(self):
        if self.state == None:
            self.state = 1 
        else:
            self.state = None

    def ajustar_postura(self, otro_agente):
            post = otro_agente.postura
            if post < 0.5:
                self.persuasion = random.uniform(0,0.5)
            else:
                self.persuasion = random.uniform(0.51, 1)

    def cambiar_postura(self):
        per = self.persuasion
         

class Modelo:
    def __init__(self, n, espacio):

        if espacio % 2 != 0:
            print("El tamano del espacio debe ser par") 
            exit()

        self.num_agents = n
        self.espacio = [[None for _ in range(espacio//2) ] for _ in range(espacio//2)]
        self.quorum = None

        count = 0

        for i in range(espacio//2):
            for j in range(espacio//2):

                if count >= n:
                    break

                self.espacio[i][j] = Estudiante(0.5, 0.76, 30)
                count += 1


    def is_quorum(self):
        if self.num_agents < (0.5 * self.espacio) + 1:
            quorum = False
        else:
            quorum = True

