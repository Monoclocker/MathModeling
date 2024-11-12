import numpy as np
import sympy as smp
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib import animation

time = 20
steps = 1000

def system_symbols():
    m, k, g, t = smp.symbols("m k g t")
    Theta = smp.Function("Theta")(t)
    r = smp.Function("r")(t)
    return m, k, g, t, Theta, r

def lagrangian(m, g, k, t, Theta, r):
    x = (1 + r) * smp.cos(Theta)
    y = -(1 + r) * smp.sin(Theta)

    T = 0.5 * m * (smp.diff(x, t) ** 2 + smp.diff(y, t) ** 2)
    V = m * g * y + 0.5 * k * r ** 2
    return T - V, x, y

def lagrange_equations(L, Theta, r, t):
    Theta_d = smp.diff(Theta, t)
    Theta_dd = smp.diff(Theta_d, t)
    r_d = smp.diff(r, t)
    r_dd = smp.diff(r_d, t)

    LE_Theta = smp.diff(L, Theta) - smp.diff(smp.diff(L, Theta_d), t)
    LE_r = smp.diff(L, r) - smp.diff(smp.diff(L, r_d), t)

    return smp.solve([LE_Theta, LE_r], (Theta_dd, r_dd))

def lambdified_functions(m, k, g, Theta, r, Theta_d, r_d, sols, Theta_dd, r_dd):
    dw_dt = smp.lambdify((m, k, g, Theta, r, Theta_d, r_d), sols[Theta_dd])
    dv_dt = smp.lambdify((m, k, g, Theta, r, Theta_d, r_d), sols[r_dd])
    return dw_dt, dv_dt

def dsdt(S, t, m, k, g, dw_dt, dv_dt):
    Theta, omega, r, v = S
    return [
        omega,
        dw_dt(m, k, g, Theta, r, omega, v),
        v,
        dv_dt(m, k, g, Theta, r, omega, v)
    ]

def show():
    t_vals = np.linspace(0, time, steps)
    initial_conditions = [np.pi / 2, 1, 1, 7]
    m_val, k_val, g_val = 1, 10, 9.81


    m, k, g, t, Theta, r = system_symbols()
    L, x, y = lagrangian(m, g, k, t, Theta, r)
    Theta_d, Theta_dd, r_d, r_dd = (smp.diff(Theta, t), smp.diff(smp.diff(Theta, t), t),
                                    smp.diff(r, t), smp.diff(
                                        smp.diff(r, t), t))
    sols = lagrange_equations(L, Theta, r, t)
    dw_dt, dv_dt = lambdified_functions(m, k, g, Theta, r, Theta_d, r_d, sols, Theta_dd, r_dd)

    solution = odeint(dsdt, y0=initial_conditions, t=t_vals, args=(m_val, k_val, g_val, dw_dt, dv_dt))

    x_vals = (1 + solution[:, 2]) * np.cos(solution[:, 0])
    y_vals = -(1 + solution[:, 2]) * np.sin(solution[:, 0])

    fig = plt.figure(figsize=(8, 6))

    ax = plt.subplot2grid((4, 2), (0, 0), colspan=2, rowspan=2)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.grid()

    ax2 = plt.subplot2grid((4, 2), (2, 0), colspan=1, rowspan=2)
    ax2.plot(t_vals, x_vals, 'r')
    ax2.set_title("Отклонения по X", loc="center")

    ax3 = plt.subplot2grid((4, 2), (2, 1), colspan=1, rowspan=2)
    ax3.plot(t_vals, y_vals, 'g')
    ax3.set_title("Отклонения по Y", loc="center")

    ln, = ax.plot([], [], 'k-', lw=2)
    mass, = ax.plot([], [], 'gs', markersize=10)

    def init():
        ln.set_data([], [])
        mass.set_data([], [])
        return ln, mass

    def animate(i):
        ln.set_data([0, x_vals[i]], [0, y_vals[i]])
        mass.set_data([x_vals[i]], [y_vals[i]])
        return ln, mass

    interval = (time / steps) * 1000

    ani = animation.FuncAnimation(fig, animate, frames=steps, init_func=init, interval=interval, blit=True)
    plt.show()

if __name__ == '__main__':
    show()
