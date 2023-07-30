import numpy as np
import matplotlib.pyplot as plt
from paramvalues import *
from adex_fns import AdEx

# Integration algorithm - Runge Kutta 4th order

t_sim = 1000.0
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

# Input current

I = np.zeros(Iterations)
t = np.arange(0, t_sim, del_t)

########### Spiking current ################

I_freq = 10 # ms
I_duration = 20 # ms
I_amplitude = 509.7 # pA

for i in range(Iterations):
    if (t[i] % (1000/I_freq) < I_duration):
        I[i] = I_amplitude
    else:
        I[i] = 0

###########################################

########### Constant Current ##############

# for i in range(Iterations):
#     I[i] = 509.7

##########################################

# print(I)

V, w = rk4(AdEx, E_l, 0, I, Iterations, del_t)
spike_time = [i[0] for i in spike]
spike_potential = [i[1] for i in spike]

# Plotting the values

figure1 = plt.figure(1)
plt.plot(t, I)
plt.xlabel("Time (ms)")
plt.ylabel("Input Current (pA)")
plt.title("Input current vs time")
# plt.savefig("/Users/Parasite/Documents/D/Codes/py codes/Plots/Inputcurrent_2.png", dpi = 1200)

figure2 = plt.figure(2)
plt.plot(t, V)
plt.xlabel("Time (ms)")
plt.ylabel("Membrane potential (mV)")
# plt.plot(t, w, color = 'r')
plt.title("Membrane potential vs time from the AdEx equation")
# plt.savefig("/Users/Parasite/Documents/D/Codes/py codes/Plots/Spikepattern_withoutspikes_2.png", dpi = 1200)

figure3 = plt.figure(3)
plt.plot(t, w)
plt.xlabel("Time (ms)")
plt.ylabel("Adaptation constant, w (pA)")
plt.title("Adaptation constant vs time")
# plt.savefig("/Users/Parasite/Documents/D/Codes/py codes/Plots/Adaptationconstant_2.png", dpi = 1200)

index = []
for i in range(Iterations):
    for j in range(len(spike_time)):
        if t[i] == spike_time[j]:
            index.append(i)

# print(index)

V_values = V
t_values = t

for i in index:
    V_values = np.insert(V_values, i, V_peak)
    t_values = np.insert(t_values, i, t[i + 1])


figure4 = plt.figure(4)
plt.plot(t_values, V_values)
plt.axhline(y = -50, color = 'r', linestyle = "--", label = "Threshold Voltage (-50 mV)")
plt.axhline(y = 20, color = 'orange', linestyle = "--", label = "Peak Voltage (20 mV)")
plt.title("Membrane potential vs time including the spikes")
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Potential (mV)")
plt.legend()
# plt.savefig("/Users/Parasite/Documents/D/Codes/py codes/Plots/Spikepattern_withspikes_2.png", dpi = 1200)

plt.show()
