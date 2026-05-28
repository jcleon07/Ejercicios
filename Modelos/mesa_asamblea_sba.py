import random
import numpy as np
import mesa


class Estudiante(mesa.Agent):
    
    def __init__(self, model):
        super().__init__(model)
        
        self.postura = random.uniform(0, 1)
        self.persuasion = random.uniform(0, 1)
        self.tol = np.random.weibull(a=1.5) * 15
        self.state = 0
        
    def palabra(self):
        if self.state == 0:
            self.state = 1
            print(f"El estado del agente es: {self.state}")
        else:
            self.state = 0
            print(f"El estado del agente es: {self.state}")


class Model(mesa.Model):
    
    def __init__(self, n=100, seed=None):
        super().__init__(seed=seed)
        
        self.num_agents = n 
        Estudiante.create_agents(model=self, n=n)

    def step(self):
        self.agents.shuffle_do("palabra")

model = Model(10)
for _ in range(20):
    model.step()
