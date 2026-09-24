# CSPC - Computer Science for Physics and Chemistry

My coursework repository. Each practical is under PW<n>/Lab <X>/.

## Setup

Create the environment for a given lab:

conda env create -f PW<n>/Lab\ <X>/environment.yml
conda activate cspc

## PW1 - Lab A: Reproducible Foundations

**What I built:**
- A radioactive decay simulation with pure-Python and NumPy versions.
- Added tests and a speed comparison between the two.

**Speed comparison (loop vs NumPy):**
- loop : 1.98184 s
- numpy : 0.0001789 s
- speed-up: about 11650.43 times faster

**Tests:** all passing? yes

**Conclusion:**
- The radioactive decay simulation worked correctly and all tests passed
- I observed that the NumPy version is much faster than pure-Python loop
- The NumPy version was about 11650 times faster in the speed test



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
