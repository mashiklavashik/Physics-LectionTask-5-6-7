import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


m = 4
g = 9.81
L = 0.3
k = 100
omega = np.sqrt(k / m)


def force_spring(x, y, t):
    r = np.sqrt(x**2 + y**2)
    F_spring = -k * (r - L) * np.array([x, y]) / r
    F_gravity = np.array([0, -m * g])
    F_total = F_spring + F_gravity
    return F_total

def potential_energy(x, y):
    r = np.sqrt(x**2 + y**2)
    U_spring = 0.5 * k * (r - L)**2
    U_gravity = m * g * y
    return U_spring + U_gravity


x = np.linspace(-0.5, 0.5, 100)
y = np.linspace(-0.5, 0.5, 100)
X, Y = np.meshgrid(x, y)


fig, ax = plt.subplots(figsize=(6, 6))
contour = ax.contourf(X, Y, potential_energy(X, Y), levels=50, cmap='viridis')
ax.set_title("Потенциальное поле U(x, y)")
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
fig.colorbar(contour, ax=ax, label="Потенциальная энергия (J)")


def update(frame):

    displacement = 0.1 * np.cos(omega * frame)
    Z = potential_energy(X + displacement, Y)
    ax.clear()
    contour = ax.contourf(X, Y, Z, levels=50, cmap='viridis')
    ax.set_title("Потенциальное поле U(x, y)")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    return contour


ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 60), interval=100)
ani.save("potential_energy_field_oscillation.gif", writer="imagemagick")
plt.show()
