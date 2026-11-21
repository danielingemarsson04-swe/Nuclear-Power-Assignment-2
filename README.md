# Nuclear-Power-Assignment-2
Simulation of a BWR reactor with scenario and reactor parameters analysis


## Contents
- - `doc/` - Documentation and dependencies
- `scr/` - Python source code
- `data/` - Generated Monte Carlo and sensitivity results

## How to Run
- Install dependencies from `doc/requirements.txt`
  
Run main file below:
```bash
python scr/main.py
```

The default run uses the simplified passing-grade model. It varies
`rho`, neutron lifetime and the fuel temperature coefficient. It prints
the Task 1 table and rankings, draws the nominal time curves and bar
charts, and prints and plots the 500-run Task 2 results.
