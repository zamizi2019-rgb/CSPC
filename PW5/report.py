import pandas as pd
ev = pd.read_csv("results/events.csv")
lines = []
for _, r in ev.iterrows():
    lines.append(f"{r.file}: P at {r.tP_s:.2f} s, S at {r.tS_s:.2f} s, distance {r.R_km:.0f} km, "
                 f"origin at {r.origin_s:.1f} s, PGV {r.PGV_cm_s:.2f} cm/s, magnitude {r.M:.1f}.")
c = ev.loc[ev.R_km.idxmin(), "file"]; s = ev.loc[ev.M.idxmax(), "file"]
lines.append(f"Closer earthquake: {c}. Stronger earthquake: {s}.")
open("results/report.txt", "w").write("\n".join(lines) + "\n")
 