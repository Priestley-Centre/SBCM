import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

plt.close("all")

### Based on this quite remarkable stack overflow technique
### https://stackoverflow.com/a/70022316/4741979


def find_intersection(first_line, second_line):
    """
    this functions takes the variables m and beta of two lines
    and returns the intersection point coordinates x, y
    """
    x = (second_line[1] - first_line[1]) / (first_line[0] - second_line[0])
    y = first_line[0] * x + first_line[1]
    return x, y


def find_m_beta(x1, y1, x2, y2):
    """
    this functions calculates m and beta of a line
    given two coordinates x1,y1 and x2,y2
    """
    if x2 != x1:
        m = (y2 - y1) / (x2 - x1)
    else:
        m = 0
    beta = y2 - m * x2

    return m, beta


def find_m_beta_bounds(df):
    """
    this function finds the equations of all lines
    that can be created by the given dataframe.
    It only calculates lines of points that are consequent.
    For example:
        index     x  y
          0       0  1
          1       1  2
          2       3  4
    Given the above dataframe, the function will find two equations:
    namely m and beta of the line between points with indexes 0 and 1
    and  m and beta of the line between points with indexes 1 and 2.
    It will also return the boundaries of these lines
    """
    data_points = df.to_numpy()
    vars = []
    bounds_x, bounds_y = [], []

    # find m, beta and bounds for each line in df
    for idx, item in enumerate(data_points):
        if idx == len(data_points) - 1:
            break
        x1 = item[1]
        y1 = item[0]
        x2 = data_points[idx + 1][1]
        y2 = data_points[idx + 1][0]

        m, beta = find_m_beta(x1, y1, x2, y2)
        vars.append([m, beta])
        bounds_x.append([min([x1, x2]), max([x1, x2])])
        bounds_y.append([min([y1, y2]), max([y1, y2])])
    return vars, bounds_x, bounds_y


def implement(df1, df2):
    # our dataframes
    df1 = pd.DataFrame({"y": df1[1:], "x": df1.index.values[1:]})
    df2 = pd.DataFrame({"y": df2[1:], "x": df2.index.values[1:]})

    # get vars (m,beta) and bounds (x,y) for each line in df1 and in df2
    # where y = mx +beta
    vars_df1, bounds_x_df1, bounds_y_df1 = find_m_beta_bounds(df1)
    vars_df2, bounds_x_df2, bounds_y_df2 = find_m_beta_bounds(df2)

    # find interesections of all lines of df1 and df2
    all_intersections_x, all_intersections_y = [], []
    for idx, item in enumerate(vars_df1):
        for idx_, item_ in enumerate(vars_df2):
            x, y = find_intersection(item, item_)
            # accept intersection only if (x,y) are in bounds of both investigated lines
            if (
                x >= bounds_x_df1[idx][0]
                and x <= bounds_x_df1[idx][1]
                and y >= bounds_y_df1[idx][0]
                and y <= bounds_y_df1[idx][1]
                and x >= bounds_x_df2[idx_][0]
                and x <= bounds_x_df2[idx_][1]
                and y >= bounds_y_df2[idx_][0]
                and y <= bounds_y_df2[idx_][1]
            ):
                all_intersections_x.append(x)
                all_intersections_y.append(y)

    # plot
    # fig = plt.figure(figsize=(10, 6))
    # ax = plt.gca()

    # ax.plot(df1["x"], df1["y"], color="red")
    # ax.plot(df2["x"], df2["y"], color="green")
    # ax.scatter(all_intersections_x, all_intersections_y)
    # plt.show()
    pbk = ([], [])
    for i in range(len(all_intersections_x)):
        # print(math.ceil(all_intersections_x[i]),math.ceil(all_intersections_y[i]))
        pbk[0].append(math.floor(all_intersections_x[i]))
        pbk[1].append(math.floor(all_intersections_y[i]))
    return pbk


# if __name__ == "__main__":
#     data = pd.read_csv("test.csv", index_col="Unnamed: 0")
#     runs = ["s1", "s2", "s3", "s4", "s5", "s6"]

#     for r in runs:
#         result = implement(data["cf"], data[r])
#         print(result[0], result[1])
