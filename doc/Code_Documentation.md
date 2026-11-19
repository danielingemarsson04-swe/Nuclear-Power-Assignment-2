## Problem description
During a rare event a reactor controlrod can mechanically fail and fall out. The potential reactor implications are lost possibility of controling neutron economy through absorption of promt neutrons, resulting in a promt critical reactor.


**Goal:**

Numerically calculate the reactor behaviour during the event and determine the uncertainty of the results based on uncertainties in the input data.

### Task 1

**Two cases:**
- Nominal case using the original values of all parameters.
- Sensitivity cases where one parameter at a time is changed while all other parameters remain constant.

**Calculation parameters:**
- P<sub>max</sub>
- ΔT<sub>max</sub>

**Results are presented as follows:**

- A table showing the percentage changes in P<sub>max</sub> and ΔT<sub>max</sub> for each parameter, ranked from largest to smallest impact.

- The total uncertainty is calculated by combining the contributions from all five parameters using the root sum of squares:

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

  
## Equations
Given that `k = k(α, T)`, the chain rule gives:

Given that \(k = k(\alpha, T_f)\), the chain rule gives:


## Input Data and Assumptions

| Parameter | Value | Unit |
|-----------|-------|------|
| Initial void fraction, α₀ | 25 | % |
| Initial fuel temperature, T_f,0 | 1000 | °C |
| Cladding surface temperature, T_c | T_f − 700 | °C |
| Pressure | 70 | bar |
| Moderator-to-fuel volume ratio, V_mod/V_fuel | 2.8 | – |
| UO₂ density | 10.5 | g/cm³ |
| Fuel rod diameter | 1 | cm |
| Linear power, P₀ | 150 | W/cm |
| UO₂ specific heat capacity, c_p | 0.4 | kJ/(kg·K) |
| Heat transfer coefficient (without steam), U_w | 14.3 (4.55 W/(cm²·K)) | W/(cm·K) |
| Heat transfer coefficient with void, U(α) | U_w · (1 − α) | W/(cm·K) |
| Void coefficient, ∂k/∂α | −100 | pcm/% void |
| Fuel temperature coefficient, ∂k/∂T_f | −4 | pcm/K |
| Prompt neutron lifetime, ℓ | 1.0 × 10⁻⁴ | s |
| Excess reactivity, ρ = k_prompt − 1 | 2000 | pcm |
| k_prompt | 1.02 | – |
| Moderator cooling | Constant (equilibrium conditions before the event) | – |
| Simulation time | 1 | s |
| Minimum number of randomized parameter sets | 500 | – |

### Uncertainty Parameters

| Parameter | Nominal value | Uncertainty (1σ) |
|-----------|---------------|------------------|
| Excess reactivity, ρ = k_prompt − 1 | 2000 pcm | 15% |
| Prompt neutron lifetime, ℓ | 1.0 × 10⁻⁴ s | 15% |
| Fuel temperature coefficient, ∂k/∂T_f | −4 pcm/K | 15% |
| Void coefficient, ∂k/∂α | −100 pcm/% void | 20% |
| Heat transfer coefficient, U_w | 14.3 W/(cm·K) | 25% |

