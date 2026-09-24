## PW1 - Lab B: Data, Plotting, and Automation

### What I built

- Read the observed radioactive decay data from `decay_observed.csv`.
- Plotted the observed data and the analytical decay law.
- Used the analytical law `N(t) = N0 * exp(-lambda * t)` with `lambda = 0.3`.
- Created a Snakemake pipeline to automatically generate `figure.png`.

### Result

The observed data showed a decreasing radioactive decay pattern. The observed data matched the analytical decay law reasonably well, as the two plots had similar shapes.

### Snakemake

The Snakemake pipeline takes `decay_observed.csv` as input and runs `plot_STUDENT.py` to produce `figure.png`. It only reruns the script when the input or script has changed.