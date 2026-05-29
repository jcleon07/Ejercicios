import random
import numpy as np

class Estudiante:
    def __init__(self, row, col):
        self.postura = random.uniform(0,1)
        self.persuasion = random.uniform(0,1)
        self.tol = np.random.weibull(a=1.5) * 15
        self.activo = True
        self.row = row
        self.col = col

    def tomar_palabra(self, vecinos, sigma, umb):
        for i in vecinos:
            i.ajustar_postura(self, sigma, umb)

    def ajustar_postura(self, agente_hablante, sigma, umb=0.5):
        diff = agente_hablante.postura - self.postura
        pow = -abs(diff)/sigma

        if abs(diff) > umb:
            self.postura -= agente_hablante.persuasion * (diff) * np.exp(pow)
        else:
            self.postura += agente_hablante.persuasion * (diff) * np.exp(pow)                                                                             
        self.postura = np.clip(self.postura, 0, 1)

