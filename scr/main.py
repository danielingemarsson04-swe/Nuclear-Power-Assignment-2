

import matplotlib.pyplot as plt
import numpy as np

from task_1 import peak_values, plot_nominal, task1
from task2 import monte_carlo, plot_histogram






def print_summary(label, values, nominal):
    # Print the main statistics for the Monte Carlo results
    mean = np.mean(values)
    median = np.median(values)
    sigma = np.std(values, ddof=1)
    interval68 = np.percentile(values, [16.0, 84.0])
    interval95 = np.percentile(values, [2.5, 97.5])
    print(f"\n{label}")
    print(f"Nominal: {nominal:.6g}")
    print(f"Mean: {mean:.6g}")
    print(f"Median: {median:.6g}")
    print(f"Standard deviation: {sigma:.6g}")
    print(f"68% interval: [{interval68[0]:.6g}, {interval68[1]:.6g}]")
    print(f"95% interval: [{interval95[0]:.6g}, {interval95[1]:.6g}]")






def print_sensitivity(full_model=True):
    # Print the one-parameter-at-a-time sensitivity results
    nominal_p, nominal_dt, rows, p_total, dt_total = task1(full_model)
    print("\nTASK 1")
    print(f"Nominal P_max: {nominal_p:.6g} W/cm")
    print(f"Nominal Delta T_max: {nominal_dt:.6g} K")
    print(f"{'Parameter':<34}{'P low':>10}{'P high':>10}{'DT low':>10}{'DT high':>10}")
    for row in rows:
        print(f"{row['name']:<34}"
              f"{row['p_low']:>9.2f}%"
              f"{row['p_high']:>9.2f}%"
              f"{row['dt_low']:>9.2f}%"
              f"{row['dt_high']:>9.2f}%")
    print(f"\nCombined P_max uncertainty: {p_total:.2f}%")
    print(f"Combined Delta T_max uncertainty: {dt_total:.2f}%")




    print("\nRanking by effect on P_max:")
    p_ranking = sorted(rows, key=lambda row: row["p_effect"], reverse=True)
    for rank, row in enumerate(p_ranking, start=1):
        print(f"{rank}. {row['name']}: {row['p_effect']:.2f}%")



    print("\nRanking by effect on Delta T_max:")
    dt_ranking = sorted(rows, key=lambda row: row["dt_effect"], reverse=True)
    for rank, row in enumerate(dt_ranking, start=1):
        print(f"{rank}. {row['name']}: {row['dt_effect']:.2f}%")





    # Compare which parameters have the largest effect
    fig, axes = plt.subplots(1, 2)
    axes[0].barh(
        [row["name"] for row in p_ranking],
        [row["p_effect"] for row in p_ranking],
    )
    axes[0].set_title("Effect on P_max")
    axes[0].set_xlabel("Average change (%)")
    axes[0].invert_yaxis()

    axes[1].barh(
        [row["name"] for row in dt_ranking],
        [row["dt_effect"] for row in dt_ranking],
    )
    axes[1].set_title("Effect on Delta T_max")
    axes[1].set_xlabel("Average change (%)")
    axes[1].invert_yaxis()
    fig.tight_layout()


def main(full_model=False):
    print_sensitivity(full_model)
    plot_nominal(full_model)

    # Use independent samples for the passing-grade analysis
    independent = monte_carlo(500, full_model, correlated=False)
    nominal_p, nominal_dt = peak_values(full_model=full_model)
    print("\nTASK 2")
    print_summary("P_max", independent["p_max"], nominal_p)
    print_summary("Delta T_max", independent["dt_max"], nominal_dt)

    plot_histogram(independent["p_max"], "P_max distribution",
                   "P_max (W/cm)", nominal_p)
    plot_histogram(independent["dt_max"], "Delta T_max distribution",
                   "Delta T_max (K)", nominal_dt)

    # Check how the mean and standard deviation change as runs are added
    counts = np.arange(10, len(independent["p_max"]) + 1)
    p_means = [np.mean(independent["p_max"][:count]) for count in counts]
    p_sigmas = [
        np.std(independent["p_max"][:count], ddof=1) for count in counts
    ]
    fig, axes = plt.subplots(1, 2)
    axes[0].plot(counts, p_means)
    axes[0].set(title="P_max mean vs number of runs",
                xlabel="Number of runs", ylabel="Mean P_max (W/cm)")
    axes[1].plot(counts, p_sigmas)
    axes[1].set(title="P_max standard deviation vs number of runs",
                xlabel="Number of runs",
                ylabel="Standard deviation (W/cm)")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main(full_model=False)
