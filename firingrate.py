import numpy as np
import matplotlib.pyplot as plt
from paramvalues import *
from adex_fns import AdEx

# Integration algorithm - Runge Kutta 4th order

t_sim = 100.0
del_t = 0.01
Iterations = int(t_sim/del_t)

spike = [] # Empty list to record spike timings and peak voltage

def rk4(f, V, w, I, N, h):
    V = np.zeros(N)
    w = np.zeros(N)
    t = np.arange(0.0, t_sim, del_t)

    V[0] = E_l
    w[0] = 0.0
    
    for i in range(1, N):
        k1, l1 = f(V[i - 1], 
                   w[i - 1],
                   I[i - 1])
        k2, l2 = f(V[i - 1] + 0.5 * h * k1, 
                   w[i - 1] + 0.5 * h * l1,
                   I[i - 1])
        k3, l3 = f(V[i - 1] + 0.5 * h * k2, 
                   w[i - 1] + 0.5 * h * l2,
                   I[i - 1])
        k4, l4 = f(V[i - 1] + h * k3, 
                   w[i - 1] + h * l3,
                   I[i - 1])

        V[i] = V[i-1] + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        w[i] = w[i-1] + (h / 6.0) * (l1 + 2 * l2 + 2 * l3 + l4)

        if V[i] >= V_t:
            V[i] = V_reset
            w[i] += b
            spike.append((t[i], V_peak))

    return V, w

# Input Current - constant current input

firingrate = []
current = np.arange(500, 520, 0.1)
for j in current:
    I = np.zeros(Iterations)
    t = np.arange(0, t_sim, del_t)

    for i in range(Iterations):
        I[i] = j

    V, w = rk4(AdEx, E_l, 0, I, Iterations, del_t) 

    # Spike timings

    spike_time = [i[0] for i in spike]
    spike_potential = [i[1] for i in spike]

    # Index of spike timings

    index = []
    for i in range(Iterations):
        for j in range(len(spike_time)):
            if t[i] == spike_time[j]:
                index.append(i)

    print(index)

    print(len(index)/t_sim)

    firingrate.append(len(index)/t_sim)

plt.scatter(current, firingrate, s = 0.2)
plt.xlabel("Current (pA)")
plt.ylabel("Firing rate (No. of spikes/ total time of simulation)")
plt.title("Firing rate of AdEx Neurons vs Input current")
# plt.savefig("/Users/Parasite/Documents/D/Codes/py codes/Plots/Firingrate.png", dpi = 1200)

plt.show()