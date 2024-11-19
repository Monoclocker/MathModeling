import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from lab2.main import omega

# Начальные параметры мяча и физики
g = 9.8
x0, y0 = 0, 0      # Начальные координаты мяча
U0, V0 = 20, -20   # Начальные скорости мяча
ht = 0.1           # Шаг по времени
ball_radius = 1    # Радиус мяча

x_min, x_max = -120, 120   # Координаты вертикальных линий-ограничителей
A1 = 15
omega1 = 0.1
phi1 = 15
D1 = -50

A2 = 15
omega2 = 0.3
phi2 = 25
D2 = 50

def calculate_sin(x, A, omega, phi, D):
    return A * math.sin(omega * x + phi) + D


def calculate_normal(x, A, omega, phi, D):
    # Вычисление нормали синусоиды
    dy_dx = A * omega * math.cos(omega * x + phi)
    norm = math.sqrt(dy_dx ** 2 + 1)
    return -dy_dx / norm, 1 / norm


def get_pos():
    x, y, U, V = x0, y0, U0, V0

    while True:
        x_new = x + U * ht
        y_new = y + V * ht - 0.5 * g * ht ** 2  # Учет ускорения свободного падения

        V -= g * ht  # Обновляем скорость по вертикали

        # Проверка столкновения с боковыми границами
        if x_new <= x_min or x_new >= x_max:
            U = -U

        # Проверка столкновения с нижней синусоидой
        elif y_new <= calculate_sin(x_new, A1, omega1, phi1, D1):
            nx, ny = calculate_normal(x_new, A1, omega1, phi1, D1)
            U, V = U - 2 * (U * nx + V * ny) * nx, V - 2 * (U * nx + V * ny) * ny
            y_new = calculate_sin(x_new, A1, omega1, phi1, D1)  # Коррекция позиции

        # Проверка столкновения с верхней синусоидой
        elif y_new >= calculate_sin(x_new, A2, omega2, phi2, D2):
            nx, ny = calculate_normal(x_new, A2, omega2, phi2, D2)
            U, V = U - 2 * (U * nx + V * ny) * nx, V - 2 * (U * nx + V * ny) * ny
            y_new = calculate_sin(x_new, A2, omega2, phi2, D2)

        # Обновляем позицию
        x, y = x_new, y_new

        yield x, y

# Инициализация графики
def init():
    ax.set_xlim(-150, 150)
    ax.set_ylim(-150, 150)

    # Рисуем боковые границы как вертикальные линии
    ax.axvline(x_min, color="red")
    ax.axvline(x_max, color="red")

    x_sin_low = [x for x in range(-150, 150)]
    y_sin_low = [calculate_sin(x, A1, omega1, phi1, D1) for x in x_sin_low]
    ax.plot(x_sin_low, y_sin_low, color="blue")

    x_sin_high = [x for x in range(-150, 150)]
    y_sin_high = [calculate_sin(x, A2, omega2, phi2, D2) for x in x_sin_high]
    ax.plot(x_sin_high, y_sin_high, color="blue")

    # Инициализация мяча
    ball.set_center((x0, y0))
    return ball

# Анимация
def animate(pos):
    x, y = pos
    ball.set_center((x, y))  # Обновление только положения мяча
    return ball

# Настройка графика
fig, ax = plt.subplots()
fig.patch.set_facecolor('white')
ax.set_facecolor("white")
ax.set_aspect('equal')

# Мяч
ball = plt.Circle((x0, y0), ball_radius, color='green')
ax.add_patch(ball)

# Настройки анимации
interval = 30
ani = animation.FuncAnimation(fig, animate, get_pos, interval=interval, repeat=False, init_func=init)

# Показ графика
plt.show()
