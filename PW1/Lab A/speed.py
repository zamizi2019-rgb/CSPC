import time
from decay import simulate_loop,simulate

N0 = 200000
lam = 0.4
dt = 0.05
steps = 200

start = time.perf_counter()
simulate_loop(N0,lam,dt,steps)
loop_time = time.perf_counter() - start

start = time.perf_counter()
simulate(N0,lam,dt,steps)
numpy_time = time.perf_counter() - start

print("Pure Python time:",loop_time,"seconds")
print("NumPy time:",numpy_time,"seconds")
print("NumPy is",loop_time / numpy_time,"times faster")