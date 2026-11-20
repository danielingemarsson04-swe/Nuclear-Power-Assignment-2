# This python file contains useful functions and data for Task 1.

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Initial conditions
void_start = 0.25               # Start void fraction
T_fuel_start = 1000             # Start fuel temperature (Celsius)
T_cladding = T_fuel_start - 700 # Cladding surface temperature (Celsius)

# Fuel
rho_UO2 = 10.5                  # UO2 density (g/cm^3)
fuel_rod_diameter = 1.0         # Fuel rod diameter (cm)
cp_UO2 = 0.4                    # Specific heat capacity (kJ/(kg*K))

# Reactor conditions
pressure = 70                   # Reactor pressure (bar)
V_mod_V_fuel = 2.8              # Moderator-to-fuel volume ratio (-)
sim_time = 1.0                  # Sufficient simulation time: first second

# Thermal-hydraulic properties
P_0 = 150                       # Initial linear power (W/cm)
U_w = 14.3                      # Heat transfer coefficient without steam (W/(cm*K))

# Reactivity parameters
rho_0 = 2000                    # Initial excess reactivity (pcm)
k_prompt = 1.02                 # Prompt multiplication factor (-)
alpha_void = -100               # Void reactivity coefficient (pcm/% void)
alpha_fuel = -4                 # Fuel temperature coefficient (pcm/K)

# Neutron kinetics
neutron_lifetime = 1.0e-4       # Prompt neutron lifetime (s)

# Uncertainty parameters (1 sigma)
uncertainty_rho = 0.15
uncertainty_lifetime = 0.15
uncertainty_alpha_fuel = 0.15
uncertainty_alpha_void = 0.20
uncertainty_U_w = 0.25

N_samples = 500


def heat_transfer_coefficient(void_fraction):
    """Return the void-dependent heat transfer coefficient."""
    return U_w * (1 - void_fraction)

#Function that Temp change with respect to time
def dT_dt(power):
    """Return the fuel temperature rate of change."""
    fuel_area = np.pi * fuel_rod_diameter**2 / 4
    heat_capacity_per_length = rho_UO2 * fuel_area * cp_UO2
    return power / heat_capacity_per_length



#Function that calculates power
def calculate_power(rho_eff, lifetime, P_initial=P_0):
    """Return an analytical single-step power estimate."""
    rho_fraction = rho_eff * 1e-5
    return P_initial * np.exp(rho_fraction * sim_time / lifetime)




def simulate(rho=rho_0, lifetime=neutron_lifetime, alpha_temperature=alpha_fuel):
    def equations(t, y):
        power_value, temperature_value = y
        rho_eff = (rho + alpha_temperature * (temperature_value - T_fuel_start)) * 1e-5

        d_power_dt = rho_eff * power_value / lifetime
        d_temperature_dt = dT_dt(power_value)
        return [d_power_dt, d_temperature_dt]



    
    solution = solve_ivp( equations, (0, sim_time), (P_0, T_fuel_start), t_eval=np.linspace(0, sim_time, 1001),)

    time_values = solution.t
    power_values, temperature_values = solution.y

    k_values = 1 + (rho + alpha_temperature * (temperature_values - T_fuel_start)) * 1e-5

    return time_values, power_values, temperature_values, k_values


parameters = [("Reactivity", rho_0, uncertainty_rho), ("Neutron lifetime", neutron_lifetime, uncertainty_lifetime),
    ("Fuel temperature coefficient", alpha_fuel, uncertainty_alpha_fuel),
    ("Void coefficient", alpha_void, uncertainty_alpha_void),
    ("Heat transfer coefficient", U_w, uncertainty_U_w),]

#Prints upper and lower boundary values for the input parameters (Mostly to confirm values)
def print_parameter_bounds():
    print(f"{'Parameter':<32}{'Lower':>12}{'Upper':>12}")

    for name, value, uncertainty in parameters:
        sigma = abs(value) * uncertainty
        lower = value - 1.645 * sigma
        upper = value + 1.645 * sigma
        
        print(f"{name:<32}{lower:>12.4g}{upper:>12.4g}")



#Plot fueltemp to time
def plot_fuel_temperature(time_values, fuel_temperature):
    fig, ax = plt.subplots()
    ax.plot(time_values, fuel_temperature)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Fuel temperature (°C)")
    ax.set_title("Fuel temperature over time")
    ax.grid(True)
    
    return fig, ax

#Plot power to time
def plot_power(time_values, power_values):
    fig, ax = plt.subplots()
    ax.plot(time_values, power_values)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Linear power (W/cm)")
    ax.set_title("Power over time")
    ax.grid(True)
    
    return fig, ax



#Function for Pmax and Delta T max
def Pmax_DeltaTmax(rho=rho_0, lifetime=neutron_lifetime,alpha_temperature=alpha_fuel):

    _, power, temperature, _ = simulate(rho, lifetime, alpha_temperature) 
    P_max = np.max(power)
    delta_T_max = np.max(temperature) - T_fuel_start
    
    return P_max, delta_T_max




#Sensitivity part for task 1
def task1_sensitivity():
    nominal_P, nominal_T = get_output() #Base scenario for task 1 ("nominal")

    cases = [("Reactivity", "rho", rho_0, uncertainty_rho), ("Neutron lifetime", "lifetime", neutron_lifetime, uncertainty_lifetime),("Fuel temperature coefficient", "alpha_temperature", alpha_fuel,uncertainty_alpha_fuel),]

    results = [] #Making Result list

    for name, argument, value, uncertainty in cases: #for loop
        high = value * (1 + uncertainty)
        low = value * (1 - uncertainty)

        P_high, T_high = get_output(**{argument: high})
        P_low, T_low = get_output(**{argument: low})

        P_changes = [100 * (P_high - nominal_P) / nominal_P, 100 * (P_low - nominal_P) / nominal_P, ] #List of power change
        T_changes = [ 100 * (T_high - nominal_T) / nominal_T, 100 * (T_low - nominal_T) / nominal_T,] #List of temperature change

        P_effect = sum(abs(change) for change in P_changes) / 2
        T_effect = sum(abs(change) for change in T_changes) / 2

        #Appending all the results to list with changes
        results.append({ "name": name, "P changes": P_changes, "T changes": T_changes, "P effect": P_effect, "T effect": T_effect,})

    print(f"Nominal P_max:       {nominal_P})
    print(f"Nominal Delta T_max: {nominal_T})

    print(f"{'Parameter':<34}{'P_max (+/-)':<24}{'Delta T_max (+/-)':<24}")

    for result in results:
        p_up, p_down = result["P_changes"]
        t_up, t_down = result["T_changes"]

        print( f"{result['name']:<34}" f"{p_up:>8}% / {p_down:>8}% f"{t_up:>8}% / {t_down:>8}%")

    P_total = np.sqrt(sum(result["P_effect"]**2 for result in results))
    T_total = np.sqrt(sum(result["T_effect"]**2 for result in results))

    print("\nRanking by effect on P_max:")
    for rank, result in enumerate(sorted(results, key=lambda row: row["P_effect"], reverse=True), start=1,): #Sorted
        print(f"{rank}. {result['name']} ({result['P_effect']:.2f}%)")

    print("\nRanking by effect on Delta T MaX:")
    for rank, result in enumerate(sorted(results, key=lambda row: row["T_effect"], reverse=True), start=1,): #Sorted
        
        print(f"{rank}. {result['name']} ({result['T_effect']}%)")

    print(f"\nCombined uncertainty for P_max:       {P_total}%")
    print(f"Combined uncertainty for Delta T_max: {T_total}%")



# Keep module execution separate from library imports.
if __name__ == "__main__":
    print_parameter_bounds()

    time_values, power_values, temperature_values, k_values = simulate() #Gets values from simulate function

    P_max = np.max(power_values)
    delta_T_max = np.max(temperature_values) - T_fuel_start

    print("P_max =", P_max)
    print("Delta T_max =", delta_T_max)
    print("Temperature minimum:", np.min(temperature_values))
    print("Temperature maximum:", np.max(temperature_values))

    plot_power(time_values, power_values)
    plot_fuel_temperature(time_values, temperature_values)
    plt.show()
