import pygame
from math import sqrt

# Параметры окна и цветов
WIN_WIDTH, WIN_HEIGHT = 800, 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
SPACE_COLOR = (30, 30, 30)  # Тёмно-серый
SUN_COLOR = (255, 204, 0)   # Жёлтый
PLANET_COLOR = (0, 102, 255)  # Синий
TRAIL_COLOR = (100, 100, 100)  # Серый для следа

# Параметры Солнца
SUN_RADIUS = 15
SUN_MASS = 5000
X0, Y0 = WIN_WIDTH // 2, WIN_HEIGHT // 2  # Центр экрана

# Параметры планеты
PLANET_RADIUS = 6
CRASH_DIST = 10
OUT_DIST = 1000

# Функция для расчёта гравитационного ускорения
def calculate_acceleration(x, y, mass, center_x, center_y):
    r = sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    ax = mass * (center_x - x) / r ** 3
    ay = mass * (center_y - y) / r ** 3
    return ax, ay

def main():
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Planet Orbit Simulation")

    # Создание заднего фона
    bg = pygame.Surface(DISPLAY)
    bg.fill(SPACE_COLOR)
    pygame.draw.circle(bg, SUN_COLOR, (X0, Y0), SUN_RADIUS)

    # Параметры планеты
    x, y = 100.0, 290.0  # Начальная позиция
    vx, vy = 0.1, 1.5    # Начальная скорость
    ax, ay = 0.0, 0.0    # Ускорение

    trail = []  # Для хранения следа планеты
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Вычисление ускорения
        ax, ay = calculate_acceleration(x, y, SUN_MASS, X0, Y0)

        # Обновление скорости и положения
        vx += ax
        vy += ay
        x += vx
        y += vy

        # Рисование следа планеты
        trail.append((int(x), int(y)))
        if len(trail) > 500:  # Ограничиваем длину следа
            trail.pop(0)
        for point in trail:
            pygame.draw.circle(screen, TRAIL_COLOR, point, 1)

        # Рисование планеты
        pygame.draw.circle(screen, PLANET_COLOR, (int(x), int(y)), PLANET_RADIUS)

        # Проверка выхода за пределы экрана
        if not (0 <= x <= WIN_WIDTH and 0 <= y <= WIN_HEIGHT):
            print("Планета покинула границы экрана.")
            running = False

        pygame.display.flip()
        clock.tick(120)  # Ограничение FPS

    pygame.quit()

if __name__ == "__main__":
    main()
