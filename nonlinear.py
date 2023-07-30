import numpy as np
import matplotlib.pyplot as plt
from paramvalues import *

V = np.arange(-75, -40)

f_V = g_l * (E_l - V) + g_l * delta_t * np.exp((V - V_t) / delta_t)

plt.plot(V, f_V)
plt.xlabel("Membrane Potential")
plt.ylabel("f(V)")
plt.title("Nonlinear function vs membrane potential")
plt.axhline(y = 0, color = 'r', linestyle = '--')
plt.show()