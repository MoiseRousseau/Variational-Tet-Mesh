import matplotlib.pyplot as plt
import numpy as np

netgen = [596.4] #1 CPU
mesher_total = [1009.4, 545.8, 326.4, 273.4, 249.2, 210.0] #1, 2, 4, 6, 8, 12 CPU
mesher = [982.33, 518.53, 299.27, 246.29, 222.17, 181.2] #1, 2, 4, 6, 8, 12 CPU
label = ["Netgen", "Var. mesher,\n1 thread", "2 threads", "4 threads", "6 threads", "8 threads", "12 threads"]
col = ['r'] + ['b']*len(mesher)

fig,ax = plt.subplots(figsize=(8,5))
ax.minorticks_on()
ax.yaxis.grid(True, which="major",linestyle="-")
ax.yaxis.grid(True, which="minor",linestyle="--", alpha=0.5)
ax.bar(np.arange(len(label)), netgen + mesher_total, align="center", tick_label=label, color = col)
ax.set_ylabel("Running time (s)")

plt.tight_layout()
plt.show()
