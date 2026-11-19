# Main entry point for the BWR reactor simulation.

import matplotlib.pyplot as plt

from task_1 import (
    T_fuel_start,
    plot_fuel_temperature,
    plot_power,
    simulate,
)


def print_nominal_results():
    """Print the nominal simulation results and show the plots."""
    nominal_time, nominal_power, nominal_temperature, nominal_k = simulate()

    p_max = nominal_power.max()
    delta_t_max = nominal_temperature.max() - T_fuel_start

    print("Nominal P_max =", p_max)
    print("Nominal Delta T_max =", delta_t_max)

    plot_power(nominal_time, nominal_power)
    plot_fuel_temperature(nominal_time, nominal_temperature)
    plt.show()


if __name__ == "__main__":
    print_nominal_results()
