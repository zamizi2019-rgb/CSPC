"""
PW2 Lab B Part 4 -- chemical equilibrium via the equilibrium constant K.

Reaction  H2 + I2 <=> 2 HI, starting from 1 mol H2 and 1 mol I2.
As the reaction proceeds by an extent x:  H2 = 1-x,  I2 = 1-x,  HI = 2x.
At equilibrium the composition satisfies the equilibrium constant
        K = [HI]^2 / ([H2][I2]) = (2x)^2 / ((1-x)(1-x)).
Given K, find the extent x. Solve it TWO ways and compare.
Run:  python equilibrium.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton, minimize

K = 15.6
a = b = 1.0
def k_imbalance(x):
    return (2*x)**2/((a-x)*(b-x)) - K

x_newton=newton(k_imbalance,0.5)

def error_sq(x):
    return k_imbalance(x[0])**2

result=minimize(error_sq,[0.5],method="SLSQP",bounds=[(0, 0.999)])

x_slsqp=result.x[0]
print("Newton: ", x_newton)
print("SLSQP: ", x_slsqp)



H2_eq=a-x_newton
I2_eq=b-x_newton
HI_eq=2*x_newton

print("H2 at equilibrium:",H2_eq,"moles")
print("I2 at equilibrium:",I2_eq,"moles")
print("HI at equilibrium:",HI_eq,"moles")



x_value=np.linspace(0,0.999,200)

plt.plot(x_value,a-x_value,label="H2")
plt.plot(x_value,b-x_value,label="I2",linestyle="--")
plt.plot(x_value,2*x_value,label="HI")
plt.axvline(x_newton,color="black",linestyle="--",label="Equilibrium")

plt.xlabel("Reaction extent x (mol)")
plt.ylabel("Amount in moles")
plt.legend()
plt.tight_layout()
plt.savefig("equilibrium.png")


# TODO 1: write k_imbalance(x) = (2x)^2/((a-x)(b-x)) - K.
#         It equals zero exactly at equilibrium.

# TODO 2 (method 1): use scipy.optimize.newton to find the root of k_imbalance
#         (start x0=0.5). This is root-finding.

# TODO 3 (method 2): use scipy.optimize.minimize to minimise k_imbalance(x)**2
#         (method "SLSQP", bounds [(0, 0.999)], x0=[0.5]). Print both answers
#         and confirm they agree.

# TODO 4: report the equilibrium amounts (H2, I2, HI), and plot how the three
#         amounts change with the extent x, marking the equilibrium. Save
#         equilibrium.png.
