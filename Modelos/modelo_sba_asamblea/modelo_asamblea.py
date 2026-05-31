import math 
import random
import numpy as np
import estudiante_asamblea as es

class ModeloAsamblea:
    def __init__(self, simulation_time, num_agents, dimension, sigma, umbral, mode="fragmentado"):
        self.dimension=dimension
        if dimension % 2 != 0:
            raise ValueError("El tamaño del espacio debe ser par") 
        
        if num_agents>dimension**2:
            num_agents=dimension**2
    
        self.espacio = [[None for _ in range(dimension) ] for _ in range(dimension)]

        self.simulation_time=simulation_time
        self.num_agents = num_agents
        self.sigma = sigma
        self.umbral = umbral
        self.mode=mode
        self.quorum = None
        self.time = 0

        self.interventor_coord = None
        self.coords_vecinos = set()

        self._init_students(self.mode)



    def _init_students(self, mode="fragmentado"):
        celdas_disponibles = [(i, j) for i in range(self.dimension) for j in range(self.dimension)]
        random.shuffle(celdas_disponibles)
        
        for k in range(self.num_agents):
            i, j = celdas_disponibles[k]
            estudiante = es.Estudiante(i, j)
            estudiante.factor_tolerancia(int(self.simulation_time*1.25))
            
            if mode == "homogeneo":
                estudiante.postura = np.clip(np.random.normal(0.5, 0.1), 0, 1)
            elif mode == "polarizado":
                estudiante.postura = np.clip(np.random.choice([np.random.normal(0.2, 0.1), np.random.normal(0.8, 0.1)]), 0, 1)
            
            self.espacio[i][j] = estudiante
        


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
    


    def imprimir_estado(self):
        RESET = "\033[0m"
        INACTIVO = "\033[90m"

        def postura_a_color(p):
            if p < 0.5:
                t = p * 2                          # 0→1
                r = 220
                g = int(220 * t)
                b = int(220 * t)
            else:
                t = (p - 0.5) * 2                  # 0→1
                r = int(220 * (1 - t))
                g = int(220 * (1 - t))
                b = 220
            return f"\033[38;2;{r};{g};{b}m"

        print(f"\n── t={self.time} | quórum={'SI' if self.quorum else 'NO'} ──")
        for i, fila in enumerate(self.espacio):
            linea = ""
            for j, agente in enumerate(fila):
                if agente is not None:
                    if self.interventor_coord == (i, j):
                        linea += postura_a_color(agente.postura) + "??" + RESET
                    elif (i,j) in self.coords_vecinos:
                        linea += postura_a_color(agente.postura) + "░░" + RESET

                    else:
                        linea += postura_a_color(agente.postura) + "██" + RESET
                else:
                    linea += INACTIVO + "░░" + RESET
            print(linea)

        activos = [agente for f in self.espacio for agente in f if agente is not None]
        if activos:
            prom = np.mean([agente.postura for agente in activos])
            var  = np.var ([agente.postura for agente in activos])
            print(f"activos={len(activos)}/{self.num_agents} | prom={prom:.3f} | var={var:.3f}")



    def step(self, automatic=True):
        clear="\033[H\033[J"
        estudiantes_activos = []
        for i in range(len(self.espacio)):
            for j in range(len(self.espacio[0])):

                if self.espacio[i][j] != None and self.espacio[i][j].tol > 0:
                    self.espacio[i][j].tol -= 1
                    estudiantes_activos.append([i,j])
                elif self.espacio[i][j] != None and self.espacio[i][j].tol <= 0:
                    self.espacio[i][j].activo = False
                    self.espacio[i][j] = None

        if not estudiantes_activos:
            return 
        self.is_quorum()

        interventor_agent = random.choice(estudiantes_activos)
        i, j = interventor_agent
        vec=self.encontrar_vecinos(self.espacio[i][j])

        self.interventor_coord = (i, j)
        self.coords_vecinos = {(v.row, v.col) for v in vec}
        print(clear)
        self.imprimir_estado()
        
        if not automatic:
            # self.interventor_coord = (i, j)
            # self.coords_vecinos = {(v.row, v.col) for v in vec}
            # print(clear)
            # self.imprimir_estado()        
            pause = input()

        self.espacio[i][j].tomar_palabra(vec, self.sigma, self.umbral)
        self.time += 1



    def metricas(self):
        n_activos = 0
        posturas = []

        for i in range(len(self.espacio)):
            for j in range(len(self.espacio[0])):
                if self.espacio[i][j] != None and self.espacio[i][j].activo == True:
                    n_activos += 1
                    posturas.append(self.espacio[i][j].postura)
        
        prom_posturas = np.average(posturas)
        var_posturas = np.var(posturas)
        met = {
            "tiempo": self.time,
            "n_activos": n_activos,
            # "posturas": posturas,
            "promedio_posturas": prom_posturas,
            "varianza_posturas": var_posturas,
            "quorum": self.quorum
        }
        return met



    def run(self,automatic=True):
        historial = []
        for i in range(self.simulation_time):
            self.step(automatic)
            historial.append(self.metricas())
            # if self.quorum == False:
            #     break
        return historial



if __name__=="__main__":
    tiempo_simulacion=60
    cantidad_estudiantes=90
    dimension_recinto=10
    apertura_ideologica=0.6
    umbral_tolerancia=0.5
    modo="fragmentado"


    model1 = ModeloAsamblea(
                            tiempo_simulacion,
                            cantidad_estudiantes, 
                            dimension_recinto, 
                            apertura_ideologica, 
                            umbral_tolerancia,
                            modo)

    hist = model1.run(automatic=False)
