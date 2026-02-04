import matplotlib.pyplot as plt
import numpy as np

a = 1000000000
b = 10000000

def pc_a (n) :
    return (2*(n**2))/a

def pc_b (n) :
    return 50*n*np.log2(n)/b

#Arrays con los resultados para cada potencia de 10 hasta 1.000.000
time_a = [pc_a(10), pc_a(100), pc_a(1000), pc_a(10000), pc_a(100000), pc_a(1000000)]
time_b = [pc_b(10), pc_b(100), pc_b(1000), pc_b(10000), pc_b(100000), pc_b(1000000)]

print("TIEMPO COMPUTADOR A: \n",[format(t, ".10f") for t in time_a])
print("\nTIEMPO COMPUTADOR B: \n",[format(t, ".10f") for t in time_b])

n_values = np.array([10, 100, 1000, 10000, 100000, 1000000])

#Grafica
plt.figure(figsize=(6, 4), layout='constrained')
plt.plot(n_values, time_a, marker='o', label='PC_A')  
plt.plot(n_values, time_b, marker='o', label='PC_B')  
plt.ylabel('tiempo (s)')
plt.xlabel('n')
plt.xscale('log')
plt.yscale('log')
plt.title("PC_A vs PC_B")
plt.legend()
plt.grid(True)
plt.show()