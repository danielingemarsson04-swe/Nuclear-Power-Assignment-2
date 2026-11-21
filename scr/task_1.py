

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

nominal_values = {
    "rho": 2000.0, "lifetime": 1.0e-4, "alpha_fuel": -4.0,
    "alpha_void": -100.0, "u_w": 14.3,}


uncertainty = {
    "rho": 0.15, "lifetime": 0.15, "alpha_fuel": 0.15,
    "alpha_void": 0.20, "u_w": 0.25,}



#Default values for the initial conditions
p0 = 150.0
t_fuel0 = 1000.0
void0 = 0.25

t_cladding = 300.0
t_saturation = 285.0

v_mod_v_fuel = 2.8
rho_steam = 36.0
h_fg = 1500.0e3
duration = 1.0




# Calculates the heat capacity for one cm of fuel rod
def heat_capacity():
    area = np.pi * 1.0**2 / 4.0
    kg_per_cm = 10.5 * area / 1000.0
    return kg_per_cm * 0.4 * 1000.0


def simulate(parameters=None, full_model=True, times=None):
    # Use the nominal values unless other values are given
    if parameters is None:
        parameters = nominal_values
    if times is None:
        times = np.linspace(0.0, duration, 501)

    capacity = heat_capacity()
    p_cooling = p0

    def equations(_time, state):
        power = state[0]
        fuel_temperature = state[1]

        # The basic model assumes void is constant
        if full_model:
            void = float(np.clip(state[2], 0.0, 1.0))
            rho_void = parameters["alpha_void"] * (
                void * 100.0 - void0 * 100.0
            )
        else:
            void = void0
            rho_void = 0.0

        rho_total = (
            parameters["rho"]
            + rho_void
            + parameters["alpha_fuel"] * (fuel_temperature - t_fuel0)
        )
        # Convert reactivity from pcm to a fraction type
        k_value = 1.0 + rho_total * 1.0e-5
        dpdt = (k_value - 1.0) * power / parameters["lifetime"]

        if not full_model:
            dtdt = power / capacity
            return [dpdt, dtdt]

        u_void = parameters["u_w"] * (1.0 - void)
        p_heat = u_void * (t_cladding - t_saturation)
        dtdt = (power - p_heat) / capacity
        vapor_mass_cm3 = rho_steam * v_mod_v_fuel
        dh_dt = (p_heat - p_cooling) / (vapor_mass_cm3 * h_fg)
        d_void_dt = dh_dt / 1.0
        d_void_dt = float(np.clip(d_void_dt, -1.0, 1.0))
        return [dpdt, dtdt, d_void_dt]

    initial = [p0, t_fuel0, void0] if full_model else [p0, t_fuel0]
    solution = solve_ivp(
        equations,
        (0.0, duration),
        initial,
        t_eval=times,
        rtol=1.0e-7,
        atol=1.0e-9,
        max_step=0.002,
    )
    if not solution.success:
        raise RuntimeError(solution.message)

    # Calculate k for every time step
    power = solution.y[0]
    fuel_temperature = solution.y[1]
    void = solution.y[2] if full_model else np.full_like(power, void0)

    rho_void = np.zeros_like(power)
    if full_model:
        rho_void = parameters["alpha_void"] * (
            void * 100.0 - void0 * 100.0
        )
    rho_total = (
        parameters["rho"] + rho_void + parameters["alpha_fuel"] * (fuel_temperature - t_fuel0))

    
    k_value = 1.0 + rho_total * 1.0e-5
    return solution.t, power, fuel_temperature, k_value, void


def peak_values(parameters=None, full_model=True):
    _time, power, temperature, _k, _void = simulate(parameters, full_model)
    return float(np.max(power)), float(np.max(temperature) - t_fuel0)


def task1(full_model=True):
    # Change one parameter at a time
    nominal_p, nominal_dt = peak_values(full_model=full_model)
    names = [   ("rho", "Excess reactivity"), ("lifetime", "Prompt neutron lifetime"), ("alpha_fuel", "Fuel temperature coefficient"),
        ("alpha_void", "Void coefficient"),
        ("u_w", "Heat transfer coefficient"),]



    
    if not full_model:
        names = names[:3]

    rows = []
    for key, name in names:
        low_value = nominal_values[key] * (1.0 - uncertainty[key])
        high_value = nominal_values[key] * (1.0 + uncertainty[key])

        low = nominal_values.copy()
        high = nominal_values.copy()
        low[key] = low_value
        high[key] = high_value

        p_low, dt_low = peak_values(low, full_model)
        p_high, dt_high = peak_values(high, full_model)
        p_low_change = 100.0 * (p_low - nominal_p) / nominal_p
        p_high_change = 100.0 * (p_high - nominal_p) / nominal_p
        dt_low_change = 100.0 * (dt_low - nominal_dt) / nominal_dt
        dt_high_change = 100.0 * (dt_high - nominal_dt) / nominal_dt




        rows.append({


            "name": name, "p_low": p_low_change, "p_high": p_high_change,
            "dt_low": dt_low_change, "dt_high": dt_high_change,
            "p_effect": np.mean([abs(p_low_change), abs(p_high_change)]),
            "dt_effect": np.mean([abs(dt_low_change), abs(dt_high_change)]),})

    p_total = np.sqrt(sum(row["p_effect"] ** 2 for row in rows))
    dt_total = np.sqrt(sum(row["dt_effect"] ** 2 for row in rows))
    # Combine the parameter effects using root sum of squares
    return nominal_p, nominal_dt, rows, float(p_total), float(dt_total)


def plot_nominal(full_model=True):
    time, power, temperature, k_value, void = simulate(full_model=full_model)
    plots = [
        ("Power", power, "Linear power (W/cm)"), ("Multiplication factor", k_value, "k"),
        ("Fuel temperature", temperature, "Temperature (C)")
    ]
    if full_model:
        plots.insert(2, ("Void", void * 100.0, "Void (%)"))

    figures = []
    for title, values, ylabel in plots:
        fig, ax = plt.subplots()
        ax.plot(time, values)
        ax.set(title=f"{title} vs time", xlabel="Time (s)", ylabel=ylabel)
        ax.grid(True)
        figures.append(fig)
    return figures
