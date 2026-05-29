import math 
import random
import numpy as np
import estudiante_asamblea as es

class Modelo:
    def __init__(self, n, espacio, sigma, umb):

        if espacio % 2 != 0:
            print("El tamano del espacio debe ser par") 
            exit()

        self.num_agents = n
        self.espacio = [[None for _ in range(espacio//2) ] for _ in range(espacio//2)]
        self.quorum = None
        self.sigma = sigma
        self.umb = umb
        self.time = 0

        count = 0
        for i in range(espacio//2):
            for j in range(espacio//2):

                if count >= n:
                    break

                self.espacio[i][j] = es.Estudiante(i,j)
                count += 1


    def is_quorum(self):
        n_activos = 0
        for i in range(len(self.espacio)):
            for j in range(len(self.espacio[0])):
                if self.espacio[i][j] != None and self.espacio[i][j].activo == True:
                    n_activos += 1
        
        if n_activos >= math.floor(0.5 * self.num_agents) + 1:
            self.quorum = True
        else:
            self.quorum = False

    def encontrar_vecinos(self, hablante):
        vecinos = []   
        for i in range(len(self.espacio)):
            for j in range(len(self.espacio[0])):
                dist = math.sqrt((hablante.row - i)**2 + (hablante.col - j)**2)
                if self.espacio[i][j] != None and dist <= 5 and self.espacio[i][j] != self.espacio[hablante.row][hablante.col]:
                    vecinos.append(self.espacio[i][j])
        return vecinos
    
    def step(self):
        activos = []
        for i in range(len(self.espacio)):
            for j in range(len(self.espacio[0])):

                if self.espacio[i][j] != None and self.espacio[i][j].tol > 0:
                    self.espacio[i][j].tol -= 1
                    activos.append([i,j])
                elif self.espacio[i][j] != None and self.espacio[i][j].tol <= 0:
                    self.espacio[i][j].activo = False
                    self.espacio[i][j] = None

        self.is_quorum()

        if self.quorum == True:
            ran_agent = random.choice(activos)
            a = ran_agent[0]
            b = ran_agent[1]

            vec = self.encontrar_vecinos(self.espacio[a][b])
            self.espacio[a][b].tomar_palabra(vec ,self.sigma,self.umb)

        self.time += 1

        def run():
            