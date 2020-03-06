import pandas as pd
import matplotlib.pyplot as plt
from variables import SPP
import formatting as form

summary = pd.read_csv("summary.csv", index_col=0)
cols = list(summary.columns.values)

form.mpl_font_setup()
mm = (120, 100)  # x value then y value
inches = (mm[0] / 25.4, mm[1] / 25.4)
fig = plt.figure(figsize=inches)

palette = plt.get_cmap("tab20")
chart = fig.add_subplot(1, 1, 1)


for col in cols[:1]:
    i = cols.index(col)
    x = [i] * len(summary[col])
    scat = chart.scatter(
        x[0],
        summary[col][0],
        color=palette(0),
        label="Sterman Model RMSE values",
        marker="o",
        zorder=100,
        alpha=1,
    )
    scat = chart.scatter(
        x[1:],
        summary[col][1:],
        color=palette(2),
        label="SBCM RSME values",
        marker="o",
        zorder=99,
        alpha=0.5,
    )

for col in cols[1:]:
    i = cols.index(col)
    x = [i] * len(summary[col])
    scat = chart.scatter(
        x[0], summary[col][0], color=palette(0), marker="o", zorder=100, alpha=1
    )
    scat = chart.scatter(
        x[1:], summary[col][1:], color=palette(2), marker="o", zorder=99, alpha=0.5
    )


labs = [form.forest_labels(i, short="star", eng=True) for i in SPP]
labs.insert(0, " ")
chart.set_ylabel("RSME (tC.ha$^{-1}$)", fontsize=12)
chart.tick_params(axis="both", which="major", labelsize=10)
chart.set_xticklabels((labs), rotation=45, fontsize=10, horizontalalignment="right")

chart.grid(color="k", alpha=0.2, linestyle=":", zorder=1)
chart.legend(fontsize=10)
plt.ylim(ymin=0, ymax=5)
plt.xlim(xmin=-0.5, xmax=7.5)

plt.subplots_adjust(
    top=0.949, bottom=0.356, left=0.227, right=0.968, hspace=0.2, wspace=0.2
)

plt.show()
plt.savefig("Fig_4_rmse.png", dpi=600)
# plt.savefig("Fig_4_rmse.svg")
