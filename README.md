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



## PW2 - Lab B: Optimization in Chemistry

### What I built

- Compared Gradient Descent, Newton’s method, and SLSQP on two functions.
- Fitted a first-order reaction rate constant using kinetics.csv.
- Calculated chemical equilibrium using Newton’s method and SLSQP.
- Created equilibrium.png showing H2, I2, HI, and the equilibrium point.
- Found the titration equivalence point using np.gradient and np.argmax.
- Created kinetics.png and titration.png.

### Results

- Reaction rate constant: approximately 0.25.
- Equilibrium constant: K = 15.6.
- Equilibrium extent: x ≈ 0.664.
- H2 at equilibrium: 0.336 mol.
- I2 at equilibrium: 0.336 mol.
- HI at equilibrium: 1.328 mol.
- Titration equivalence point: approximately 50 mL.

### Observations

- Different optimization methods can give different results depending on the starting point and learning rate.
- The H2 and I2 lines overlap because their initial amounts are equal.
- The equilibrium point is determined by the equilibrium constant, not by the intersection of the plotted lines.
- Differentiation helps identify the steepest part of the titration curve.

### Conclusion

- Optimization can minimize functions and fit experimental data.
- Newton’s method and SLSQP can both be used to find chemical equilibrium.
- Numerical differentiation can identify the titration equivalence point.
- The results demonstrate how numerical methods are applied to chemistry problems.

## PW3 - Part 1: Statistical Analysis of Heart Disease Data

### What I built

- Loaded the heart disease dataset using pandas.
- Printed the dataset shape and the first rows.
- Selected four continuous variables: age, chol, trestbps, and thalach.
- Created Health_graphs.png to visualise the distributions using histograms.
- Created Distribution.png to check normality using Q-Q plots.
- Compared the observed values with the theoretical quantiles of a normal distribution.

### Results

- Age: approximately normally distributed.
- Chol (cholesterol): not normally distributed, with a noticeable deviation in the upper tail.
- Trestbps (resting blood pressure): approximately normal in the central part, but with deviations at the tails.
- Thalach (maximum heart rate): approximately normally distributed, with some deviations at the tails.

### Observations

- The histograms help show the spread and shape of each variable.
- In a Q-Q plot, points close to the reference line indicate that the data are consistent with a normal distribution.
- Age and thalach follow the reference line relatively closely.
- Chol has a strong deviation at the upper end and contains an unusually high value.
- Trestbps follows the line in its central part but shows some deviations at the extremes.
- Visual inspection alone cannot conclusively determine normality; a statistical test can provide additional evidence.

### Conclusion

- Pandas was used to load and explore the dataset.
- Histograms and Q-Q plots were used to investigate the distributions of four continuous variables.
- Age and thalach appear closest to a normal distribution based on the Q-Q plots.
- Chol shows the clearest evidence of non-normality, while trestbps has some deviations.
- These findings can help guide the choice of statistical methods in Session 2.