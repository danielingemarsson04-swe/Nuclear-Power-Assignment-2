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


def dT_dt(power):
    """Return the fuel temperature rate of change."""
    fuel_area = np.pi * fuel_rod_diameter**2 / 4
    heat_capacity_per_length = rho_UO2 * fuel_area * cp_UO2
    return power / heat_capacity_per_length


def calculate_power(rho_eff, lifetime, P_initial=P_0):
    """Return an analytical single-step power estimate."""
    rho_fraction = rho_eff * 1e-5
    return P_initial * np.exp(rho_fraction * sim_time / lifetime)


def simulate(rho=rho_0, lifetime=neutron_lifetime,
             alpha_temperature=alpha_fuel):
    """Solve the point-kinetics and fuel-temperature equations."""

    def equations(t, y):
        power_value, temperature_value = y
        rho_eff = (
            rho
            + alpha_temperature * (temperature_value - T_fuel_start)
        ) * 1e-5

        d_power_dt = rho_eff * power_value / lifetime
        d_temperature_dt = dT_dt(power_value)

        return [d_power_dt, d_temperature_dt]

    solution = solve_ivp(
        equations,
        (0, sim_time),
        (P_0, T_fuel_start),
        t_eval=np.linspace(0, sim_time, 1001),
    )

    time_values = solution.t
    power_values, temperature_values = solution.y

    k_values = 1 + (
        rho
        + alpha_temperature * (temperature_values - T_fuel_start)
    ) * 1e-5

    return time_values, power_values, temperature_values, k_values


parameters = [
    ("Reactivity", rho_0, uncertainty_rho),
    ("Neutron lifetime", neutron_lifetime, uncertainty_lifetime),
    ("Fuel temperature coefficient", alpha_fuel, uncertainty_alpha_fuel),
    ("Void coefficient", alpha_void, uncertainty_alpha_void),
    ("Heat transfer coefficient", U_w, uncertainty_U_w),
]


def print_parameter_bounds():
    """Print 90-percent parameter bounds based on 1.645 sigma."""
    print(f"{'Parameter':<32}{'Lower':>12}{'Upper':>12}")

    for name, value, uncertainty in parameters:
        sigma = abs(value) * uncertainty
        lower = value - 1.645 * sigma
        upper = value + 1.645 * sigma
        print(f"{name:<32}{lower:>12.4g}{upper:>12.4g}")


def plot_fuel_temperature(time_values, fuel_temperature):
    """Plot fuel temperature against time."""
    fig, ax = plt.subplots()
    ax.plot(time_values, fuel_temperature)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Fuel temperature (°C)")
    ax.set_title("Fuel temperature over time")
    ax.grid(True)
    return fig, ax


def plot_power(time_values, power_values):
    """Plot linear power against time."""
    fig, ax = plt.subplots()
    ax.plot(time_values, power_values)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Linear power (W/cm)")
    ax.set_title("Power over time")
    ax.grid(True)
    return fig, ax


# Keep module execution separate from library imports.
if __name__ == "__main__":
    print_parameter_bounds()

    time_values, power_values, temperature_values, k_values = simulate()

    P_max = np.max(power_values)
    delta_T_max = np.max(temperature_values) - T_fuel_start

    print("P_max =", P_max)
    print("Delta T_max =", delta_T_max)
    print("Temperature minimum:", np.min(temperature_values))
    print("Temperature maximum:", np.max(temperature_values))

    plot_power(time_values, power_values)
    plot_fuel_temperature(time_values, temperature_values)
    plt.show()
