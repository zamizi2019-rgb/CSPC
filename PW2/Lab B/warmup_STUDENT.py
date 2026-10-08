"""
PW2 Lab B Part 2 -- three routes to a minimum.

Compare gradient descent, Newton, and SLSQP on two functions:
  2A: f(x) = (x-3)**2 + 1          (easy, one minimum at x=3)
  2B: g(x) = x**4 - 3*x**2 + x + 5 (harder, several stationary points)
Run:  python warmup.py
"""
import numpy as np
from scipy.optimize import newton, minimize

# ---------- 2A: easy convex function ----------
def f(x):   return (x-3)**2 + 1
def df(x):  return 2*(x-3)
def d2f(x): return 2.0

# ---------- 2B: harder landscape ----------
def g(x):   return x**4 - 3*x**2 + x + 5
def dg(x):  return 4*x**3 - 6*x + 1
def d2g(x): return 12*x**2 - 6

#TODO 2A (1)

x0 = 0
x = x0
lr = 0.1

def gradient_desc(x,lr):
  while True:
      old_x=x
      x = x - lr * df(x)
      if abs(old_x-x) < 0.00000001:
          return x 

print("2A Gradient Descent:",gradient_desc(x,lr))

#TODO 2A (2)

x_newton = newton(df,x0,fprime=d2f)
print("2A Newton:",x_newton)

#TODO 2A (3)

result = minimize(f,x0,method="SLSQP")
print("2A SLSQP:",result.x[0])

#TODO 2B (1)
def gradient_desc_B(x,lr):
  while True:
      old_x=x
      x = x - lr * dg(x)
      if abs(old_x-x) < 0.00000001:
          return x 

print("2B Gradient Descent(x0=0):",gradient_desc_B(0,lr),)
print("2B Gradient Descent(x0=2):",gradient_desc_B(2,lr),)
#TODO 2B (2)

x_newton = newton(dg,x0,fprime=d2g)
x_newton_2 = newton(dg,2,fprime=d2g)
print("2B Newton(x0=0):",x_newton,"minimum" if d2g(x_newton)>0 else "maximum")
print("2B Newton(x0=2):",x_newton_2,"minimum" if d2g(x_newton_2)>0 else "maximum")
#TODO 2B (3)

result = minimize(g,0,method="SLSQP")
result_2 = minimize(g,2,method="SLSQP")
print("2B SLSQP(x0=0):",result.x[0])
print("2B SLSQP(x0=2):",result_2.x[0])