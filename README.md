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