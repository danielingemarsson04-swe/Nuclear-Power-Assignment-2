# Main entry point for the BWR reactor simulation.

import numpy as np

from task_1 import (
    P_max,
    alpha_fuel,
    alpha_void,
    k_prompt,
    neutron_lifetime,
    plot_fuel_temperature,
    plot_power,
    rho_0,
    simulate,
    temperature,
    time,
    power,
)


def print_nominal_results():
    """Print the nominal simulation results."""
    nominal_time, nominal_power, nominal_temperature, nominal_k = simulate()

    p_max = np.max(nominal_power)
    delta_t_max = np.max(nominal_temperature) - nominal_temperature[0]

    print("Nominal P_max =", p_max)
    print("Nominal Delta T_max =", delta_t_max)

    plot_power(nominal_time, nominal_power)
    plot_fuel_temperature(nominal_time, nominal_temperature)


if __name__ == "__main__":
    print_nominal_results()
