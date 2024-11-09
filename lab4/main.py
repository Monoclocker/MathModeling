import numpy as np
import sympy as smp
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib import animation


# Параметры системы (определяем их символически)
def system_params():
    return smp.symbols("m k g t")

# Символы для угла и длины нити
def angle_and_length_symbols(t):
    Theta = smp.Function("Theta")(t)    # Угол отклонения маятника
    r = smp.Function("r")(t)            # Длина нити
    return Theta, r

# Производные для угла и длины
def angle_and_length_diffs(Theta, r, t):
    Theta_d = smp.diff(Theta, t)
    Theta_dd = smp.diff(Theta_d, t)
    r_d = smp.diff(r, t)
    r_dd = smp.diff(r_d, t)
    return Theta_d, Theta_dd, r_d, r_dd

# Определение координат груза
def coordinates_definition(Theta, r):
    x = (1 + r) * smp.cos(Theta)
    y = -(1 + r) * smp.sin(Theta)
    return x, y

def lagranjian(m, t, g, k, r, x, y):
    T = 0.5 * m * (smp.diff(x, t) ** 2 + smp.diff(y, t) ** 2)
    V = m * g * y + 0.5 * k * r ** 2
    L = T - V
    return L

def angle_movement(Theta, Theta_d, r, r_d, L, t):
    LE_Theta = smp.diff(L, Theta) - smp.diff(smp.diff(L, Theta_d), t)
    LE_r = smp.diff(L, r) - smp.diff(smp.diff(L, r_d), t)
    return LE_Theta, LE_r

# Решаем уравнения относительно вторых производных
def second_diffs_solution(LE_Theta, LE_r, Theta_dd, r_dd):
    return smp.solve([LE_Theta, LE_r], (Theta_dd, r_dd))

# Функции для численного решения
def numeric_solution(m, k, g, Theta, r, Theta_d, r_d, sols, Theta_dd, r_dd):
    dw_dt = smp.lambdify((m, k, g, Theta, r, Theta_d, r_d), sols[Theta_dd])
    dv_dt = smp.lambdify((m, k, g, Theta, r, Theta_d, r_d), sols[r_dd])
    return dw_dt, dv_dt

# Система дифференциальных уравнений
def dsdt(S, t, m_val, k_val, g_val, dw_dt, dv_dt):
    Theta, omega, r, v = S
    return [
        omega,
        dw_dt(m_val, k_val, g_val, Theta, r, omega, v),
        v,
        dv_dt(m_val, k_val, g_val, Theta, r, omega, v)
    ]

def show():
    # Начальные условия и параметры
    t_vals = np.linspace(0, 20, 1000)
    initial_conditions = [np.pi / 2, 1, 1, 7]
    m_val, k_val, g_val = 1, 10, 9.81

    m, k, g, t = system_params()
    Theta, r = angle_and_length_symbols(t)
    Theta_d, Theta_dd, r_d, r_dd = angle_and_length_diffs(Theta, r, t)
    x, y = coordinates_definition(Theta, r)
    L = lagranjian(m, t, g, k, r, x, y)
    LE_Theta, LE_r = angle_movement(Theta, Theta_d, r, r_d, L, t)
    sols = second_diffs_solution(LE_Theta, LE_r, Theta_dd, r_dd)

    dw_dt, dv_dt = numeric_solution(m, k, g, Theta, r, Theta_d, r_d, sols, Theta_dd, r_dd)

    # Решение уравнений
    solution = odeint(dsdt, y0=initial_conditions, t=t_vals, args=(m_val, k_val, g_val, dw_dt, dv_dt))

    # Вычисляем координаты груза на основе решения
    x_vals = (1 + solution[:, 2]) * np.cos(solution[:, 0])
    y_vals = -(1 + solution[:, 2]) * np.sin(solution[:, 0])

    # Анимация маятника
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.grid()

    # Нить и груз
    ln, = plt.plot([], [], 'k-', lw=2)
    mass, = plt.plot([], [], 'gs', markersize=10)
    circle = plt.Circle((0, 0), np.max(np.sqrt(x_vals ** 2 + y_vals ** 2)), color='blue', fill=False, linestyle='--')
    ax.add_artist(circle)

    def animate(i):
        ln.set_data([0, x_vals[i]], [0, y_vals[i]])  # Нить
        mass.set_data([x_vals[i]], [y_vals[i]])  # Груз как точка

    ani = animation.FuncAnimation(fig, animate, frames=500, interval=1)
    plt.show()

def main():
    show()

if __name__ == '__main__':
    main()
