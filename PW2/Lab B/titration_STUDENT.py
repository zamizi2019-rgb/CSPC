"""
PW2 Lab B Part 5 (bonus) -- find a titration's equivalence point.

titration.csv holds a titration curve: pH versus the volume of base added.
The equivalence point is the volume where the pH changes fastest (the steep
jump). Numerically, that is where the SLOPE of the pH curve is largest.
Run:  python titration.py
"""
import numpy as np
import matplotlib.pyplot as plt

data=np.loadtxt("titration.csv",delimiter=",",skiprows=1)

V=data[:,0]
pH=data[:,1]

slope=np.gradient(pH,V)

index=np.argmax(slope)
equivalence_volume=V[index]

print("Equivalence point: ",equivalence_volume,"ml")

fig,axes=plt.subplots(1,2,figsize=(12,5))

axes[0].plot(V, pH, marker="o")
axes[0].set_xlabel("Volume of base (mL)")
axes[0].set_ylabel("pH")
axes[0].set_title("Titration Curve")

axes[1].plot(V, slope, marker="o")
axes[1].axvline(
    equivalence_volume,
    linestyle="--",
    label="Equivalence point"
)
axes[1].set_xlabel("Volume of base (mL)")
axes[1].set_ylabel("Slope (dpH/dV)")
axes[1].set_title("Slope of Titration Curve")
axes[1].legend()

plt.tight_layout()
plt.savefig("titration.png")
plt.show()

# TODO 1: read titration.csv (columns volume_base, pH) into arrays V, pH.

# TODO 2: compute the slope of the pH curve with np.gradient(pH, V), and find
#         the volume where that slope is largest (np.argmax). That is the
#         equivalence point. Print it.

# TODO 3: make two plots side by side: (left) pH vs volume with a line at the
#         equivalence point; (right) the slope vs volume, showing it peaks
#         at the equivalence point. Save as titration.png.
