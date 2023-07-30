import numpy as np
from paramvalues import *

def AdEx(V, w, I):
    dV_dt = (g_l * (E_l - V) + g_l * delta_t * np.exp((V - V_t) / delta_t) - w + I) / C
    dw_dt = (a * (V - E_l) - w) / tau_w

    return dV_dt, dw_dt
