# This python file will contain useful functions and data for task 1.

import numpy as np
import matplotlib.pyplot as plt

# Input parameters, assumptions

# Initial conditions
void_start = 0.25               # Start void fraction 
T_fuel_start = 1000             # Start fuel temperature (celisus)
T_cladding = T_fuel_start - 700 # Cladding surface temperature (celisus)


# Fuel
rho_UO2 = 10.5                  # UO2 density (g/cm^3)
fuel_rod_diameter = 1.0         # Fuel rod diameter (cm)
cp_UO2 = 0.4                    # Specific heat capacity

# Reactor conditions
pressure = 70                   # Reactor pressure (bar)
V_mod_V_fuel = 2.8              # Moderator-to-fuel volume ratio (-)
sim_time = 1.0           



# Thermal-hydraulic properties
P_0 = 150                       # Initial linear power (W/cm)
U_w = 14.3                      # Heat transfer coefficient without steam (W/(cm*K))

# Reactivity parameters
rho_0 = 2000                    # Initial excess reactivity (pcm)
k_prompt = 1.02                 # Prompt multiplication factor (-)
alpha_void = -100               # Void reactivity coefficient (pcm/% void)
alpha_fuel = -4                 # Fuel temperature coefficient (pcm/K)

# Neutron kinetics
neutron_lifetime = 1.0e-4       # Neutron lifetime (promt, s)

# Uncertainty parameters (1 sigma)
uncertainty_rho = 0.15          # Excess reactivity uncertainty (15%)
uncertainty_lifetime = 0.15     # Prompt neutron lifetime uncertainty (15%)
uncertainty_alpha_fuel = 0.15   # Fuel temperature coefficient uncertainty (15%)
uncertainty_alpha_void = 0.20   # Void coefficient uncertainty (20%)
uncertainty_U_w = 0.25          # Heat transfer coefficient uncertainty (25%)

# N sample count
N_samples = 500

# Heat transfer coefficient as a function of void fraction
def heat_transfer_coefficient(void):
    return U_w * (1 - void)




#Temperature dependence over time
def dT_dt(power):
    fuel_area = np.pi * fuel_rod_diameter**2 / 4
    heat_capacity_per_length = rho_UO2 * fuel_area * cp_UO2
    return power / heat_capacity_per_length


U_initial = U_w * (1 - void_start)


#Caluclates Power
def calculate_power(rho_eff, neutron_lifetime, P_initial=P_0):
    rho_fraction = rho_eff * 1e-5  # Konvertera pcm till absolut reaktivitet
    return P_initial * np.exp(rho_fraction * sim_time / neutron_lifetime)


parameters = [ ("Reactivity", rho_0, uncertainty_rho),
    ("Neutron lifetime", neutron_lifetime, uncertainty_lifetime),
    ("Fuel temperature coefficient", alpha_fuel, uncertainty_alpha_fuel),
    ("Void coefficient", alpha_void, uncertainty_alpha_void),
    ("Heat transfer coefficient", U_w, uncertainty_U_w)]

print(f"{'Parameter':<32}{'Lower':>12}{'Upper':>12}")

for name, value, uncertainty in parameters:
    sigma = abs(value) * uncertainty
    print(f"{name:<32}{value - 1.645*sigma:>12.4g}{value + 1.645*sigma:>12.4g}")

#Plot of Fuel Temperature with respect to time
def plot_fuel_temperature(time, fuel_temperature):
    fig, ax = plt.subplots()
    ax.plot(time, fuel_temperature)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Fuel temperature (°C)")
    ax.set_title("Fuel temperature over time")
    ax.grid(True)
    plt.show()
    return fig, ax

#Plot of Power with respect to time
def plot_power(time, power):
    fig, ax = plt.subplots()
    ax.plot(time, power)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Linear power (W/cm)")
    ax.set_title("Power over time")
    ax.grid(True)
    plt.show()
    return fig, ax
