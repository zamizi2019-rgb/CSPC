# CSPC - Computer Science for Physics and Chemistry

My coursework repository. Each practical is under PW<n>/Lab <X>/.

## Setup

Create the environment for a given lab:

conda env create -f PW<n>/Lab\ <X>/environment.yml
conda activate cspc

## PW1 - Lab A: Reproducible Foundations

### What I built:
- A radioactive decay simulation with pure-Python and NumPy versions.
- Added tests and a speed comparison between the two.

### Speed comparison (loop vs NumPy):
- loop : `1.98184 s`
- numpy : `0.0001789 s`
- speed-up: about `11650.43` times faster

### Tests: all passing? yes

### Conclusion:
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



## PW2 - Lab A: Motion from Tracking Data

### What I built

- Read the falling-object data from freefall.csv.
- Calculated velocity and acceleration using np.gradient.
- Integrated acceleration back to velocity and position using cumulative_trapezoid.
- Created motion.png with position, velocity, and acceleration plots.

### Results

- Mean acceleration: `-8.5797 m/s²`
- Acceleration standard deviation: `28.71 m/s²`
- Largest difference between original and recovered position: `0.7846 m`

### Noise observation

The acceleration is much noisier than the position because differentiation amplifies small measurement noise, especially after applying it twice.

### Conclusion

- The measured acceleration was not very far from the expected value `-8.58`.
- Differentiation made the noise much larger in the acceleration data.
- Integrating the acceleration back recovered the original position within about 1 metre.
- The final results were plotted in motion.png.

### Bonus - 2D Tracked Trajectory

- Read trajectory.csv containing time, x, and y coordinates.
- Calculated velocity separately in the x and y directions using np.gradient.
- Calculated the speed using sqrt(vx² + vy²).
- Plotted the 2D trajectory and speed over time.
- The bonus results were saved as trajectory.png and speed.png.