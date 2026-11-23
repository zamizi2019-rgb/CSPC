import numpy as np, pandas as pd
VP, VS = 6.2, 3.6

def bandpass(x, fs, a, b):
    X = np.fft.fft(x)
    f = np.fft.fftfreq(len(x), 1/fs)
    X[(np.abs(f) < a) | (np.abs(f) > b)] = 0
    return np.fft.ifft(X).real

def envelope(x, fs, win_s):
    w = max(1, int(round(win_s*fs)))
    return np.convolve(np.abs(x), np.ones(w)/w, mode="same")

def analyse(csv_file):
    d = pd.read_csv(csv_file)
    t = d["time_s"].to_numpy(); fs = 1/(t[1]-t[0])
    Z, N, E = (d[c].to_numpy() for c in "ZNE")
    A, B = 0.5, 10.0
    Zf, Nf, Ef = (bandpass(x, fs, A, B) for x in (Z, N, E))
    envZ = envelope(Zf, fs, 0.5)
    envH = envelope(np.sqrt(Nf**2 + Ef**2), fs, 0.5)
    tP = t[np.argmax(envZ > 0.05*envZ.max())]
    after = t > tP + 2
    tS = t[after][np.argmax(envH[after] > 0.10*envH.max())]
    R = (tS - tP) / (1/VS - 1/VP)
    t0 = tP - R/VP
    pgv = np.sqrt(N**2 + E**2).max() * 100          # cm/s
    M = (np.log10(pgv) + np.log10(R) + 1.0) / 0.55
    return dict(file=csv_file.split("/")[-1], tP_s=tP, tS_s=tS, R_km=R,
                origin_s=t0, PGV_cm_s=pgv, M=M)

if __name__ == "__main__":
    import os
    os.makedirs("results", exist_ok=True)
    rows = [analyse(f"data/seismogram_{k}.csv") for k in "AB"]
    pd.DataFrame(rows).to_csv("results/events.csv", index=False)