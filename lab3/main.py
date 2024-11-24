from math import sin, cos
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation

g = 9.8
leng = 1.0
b_const = 0.2


# no decay case:
def pendulum_equations1(w, t, l):
    th, v = w
    dth = v
    dv = - g / l * sin(th)
    return dth, dv


# the decay exist case:
def pendulum_equations2(w, t, l, b):
    th, v = w
    dth = v
    dv = -b / l * v - g / l * sin(th)
    return dth, dv


t = np.arange(0, 20, 0.1)
# track = odeint(pendulum_equations1, (1.0, 0), t, args=(leng,))
track = odeint(pendulum_equations2, (1.0, 0), t, args=(leng, b_const))
xdata = [leng * sin(track[i, 0]) for i in range(len(track))]
ydata = [-leng * cos(track[i, 0]) for i in range(len(track))]

fig, ax = plt.subplots()
ax.grid()
line, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    time_text.set_text('')
    return line, time_text


def update(i):
    newx = [0, xdata[i]]
    newy = [0, ydata[i]]
    line.set_data(newx, newy)
    time_text.set_text(time_template % (0.1 * i))
    return line, time_text


ani = animation.FuncAnimation(fig, update, range(1, len(xdata)), init_func=init, interval=10)
# ani.save('single_pendulum_decay.gif', writer='imagemagick', fps=100)
# ani.save('single_pendulum_nodecay.gif', writer='imagemagick', fps=100)
plt.show()