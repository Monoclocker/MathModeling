import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import legend

g = 9.81
l = 1
m = 1
analytic_const = 0.6

# начальный угол отклонения
alpha0 = 1

# начальная угловая скорость
omega0 = 0

dt = 0.01
max_time = 10
time = np.arange(0, max_time+dt, dt)


def calculate_analytic():
    new_alphas = []
    omega = math.sqrt(g / l)

    for t in time:
        new_alpha = (alpha0 * math.cos(omega * t)
                    + omega * omega0 * analytic_const * math.sin(omega * t))
        new_alphas.append(new_alpha)

    return new_alphas

def calculate_euler():
    new_alphas = []
    alpha = alpha0
    omega = omega0

    for _ in time:
        new_alphas.append(alpha)

        omega += -g * math.sin(alpha) * dt / l
        alpha += omega * dt

    return new_alphas

def calculate_euler_linear():
    new_alphas = []
    alpha = alpha0
    omega = omega0

    for _ in time:
        new_alphas.append(alpha)

        omega += -g * alpha * dt / l
        alpha += omega * dt

    return new_alphas

def main():

    alphas_analytic = calculate_analytic()
    alphas_euler = calculate_euler()
    alphas_euler_linear = calculate_euler_linear()

    plt.plot(time, alphas_analytic)
    plt.plot(time, alphas_euler)
    plt.plot(time, alphas_euler_linear)
    plt.legend(["Аналитическое решение", "Решение через sin(a)", "Решение через a"], loc="lower right")

    plt.show()

main()