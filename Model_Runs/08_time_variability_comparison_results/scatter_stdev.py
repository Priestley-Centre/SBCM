import numpy as np
import matplotlib.pyplot as plt
import formatting as form
from scipy.stats.stats import linregress
import pandas as pd
from variables import SPP as spp
import statistics

x_all1 = []
y_all1 = []
x_all2 = []
y_all2 = []

form.mpl_font_setup()
mm = (146, 100)  # x value then y value
inches = (mm[0] / 25.4, mm[1] / 25.4)
fig = plt.figure(figsize=inches)

palette = plt.get_cmap("tab10")
chart = fig.add_subplot(1, 1, 1)

for sp in spp:

    index = spp.index(sp)
    data = pd.read_csv(f"{sp}_values.csv")
    x = list(data["x"])
    y = list(data["y"])
    x_var = statistics.stdev(x)
    y_var = statistics.stdev(y)
    print(f"{sp} x = {x_var} y = {y_var}")
    x_all1 = x_all1 + [np.mean(x)]
    y_all1 = y_all1 + [y_var]
    x_all2 = x_all2 + [np.mean(x)]
    y_all2 = y_all2 + [np.mean(y)]

    plot = chart.errorbar(
        np.mean(x),
        np.mean(y),
        yerr=y_var,
        xerr=x_var,
        color=palette(index),
        #        label="col_1",
        ls="none",
        marker="o",
        capsize=3,
        linewidth=0.5,
        label=form.forest_labels(sp, short="star", eng=True),
    )


slope, intercept, r_value, p_value, std_err = linregress(x_all1, y_all1)
# https://blog.minitab.com/blog/adventures-in-statistics-2/how-to-interpret-regression-analysis-results-p-values-and-coefficients


print(f"r\N{SUPERSCRIPT TWO} value = {r_value}")
print(f"p value = {p_value}")
slope, intercept, r_value, p_value, std_err = linregress(x_all2, y_all2)
r_value = np.round(r_value, 2)

r_line_x = np.arange(-100, 3500, 100)
r_line_y = intercept + r_line_x * slope
plot = chart.plot(r_line_x, r_line_y, marker=None, color="k", ls=":")


chart.set_ylabel("Site carbon at equilibrium (tC.ha$^{-1}$)", fontsize=12)
chart.set_xlabel(
    "Extention of site carbon curves\n beyond training data (years)", fontsize=12
)
chart.tick_params(axis="both", which="major", labelsize=10)
# note = f"r$^2$ = {r_value}"  # \np = {float(p_value):.8}"
# chart.text(-50, 50, f"{note}", bbox_to_anchor=(0, 1),fontsize=12)

# fig.text(0.8, 0.1, f"{note}", ha="center", fontsize=12)


chart.legend(
    ncol=1,
    loc="center right",
    bbox_to_anchor=(1, 1, 0.8, -1),
    borderaxespad=0,
    frameon=False,
    labelspacing=0.75,
)


chart.grid(color="k", alpha=0.2, linestyle=":", zorder=1)
plt.ylim(ymin=150, ymax=600)
plt.xlim(xmin=0, xmax=3000)

plt.subplots_adjust(
    top=0.949, bottom=0.197, left=0.123, right=0.585, hspace=0.2, wspace=0.2
)

plt.show()
plt.savefig("Fig_7_time_uncertainty.png", dpi=600)
# plt.savefig("Fig_7_time_uncertainty.svg")
