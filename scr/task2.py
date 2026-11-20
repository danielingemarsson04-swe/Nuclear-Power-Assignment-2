
#This is the code for task 2 with the Monte Carlo simulation.

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from task_1 import ( P_0, T_fuel_start, rho_UO2, fuel_rod_diameter, cp_UO2, sim_time, rho_0, neutron_lifetime, alpha_fuel, alpha_void, U_w, N_samples)

N_runs = N_Samples #Amount of monte carlo simulations

#Function that returns nominal parameters
def nominal_parameters():
  return { "rho": rho_0, "lifetim": neutron_lifetime, "alpha_fuel": alpha_fuel, "void": alpha_void, "U_w": U_w,}


def samplefunction(rng): #Randomizes parameters (normaldsitribution)
    rho = rng.normal(rho_0, 0.15 * rho_0)
  
    lifetime = rng.normal(neutron_lifetime, 0.15 * neutron_lifetime)
    alpha = rng.normal(alpha_fuel, 0.15 * abs(alpha_fuel))
    lifetime = max(lifetime)
  
    return rho, lifetime, alpha

#Basic structure for percentile band (more added soon)
def percentile_band(values, central_fraction): 
    tail = (1 - central_fraction) * 50
    low, high = np.percentile(values, [tail, 100 - tail], axis=0)
    return low, high
