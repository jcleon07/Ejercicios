import matplotlib.pyplot as plt
import modelo_asamblea as model
import numpy as np
M_replicas=100

resultados=[]

tiempo_simulacion=60
cantidad_estudiantes=90
dimension_recinto=10
apertura_ideologica=0.6
umbral_tolerancia=0.5
modo="fragmentado"

for i in range(M_replicas):
    modelo_i=model.ModeloAsamblea(
                        tiempo_simulacion,
                        cantidad_estudiantes, 
                        dimension_recinto, 
                        apertura_ideologica, 
                        umbral_tolerancia,
                        modo)
    
    resultado_i=modelo_i.run(automatic=True)
    resultados.append(resultado_i)
    print(f"Replica #{i+1}")

exito_quorum=sum(1 for resultado in resultados if resultado[-1]["quorum"] == True)
print(f"quorums exitosos: {exito_quorum}")



promedios_por_paso = [np.mean([r[t]["promedio_posturas"] for r in resultados]) for t in range(tiempo_simulacion)]
varianzas_por_paso = [np.mean([r[t]["varianza_posturas"] for r in resultados]) for t in range(tiempo_simulacion)]
activos_por_paso   = [np.mean([r[t]["n_activos"] for r in resultados]) for t in range(tiempo_simulacion)]
quorum_por_paso    = [np.mean([1 if r[t]["quorum"] else 0 for r in resultados]) for t in range(tiempo_simulacion)]


time=list(range(tiempo_simulacion))

fig, axs = plt.subplots(2, 2, figsize=(14, 8))
fig.suptitle(f"Escenario: {modo} | P(éxito) = {exito_quorum/M_replicas:.2f}")

axs[0,0].set_title("Postura colectiva promedio")
axs[0,0].plot(time, promedios_por_paso, color="green")
axs[0,0].set_ylim(0, 1)
axs[0,0].set_xlabel("Paso")

axs[0,1].set_title("Varianza de postura colectiva")
axs[0,1].plot(time, varianzas_por_paso, color="orange")
axs[0,1].set_xlabel("Paso")

axs[1,0].set_title("Agentes activos promedio")
axs[1,0].plot(time, activos_por_paso, color="blue")
axs[1,0].set_xlabel("Paso")

axs[1,1].set_title("Proporción de réplicas con quórum")
axs[1,1].plot(time, quorum_por_paso, color="red")
axs[1,1].set_ylim(0, 1)
axs[1,1].set_xlabel("Paso")

plt.tight_layout()
plt.show()
