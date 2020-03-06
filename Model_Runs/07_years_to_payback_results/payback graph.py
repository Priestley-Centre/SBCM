import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from variables import SPP
import formatting as form

summary = pd.read_csv("payback.csv", index_col=0)

summary.to_clipboard()

print(summary.to_string())

index = np.arange(8)
width = 0.5

# Matplotlib figure setup
form.mpl_font_setup()
mm = (120, 100)  # x value then y value
inches = (mm[0] / 25.4, mm[1] / 25.4)
fig = plt.figure(figsize=inches)
ft = 30
palette = plt.get_cmap("tab20")

chart = fig.add_subplot(1, 1, 1)


value_2 = chart.bar(
    index - width / 2,
    summary["max"] - summary["min"],
    width,
    bottom=summary["min"],
    align="edge",
    color=palette(4),
    edgecolor="k",
    linewidth=0.5,
    label="Payback period range",
    zorder=10,
    alpha=0.8,
)


# scat = chart.scatter(
#    index, summary["mean"], zorder=100, color="k", label="Mean values", marker="x", s=12
# )


scat = chart.scatter(
    index,
    summary["sterman"],
    zorder=100,
    color="k",
    label="Sterman et al. values",
    marker="x",
    s=30,
)


labs = [form.forest_labels(i, eng=True) for i in SPP]
labs.insert(0, "")
chart.set_ylabel("Time to carbon \nsequestration parity (years)", fontsize=12)
chart.tick_params(axis="both", which="major", labelsize=10)
chart.set_xticklabels((labs), rotation=45, fontsize=10, horizontalalignment="right")
for label in chart.get_yticklabels():
    label.set_fontsize(10)  # Size here overrides font_prop


chart.grid(color="k", alpha=0.5, linestyle=":", zorder=1)
chart.legend(fontsize=10)  # ), ncol=2)
plt.ylim(ymin=0, ymax=121)
plt.xlim(xmin=-0.5, xmax=7.5)

plt.subplots_adjust(
    top=0.952, bottom=0.374, left=0.211, right=0.968, hspace=0.2, wspace=0.2
)

plt.show()
plt.savefig("Fig_6_payback.png", dpi=600)
# plt.savefig("Fig_6_payback.svg")
