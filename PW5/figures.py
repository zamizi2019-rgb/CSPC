import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scipy.signal as ss
from scipy.signal import find_peaks
from analyse import bandpass, envelope, analyse, VP, VS

os.makedirs("figures", exist_ok=True)
d = pd.read_csv("data/seismogram_A.csv")
t = d["time_s"].to_numpy(); fs = 1 / (t[1] - t[0])
Z, N, E = d["Z"].to_numpy(), d["N"].to_numpy(), d["E"].to_numpy()
r = analyse("data/seismogram_A.csv")
tP, tS = r["tP_s"], r["tS_s"]
print("fs =", fs, "Hz, duration =", t[-1], "s")

#1)

fig, ax = plt.subplots(3, 1, sharex=True, figsize=(10, 6))

for a, x, n in zip(ax, (Z, N, E), "ZNE"):
    a.plot(t, x * 1e3, lw=0.5); a.set_ylabel(f"{n} (mm/s)")
    print(f"max |{n}| = {np.abs(x).max()*1e3:.2f} mm/s")

ax[-1].set_xlabel("time (s)"); fig.tight_layout()
fig.savefig("figures/1_Channels.png", dpi=110)
ax[0].set_xlim(0, 60)

for a, x in zip(ax, (Z, N, E)):
    s = x[t < 60] * 1e3; a.set_ylim(s.min() * 1.3, s.max() * 1.3)

fig.savefig("figures/1b_ZoomFirst.png", dpi=110)
print("quiet part rms (um/s): Z %.2f N %.2f E %.2f" % tuple(x[t < 60].std() * 1e6 for x in (Z, N, E)))

#2a)

X = np.fft.fft(Z); f = np.fft.fftfreq(len(Z), 1 / fs); amp = np.abs(X) / len(Z) * 2
fig, ax = plt.subplots(1, 2, figsize=(10, 3.5))
ax[0].plot(amp * 1e3, lw=0.6); ax[0].set_xlabel("array index"); ax[0].set_ylabel("amplitude (mm/s)")
ax[1].plot(f, amp * 1e3, lw=0.6); ax[1].set_xlabel("frequency (Hz)")
fig.tight_layout(); fig.savefig("figures/2a_Spectrum.png", dpi=110)

#2b)

q = Z[t < 60]; fq = np.fft.fftfreq(len(q), 1 / fs); ampq = np.abs(np.fft.fft(q)) / len(q) * 2
plt.figure(figsize=(8, 5))
plt.loglog(f[f > 0], amp[f > 0], lw=0.6, label="whole record")
plt.loglog(fq[fq > 0], ampq[fq > 0], lw=0.6, label="quiet part (0-60 s)")
plt.xlabel("frequency (Hz)"); plt.ylabel("amplitude (m/s)"); plt.legend(); plt.tight_layout()
plt.savefig("figures/2b_Spectra.png", dpi=110)
print("quiet spectrum peak: %.3f Hz" % fq[fq > 0][np.argmax(ampq[fq > 0])])

for lo, hi in [(0.05, 0.5), (0.5, 2), (2, 10), (10, 50)]:
    mq = (fq > lo) & (fq <= hi); mw = (f > lo) & (f <= hi)
    print(f"band {lo}-{hi} Hz: quiet mean {ampq[mq].mean():.2e}  whole mean {amp[mw].mean():.2e}  ratio {amp[mw].mean()/ampq[mq].mean():.1f}")

#3)

print("ifft(fft(Z)) == Z:", np.allclose(np.fft.ifft(np.fft.fft(Z)).real, Z))
Zf, Nf, Ef = (bandpass(x, fs, 0.5, 10) for x in (Z, N, E))
plt.figure(figsize=(10, 3.2)); plt.plot(t, (Z - Zf) * 1e3, lw=0.5)
plt.xlabel("time (s)"); plt.ylabel("Z - clean (mm/s)"); plt.tight_layout()
plt.savefig("figures/3c_Removed.png", dpi=110)
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(10, 5))
ax[0].plot(t, Z * 1e3, lw=0.5); ax[0].set_ylabel("raw Z (mm/s)")
ax[1].plot(t, Zf * 1e3, lw=0.5); ax[1].set_ylabel("filtered Z (mm/s)"); ax[1].set_xlabel("time (s)")
fig.tight_layout(); fig.savefig("figures/3b_RawVsFiltered.png", dpi=110)
print("removed part: rms before 60 s %.2e, rms around quake %.2e" % ((Z-Zf)[t<60].std(), (Z-Zf)[(t>tS)&(t<tS+60)].std()))

#4)

H = np.sqrt(Nf**2 + Ef**2)
envZ, envH = envelope(Zf, fs, 0.5), envelope(H, fs, 0.5)
plt.figure(figsize=(10, 4))

for w in (0.05, 0.5, 5):
    plt.plot(t, envelope(Zf, fs, w) * 1e3, lw=0.8, label=f"Z, window {w} s")

plt.xlabel("time (s)"); plt.ylabel("envelope (mm/s)"); plt.legend(); plt.xlim(90, 220); plt.tight_layout()
plt.savefig("figures/4a_Envelopes.png", dpi=110)
plt.figure(figsize=(10, 4))
plt.plot(t, envZ * 1e3, label="Z envelope (0.5 s)"); plt.plot(t, envH * 1e3, label="horizontal envelope (0.5 s)")
plt.xlabel("time (s)"); plt.ylabel("mm/s"); plt.legend(); plt.tight_layout()
plt.savefig("figures/4b_Envelopes.png", dpi=110)

#5)

pk, _ = find_peaks(envH, height=0.5 * envH.max()); t_max = t[pk[np.argmax(envH[pk])]]
print(f"tP={tP:.2f} tS={tS:.2f} t(max horizontal envelope)={t_max:.2f}")
fig, ax = plt.subplots(3, 1, sharex=True, figsize=(10, 6))

for a, x, n in zip(ax, (Z, N, E), "ZNE"):
    a.plot(t, x * 1e3, lw=0.5); a.set_ylabel(f"{n} (mm/s)")
    a.axvline(tP, c="g", label="tP"); a.axvline(tS, c="r", label="tS"); a.axvline(t_max, c="k", ls="--", label="max H envelope")

ax[0].legend(loc="upper left"); ax[-1].set_xlabel("time (s)"); fig.tight_layout()
fig.savefig("figures/5_Picks.png", dpi=110)

#6)

k = 1 / VS - 1 / VP; R = (tS - tP) / k
print(f"k={k:.5f} s/km  R={R:.1f} km  R(tS-1)={(tS-1-tP)/k:.1f}  R(tS+1)={(tS+1-tP)/k:.1f}  dR/dtS={1/k:.2f} km/s")
print(f"origin={tP - R/VP:.2f} s;  R if t_max used: {(t_max-tP)/k:.1f} km")

#7)

ff, ts_, S = ss.spectrogram(Z, fs=fs, nperseg=256); m = ff <= 10
plt.figure(figsize=(10, 4)); plt.pcolormesh(ts_, ff[m], 10 * np.log10(S[m]), shading="auto")
plt.colorbar(label="dB"); plt.xlabel("time (s)"); plt.ylabel("frequency (Hz)"); plt.tight_layout()
plt.savefig("figures/7_Spectrogram.png", dpi=110)

for name, (a, b) in {"before P": (0, tP - 3), "P window": (tP, tP + 10), "S window": (tS, tS + 10), "late 200-250s": (200, 250)}.items():
    sel = (ts_ >= a) & (ts_ < b); mm = (ff > 0.2) & (ff <= 10)
    p = S[:, sel].mean(axis=1)[mm]; print(f"{name:14s} dominant {ff[mm][np.argmax(p)]:.2f} Hz, power-weighted centroid {np.sum(ff[mm]*p)/p.sum():.2f} Hz")

#8)

pgv = np.sqrt(N**2 + E**2).max() * 100
M = (np.log10(pgv) + np.log10(R) + 1.0) / 0.55
print(f"PGV={pgv:.3f} cm/s  M={M:.2f}  M ignoring R: {(np.log10(pgv)+1)/0.55:.2f}")
print(f"2x farther, R-term effect on M: {np.log10(2)/0.55:.2f}; PGV factor per +1 M: {10**0.55:.2f}")