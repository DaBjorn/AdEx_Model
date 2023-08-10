from brian2 import *

start_scope() # Just like implicit none

# Parameters

C = 200.0 * pF  # Membrane capacitance (pF)
g_l = 12.0 * nS  # Leak conductance (nS)
E_l = -70.0 * mV # Leak reversal potential (mV)
V_t = -50.0 * mV # Threshold potential (mV)
V_peak = 20.0 * mV # Peak potential (mV)
delta_t = 2 * mV # slope factor (mV)
tau_w = 300.0 * ms # Adaptation time constant (ms)
a = 2.0 * nS # Subthreshold adaptation coupling (nS)
b = 80.5 * pA # Spike-triggered adaptation increment (pA)
I = 509.7 * pA# Input current (pA)

# Equation for AdEx

eqn = """
    dV/dt = (g_l * (E_l - V) + g_l * delta_t * exp((V - V_t) / delta_t) - w + I) / C : volt (unless refractory)
    dw/dt = (a * (V - E_l) - w) / tau_w : amp
"""

# Reset condition for firing
reset_condition = """
V = E_l
w += b
"""

# Creating Neuron group
neuron = NeuronGroup(1, eqn, reset = reset_condition, threshold = 'V > V_t', method = 'rk4', refractory = 0 * ms)

# Monitoring and recording neuron state values
neuron_state = StateMonitor(neuron, 'V', record = 0)

# Monitoring neurons spikes
neuron_spike = SpikeMonitor(neuron)

# Initial conditions
neuron.V = 'E_l'

# Running simulations
run(1 * second)

# Creating a new array to store potential values with spike values
V_values = neuron_state[0].V[:]
for t in neuron_spike.t:
    i = int(t/defaultclock.dt)
    V_values[i] = V_peak

# Plotting the figures
figure(figsize = (12, 4))

subplot(121)
plot(neuron_state.t/ms, neuron_state.V[0])
xlabel("Time (ms)")
ylabel("Membrane Potential")
title("AdEx graph")

subplot(122)
plot(neuron_state.t/ms, V_values)
xlabel("Time")
ylabel("Membrane Potential")
title("With spikes")

show()