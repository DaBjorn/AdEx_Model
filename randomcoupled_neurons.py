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

Number_of_Neurons = 100
neuron = NeuronGroup(Number_of_Neurons, eqn, reset = reset_condition, threshold = 'V > V_t', method = 'rk4', refractory = 0 * ms)

# Initial Conditions
neuron.V = full(Number_of_Neurons, -70.0) * mV
neuron.I = full(Number_of_Neurons, 509.7) * pA
neuron.g_l = '12 * rand() * nS'

# Establishing synapses
synapse = Synapses(neuron, neuron, on_pre = 'V_post += 15 * mV')
synapse.connect(condition = 'i != j', p = 0.2)

# State and spike recording
M = StateMonitor(neuron, 'V', record = True)
spikemon = SpikeMonitor(neuron)

run(1000 * ms)

# Plotting the function
figure(figsize = (12, 4))
      
subplot(121)
plot(spikemon.t/ms, spikemon.i, '.k')
ylabel("Neuronal Index")
xlabel("Time (ms)")
title("Raster Plot for spiking behaviour of 100 randomly coupled neurons")

subplot(122)
plot(synapse.i, synapse.j, '.k')
ylabel("Target Neuron")
xlabel("Source Neuron")
title("How the Neurons are connected")

savefig("/Users/Parasite/Documents/D/Codes/py codes/Plots/random_neurons.png", dpi = 1200)
show()