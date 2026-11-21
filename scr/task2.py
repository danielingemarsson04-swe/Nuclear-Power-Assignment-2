

import matplotlib.pyplot as plt
import numpy as np

from task_1 import nominal_values, uncertainty, t_fuel0, simulate

#Sample parameters from a normal distribution with the given uncertainties
def sample_parameters(rng, correlated=False):
    # rho and lifetime can also be sampled as correlated values
    z1, z2 = rng.normal(size=2)



    if correlated:
        lifetime_z = 0.8 * z1 + np.sqrt(1.0 - 0.8**2) * z2
        rho_z = z1
    else:
        rho_z = z1
        lifetime_z = z2

    parameters = nominal_values.copy()
    parameters["rho"] *= 1.0 + uncertainty["rho"] * rho_z
    parameters["lifetime"] *= (
        1.0 + uncertainty["lifetime"] * lifetime_z)
    parameters["alpha_fuel"] *= (
        1.0 + uncertainty["alpha_fuel"] * rng.normal())
    parameters["alpha_void"] = nominal_values["alpha_void"]
    parameters["u_w"] = nominal_values["u_w"]



    # Keep these values positive
    parameters["lifetime"] = max(parameters["lifetime"], 1.0e-6)
    parameters["u_w"] = max(parameters["u_w"], 1.0e-6)
    return parameters


def monte_carlo(runs=500, full_model=True, correlated=False, seed=2026):
    rng = np.random.default_rng(seed)
    times = np.linspace(0.0, 1.0, 501)
    power_runs = []
    temperature_runs = []
    k_runs = []
    void_runs = []
    p_maxes = []
    dt_maxes = []

    # Run the model once for each random parameter set
    for _ in range(runs):
        parameters = sample_parameters(rng, correlated)
        time, power, temperature, k_value, void = simulate(
            parameters, full_model, times
        )
        power_runs.append(power)
        temperature_runs.append(temperature)
        k_runs.append(k_value)
        void_runs.append(void)
        p_maxes.append(np.max(power))
        dt_maxes.append(np.max(temperature) - t_fuel0)

    return {
        "time": time, "power": np.asarray(power_runs),
        "temperature": np.asarray(temperature_runs), "k": np.asarray(k_runs),
        "void": np.asarray(void_runs), "p_max": np.asarray(p_maxes),
        "dt_max": np.asarray(dt_maxes),
    }


def interval(values, fraction):
    # Return the central percentile interval
    tail = (1.0 - fraction) * 50.0


    return np.percentile(values, [tail, 100.0 - tail], axis=0)




def plot_bands(results, quantity, title, ylabel, full_model=True):
    values = results[quantity]
    median = np.median(values, axis=0)
    # Show the 68% and 95% ranges around the median
    band68 = interval(values, 0.68)
    band95 = interval(values, 0.95)
    nominal_time, nominal_power, nominal_temperature, nominal_k, nominal_void = simulate(
        full_model=full_model
    )
    nominal = {
        "power": nominal_power, "k": nominal_k,
        "temperature": nominal_temperature, "void": nominal_void * 100.0,}[quantity]

    fig, ax = plt.subplots()
    ax.fill_between(results["time"], band95[0], band95[1], alpha=0.15, label="95%")
    ax.fill_between(results["time"], band68[0], band68[1], alpha=0.35, label="68%")
    ax.plot(results["time"], median, label="Median")
    ax.plot(nominal_time, nominal, "k--", label="Nominal")
    ax.set(title=title, xlabel="Time (s)", ylabel=ylabel)
    ax.grid(True)
    ax.legend()
    return fig

#Plot histogram of the maximum power and temperature increase
def plot_histogram(values, title, xlabel, nominal):
    fig, ax = plt.subplots()
    ax.hist(values, bins="auto", density=True, alpha=0.75)
    ax.axvline(nominal, color="k", linestyle="--", label="Nominal")
    ax.set(title=title, xlabel=xlabel, ylabel="Probability density")
    ax.grid(True, alpha=0.3)
    ax.legend()
    return fig
