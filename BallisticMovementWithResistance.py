import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def ballistic_trajectory_with_resistance(h, v0, theta, k, dt=0.01):

    theta_rad = np.radians(theta)


    v0x = v0 * np.cos(theta_rad)
    v0y = v0 * np.sin(theta_rad)

    g = 9.81

    x, y = [0], [h]
    vx, vy = v0x, v0y
    t = [0]
    v = [np.sqrt(v0x**2 + v0y**2)]


    def derivatives(vx, vy, k, g):
        ax = -k * vx
        ay = -g - k * vy
        return ax, ay


    while y[-1] >= 0:
        k1x, k1y = derivatives(vx, vy, k, g)
        k2x, k2y = derivatives(vx + 0.5 * dt * k1x, vy + 0.5 * dt * k1y, k, g)
        k3x, k3y = derivatives(vx + 0.5 * dt * k2x, vy + 0.5 * dt * k2y, k, g)
        k4x, k4y = derivatives(vx + dt * k3x, vy + dt * k3y, k, g)

        vx += (dt / 6) * (k1x + 2 * k2x + 2 * k3x + k4x)
        vy += (dt / 6) * (k1y + 2 * k2y + 2 * k3y + k4y)

        x.append(x[-1] + vx * dt)
        y.append(y[-1] + vy * dt)
        t.append(t[-1] + dt)
        v.append(np.sqrt(vx**2 + vy**2))

    return np.array(t), np.array(x), np.array(y), np.array(v)


def create_animation(t, x, y, v, filename, color):
    fig, ax = plt.subplots()
    ax.set_xlim(0, max(x))
    ax.set_ylim(0, max(y))
    ax.set_xlabel('x (м)')
    ax.set_ylabel('y (м)')
    ax.set_title('Траектория движения тела с учетом сопротивления воздуха')

    line, = ax.plot([], [], 'o-', lw=2, color=color)
    speed_text = ax.text(0.1, 0.95, '', transform=ax.transAxes, color=color, fontsize=12, verticalalignment='top')

    def init():
        line.set_data([], [])
        speed_text.set_text('')
        return line, speed_text

    def update(i):
        line.set_data(x[:i], y[:i])
        speed_text.set_text(f'Скорость: {v[i]:.2f} м/с')
        return line, speed_text

    ani = FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True, interval=20)
    ani.save(filename, writer='pillow')


def plot_speed_time(t, v, filename, color):
    plt.figure()
    plt.plot(t, v, label='Скорость', color=color)
    plt.xlabel('Время (с)')
    plt.ylabel('Скорость (м/с)')
    plt.title('Зависимость скорости от времени')
    plt.legend()
    plt.savefig(filename)
    plt.close()


def plot_coordinate_time(t, x, filename, color):
    plt.figure()
    plt.plot(t, x, label='Координата x', color=color)
    plt.xlabel('Время (с)')
    plt.ylabel('Координата x (м)')
    plt.title('Зависимость координаты x от времени')
    plt.legend()
    plt.savefig(filename)
    plt.close()


def main():

    h = float(input("Введите высоту, с которой брошено тело в метрах: "))
    v0 = float(input("Введите начальную скорость в м/c: "))
    theta = float(input("Введите угол, под которым брошено тело в градусах: "))
    k = float(input("Введите коэффициент сопротивления воздуха (k): "))

    color = '#ff73f1'

    t, x, y, v = ballistic_trajectory_with_resistance(h, v0, theta, k)

    create_animation(t, x, y, v, 'ballistic_trajectory_with_resistance.gif', color)

    plot_speed_time(t, v, 'speed_time_with_resistance.png', color)
    plot_coordinate_time(t, x, 'coordinate_time_with_resistance.png', color)

if __name__ == "__main__":
    main()
