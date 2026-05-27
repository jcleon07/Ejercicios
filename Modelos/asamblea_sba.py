import random
import numpy as np

class Estudiante:
    def __init__(self):
        self.postura = random.uniform(0,1)
        self.persuasion = random.uniform(0,1)
        self.tol = np.random.weibull(a=1.5) * 15


