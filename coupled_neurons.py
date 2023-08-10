from brian2 import *

start_scope()

# Parameters

C = 200.0 * pF  # Membrane capacitance (pF)
# g_l = 12.0 * nS  # Leak conductance (nS)
E_l = -70.0 * mV # Leak reversal potential (mV)
V_t = -50.0 * mV # Threshold potential (mV)
V_peak = 20.0 * mV # Peak potential (mV)
delta_t = 2 * mV # slope factor (mV)
tau_w = 300.0 * ms # Adaptation time constant (ms)
a = 2.0 * nS # Subthreshold adaptation coupling (nS)
b = 80.5 * pA # Spike-triggered adaptation increment (pA)
I_input = 509.7 * pA # Input current (pA)

# Equation for AdEx

eqn = """
    dV/dt = (g_l * (E_l - V) + g_l * delta_t * exp((V - V_t) / delta_t) - w + I) / C : volt (unless refractory)
    dw/dt = (a * (V - E_l) - w) / tau_w : amp
    I : amp
    g_l : siemens
"""

# Reset condition for firing
reset_condition = """
V = E_l
w += b
"""

# Creating Neuron group
Number_of_Neurons = 2

neuron = NeuronGroup(Number_of_Neurons, eqn, reset = reset_condition, threshold = 'V > V_t', method = 'rk4', refractory = 0 * ms)

# Initial Conditions
neuron.V = full(Number_of_Neurons, -70.0) * mV
neuron.I = [509.7, 0] * pA
neuron.g_l = [12.0, 6.0] * nS

# Establishing synapses
synapse = Synapses(neuron, neuron, on_pre = 'V_post += 20 * mV')
synapse.connect(i = 0, j = 1)

# State and spike monitoring
M = StateMonitor(neuron, 'V', record = True)
spikemon = SpikeMonitor(neuron)

run(1000 * ms)

# Plotting results
figure(figsize = (12, 4))

subplot(121)
plot(M.t/ms, M.V[0], label = "Neuron 1")
plot(M.t/ms, M.V[1], label = "Neuron 2", linestyle = "--")
title("Time series of two coupled neurons")
xlabel("Time (ms)")
ylabel("Membrane Potential")
legend()

subplot(122)
plot(spikemon.t/ms, spikemon.i, '.k')
ylabel("Neuronal Index")
xlabel("Time (ms)")
title("Raster Plot for spiking behaviour of two neurons")

savefig("/Users/Parasite/Documents/D/Codes/py codes/Plots/coupled_neurons.png", dpi = 1200)
show()