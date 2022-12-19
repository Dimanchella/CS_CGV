import math
import sys
import matplotlib.pyplot as plt
import numpy as np
import itertools as it
import random as rand
import json
import csv

ERROR_CODE = -1

PLOT_STEPS_X = 55
PLOT_STEPS_Y = 55
NUMBER_SAVED_RANDOM_INNER_POINTS = 5
NUMBER_SAVED_INNER_POINTS = 20


def calculate_points(
        kxc: int, kyc: int, dc: int,
        ac: float, bc: float, cc: float,
        uc: int, vc: int, hxc: float, hyc: float):
    xsc = [hxc * i for i in range(uc)]
    ysc = [hyc * j for j in range(vc)]

    fc = [[0] * uc for _ in range(vc)]
    fc[0][0] = math.sin(dc)
    for ij in range(1, max(uc, vc)):
        if ij < uc:
            fc[0][ij] = math.sin(kxc * xsc[ij] + dc)
        if ij < vc:
            fc[ij][0] = math.sin(kyc * ysc[ij] + dc)

    ahy3 = 3 * ac * hyc
    bhx3 = 3 * bc * hxc
    chxhy = cc * hxc * hyc

    for i, j in it.product(range(1, uc), range(1, vc)):
        n_k = 3 / pow(3, 1 / 3) * (fc[j - 1][i] + fc[j][i - 1] + fc[j - 1][i - 1]) \
              * (ahy3 - bhx3 - chxhy)
        fc[j][i] = (ahy3 * fc[j][i - 1]
                    - bhx3 * fc[j - 1][i]
                    + chxhy * fc[j - 1][i - 1]) / n_k
    return [xsc, ysc, fc]


def save_values(
        al_save: float, bl_save: float, kx_save: int, ky_save: int,
        d_save: int, a_save: float, b_save: float, c_save: float,
        hx_save: float, hy_save: float, u_save: int, v_save: int,
        num_outer_p: int, num_inner_p: int, accuracy: float,
        xsl: list[float], ysl: list[float], fsl: list[float]
):
    saving_data = [("A =", al_save, "", "d =", d_save),
                   ("B =", bl_save, "", "a =", a_save),
                   ("kx =", kx_save, "", "b =", b_save),
                   ("ky =", ky_save, "", "c =", c_save), (),
                   ("hx =", hx_save, "", "u =", u_save),
                   ("hy =", hy_save, "", "v =", v_save), (),
                   ("outer pts =", num_outer_p),
                   ("inner pts =", num_inner_p),
                   ("accuracy =", accuracy), (),
                   ("random points",),
                   ("N", "i", "j", "x[i]", "y[i]", "f[i][j]")]
    num_points_x: int
    num_points_y: int
    if NUMBER_SAVED_RANDOM_INNER_POINTS < 1:
        num_points_x = 1
        num_points_y = 1
    else:
        num_points_x = int(math.sqrt(NUMBER_SAVED_RANDOM_INNER_POINTS))
        num_points_y = math.ceil(NUMBER_SAVED_RANDOM_INNER_POINTS / num_points_x)

    counter = 0
    for _, _ in it.product(range(1, num_points_x + 1), range(1, num_points_y + 1)):
        counter += 1
        i = rand.randint(0, u_save - 1)
        j = rand.randint(0, v_save - 1)
        saving_data.append((counter, i, j, xsl[i], ysl[j], fsl[j][i]))
        if counter == NUMBER_SAVED_RANDOM_INNER_POINTS:
            break

    saving_data.extend(
        [(), ("inner neighboring points",),
         ("N", "i", "j", "x[i]", "y[i]", "f[i][j]")])

    if NUMBER_SAVED_INNER_POINTS < 1:
        num_points_x = len(xsl) - 1
        num_points_y = len(ysl) - 1
    else:
        num_points_x = int(math.sqrt(NUMBER_SAVED_INNER_POINTS))
        num_points_y = math.ceil(NUMBER_SAVED_INNER_POINTS / num_points_x)

    counter = 0
    for i, j in it.product(range(1, num_points_x + 1), range(1, num_points_y + 1)):
        counter += 1
        saving_data.append((counter, i, j, xsl[i], ysl[j], fsl[j][i]))
        if counter == NUMBER_SAVED_INNER_POINTS:
            break
    try:
        with open("output2.csv", "w+", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerows(saving_data)
    except PermissionError as perm:
        print(f"Доступ к файлу output4.csv запрещён.\n{perm}")
        sys.exit(ERROR_CODE)


def show_plot(xsl: list[float], ysl: list[float], fsl: list[list[float]]):
    fig = plt.figure()

    x2d = np.array(xsl)
    fx2d = np.array(fsl[-1])
    aver = sum(fx2d) / len(fx2d)
    lim_f = max(math.fabs(min(fx2d) - aver), math.fabs(max(fx2d) - aver)) * 1.5
    ax = fig.add_subplot(2, 2, 1)
    ax.plot(x2d, fx2d, color="black")
    ax.grid(True)
    ax.set_facecolor("lightgray")
    ax.set_xlabel(r"$x_i$")
    ax.set_ylabel(r"$f_{i,B}$")
    ax.set_ylim(aver - lim_f, aver + lim_f)

    y2d = np.array(ysl)
    fy2d = np.array(list(map(lambda fx: fx[-1], fsl)))
    aver = sum(fy2d) / len(fy2d)
    lim_f = max(math.fabs(min(fy2d) - aver), math.fabs(max(fy2d) - aver)) * 1.5
    ax = fig.add_subplot(2, 2, 3)
    ax.plot(y2d, fy2d, color="black")
    ax.grid(True)
    ax.set_facecolor("lightgray")
    ax.set_xlabel(r"$y_i$")
    ax.set_ylabel(r"$f_{A,j}$")
    ax.set_ylim(aver - lim_f, aver + lim_f)

    x3d, y3d = np.meshgrid(xsl, ysl)
    f3d = np.array(fsl)
    ax = fig.add_subplot(1, 2, 2, projection="3d")
    ax.plot_surface(x3d, y3d, f3d, cmap="gray", linewidth=0, antialiased=False)
    ax.set_facecolor("lightgray")
    ax.set_xlabel(r"$x_i$")
    ax.set_ylabel(r"$y_j$")
    ax.set_zlabel(r"$f_{i,j}$")

    plt.subplots_adjust(left=0.05, bottom=0.1, right=0.95, top=0.9)
    plt.show()


if __name__ == '__main__':
    n: int
    dd: int
    mm: int
    yyyy: int
    try:
        with open("input.json", "r") as json_file:
            reading_data = json.load(json_file)
            n = reading_data["N"]
            dd = reading_data["DD"]
            mm = reading_data["MM"]
            yyyy = reading_data["YYYY"]
    except FileNotFoundError as fnf:
        print(f"Файл input.json не найден.\n{fnf}")
        sys.exit(ERROR_CODE)

    A = (mm * 100 + dd) / 12
    B = (dd * 100 + mm) / 31
    kx = (11 * n + dd) % 7 + 3
    ky = (13 * n + mm) % 7 + 3
    d = (7 * n + mm) % 5 + 3
    a = ((dd + mm) % 11 + dd * 100 + mm) / yyyy
    b = ((dd + mm) % 13 + mm * 100 + dd) / yyyy
    c = (dd * 100 + mm + 31) / yyyy

    hx = dd / 99
    hy = mm / 99
    u = int(A // hx)
    v = int(B // hy)

    xs, ys, fs = calculate_points(
        kx, ky, d, a, b, c, u, v, hx, hy)
    num_outp = (u - 1) * 2 + (v - 1) * 2
    num_inp = (u - 2) * (v - 2)
    average = sum(map(sum, fs)) / (u * v)
    save_values(
        A, B, kx, ky, d, a, b, c, hx, hy, u, v,
        num_outp, num_inp, average, xs, ys, fs)

    px = 1
    up = u
    py = 1
    vp = v
    if PLOT_STEPS_X > 1:
        px = A * 99 / (dd * PLOT_STEPS_X)
        up = PLOT_STEPS_X
    if PLOT_STEPS_Y > 1:
        py = B * 99 / (mm * PLOT_STEPS_Y)
        vp = PLOT_STEPS_Y
    if PLOT_STEPS_Y > 1 or PLOT_STEPS_Y > 1:
        xs, ys, fs = calculate_points(
            kx, ky, d, a, b, c, up, vp, hx * px, hy * py)
    show_plot(xs, ys, fs)
