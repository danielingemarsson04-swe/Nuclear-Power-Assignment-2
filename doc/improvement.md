## Repository overview

- **Repository:** [danielingemarsson04-swe/Nuclear-Power-Assignment-2](https://github.com/danielingemarsson04-swe/Nuclear-Power-Assignment-2)
- **Description:** Simulation of a BWR reactor with scenario and reactor parameters analysis
- **Primary language:** Python (100%)

## Improvements

The following improvements are proposed for the BWR reactor simulation repository.

- Improve the structure of the Python source code and documentation.
- Make it easier to reproduce sensitivity and uncertainty analyses.
- Add clearer input validation and handling for reactor parameters.
- Present simulation results consistently, for example through time curves and ranked impact tables.
- Improve the setup instructions and dependency management.
- Separate nominal, sensitivity, and Monte Carlo calculations where appropriate.
- Expand automated checks for reactor parameter ranges and generated output files.
- Improve naming and consistency in source files and documentation.

## Analysis goals

The repository can be extended to better support:

- Nominal BWR reactor simulations.
- Sensitivity analyses for one parameter at a time.
- Quantitative ranking of parameter impacts.
- Monte Carlo analyses based on parameter uncertainties.
- Clear reporting of power, multiplication factor, void fraction, and fuel temperature.

## Recommended repository structure

- `doc/` – Documentation and dependencies.
- `scr/` – Python source code.
- `data/` – Generated Monte Carlo and sensitivity results.
- `figures/` – Time curves, histograms, and bar charts.
- `report/` – Report with source code in the appendix.

## Input quality improvements

- Validate that reactor parameters are within physically reasonable ranges.
- Document units for every input and output parameter.
- Check dependencies before starting a simulation.
- Provide clear warnings for invalid or inconsistent parameters.
- Include a configuration file for nominal values and uncertainty distributions.

## Result quality improvements

- Compare nominal and sensitivity results in one table.
- Rank percentage changes in maximum power and maximum fuel temperature from largest to smallest impact.
- Include uncertainty ranges for the maximum power and maximum fuel temperature.
- Export numerical results in a consistent format, such as CSV.
- Save figures with descriptive filenames and documented units.

## Suggested future tasks

- Add automated unit tests for core reactor calculations.
- Add a command-line interface with configurable input data.
- Add a complete Monte Carlo workflow with a reproducible random seed.
- Add more detailed assumptions and model limitations.
- Include example runs and expected output in the documentation.

## Total uncertainty

The total uncertainty can be calculated by combining parameter contributions using the root sum of squares:

$$
\delta_{\text{total}} =
\sqrt{
\delta_1^2 +
\delta_2^2 +
\delta_3^2 +
\delta_4^2 +
\delta_5^2
}
$$
