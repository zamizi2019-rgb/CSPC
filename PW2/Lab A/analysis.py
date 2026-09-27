"""
PW2 Lab A -- Motion from tracking data.

Read noisy free-fall position measurements, then:
  - differentiate once  -> velocity
  - differentiate twice -> acceleration (should be ~ constant -g, but noisy!)
  - integrate the acceleration back up -> recover velocity and position

Complete the TODOs. Run:  python analysis.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

data = np.loadtxt("freefall.csv",delimiter=",",skiprows=1)
t = data[:,0]
y = data[:,1]

v = np.gradient(y,t)
a = np.gradient(v,t)
print("Mean acceleration:",np.mean(a))
print("Standard deviation:",a.std())

v_recovered = cumulative_trapezoid(a,t,initial=0) + v[0]
y_recovered = cumulative_trapezoid(v_recovered,t,initial=0) + y[0]
difference = np.abs(y_recovered-y)
print("Largest difference:",np.max(difference))

#Graph part
fig,axs = plt.subplots(3,1,sharex=True)

axs[0].plot(t,y)
axs[0].set_ylabel("Position")
axs[0].grid()

axs[1].plot(t,v)
axs[1].set_ylabel("Velocity")
axs[1].grid()

axs[2].plot(t,a)
axs[2].axhline(-9.81,linestyle="--")
axs[2].set_ylabel("Acceleration")
axs[2].set_xlabel("Time")
axs[2].grid()
plt.tight_layout()
plt.savefig("motion.png")
#add ex

data2 = np.loadtxt("trajectory.csv",delimiter=",",skiprows=1)

time = data2[:,0]
x2 = data2[:,1]
y2 = data2[:,2]

vx = np.gradient(x2,time)
vy = np.gradient(y2,time)

speed = np.sqrt(vx**2 + vy**2)

plt.figure()
plt.plot(x2,y2)
plt.xlabel("x")
plt.ylabel("y")
plt.title("2D Trajectory")
plt.savefig("trajectory.png")

plt.figure()
plt.plot(time,speed)
plt.xlabel("Time (s)")
plt.ylabel("Speed (m/s)")
plt.title("Speed vs Time")
plt.savefig("speed.png")