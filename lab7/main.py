import pygame
import sys
import math

# --- Класс для квадрата ---
class Square:
    def __init__(self, x, y, vx, vy, size, mass, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.mass = mass
        self.color = color
        self.angle = 0  # Угол поворота (в градусах)
        self.angular_velocity = 0  # Угловая скорость

        # Создаём поверхность квадрата
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.surface.fill(self.color)  # Заливаем квадрат цветом

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Поворот квадратов с учётом угловой скорости
        self.angle += self.angular_velocity

    def check_collision_with_walls(self, width, height):
        if self.x <= 0 or self.x + self.size >= width:
            self.vx = -self.vx
        if self.y <= 0 or self.y + self.size >= height:
            self.vy = -self.vy

    def check_collision_with_square(self, other):
        # Проверка пересечения прямоугольников
        if (
            self.x < other.x + other.size and
            self.x + self.size > other.x and
            self.y < other.y + other.size and
            self.y + self.size > other.y
        ):
            # При столкновении меняем угловые скорости
            self.angular_velocity += 0.1 * (self.vx - other.vx)
            other.angular_velocity += 0.1 * (other.vx - self.vx)

            # Обмен скоростями для линейного движения
            self.vx, other.vx = other.vx, self.vx
            self.vy, other.vy = other.vy, self.vy

    def render(self, screen):
        # Поворот квадратов
        rotated_square = pygame.transform.rotate(self.surface, self.angle)
        rotated_rect = rotated_square.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))

        # Рисуем повернутый квадрат
        screen.blit(rotated_square, rotated_rect.topleft)

# --- Класс для симуляции ---
class Simulation:
    def __init__(self):
        # Задаём размер экрана
        self.width = 800
        self.height = 600
        self.squares = []

        # Задаём начальные данные для квадратов
        self.initialize_squares()

        # Инициализация Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Square Collision Simulation with Rotation")
        self.clock = pygame.time.Clock()

    def initialize_squares(self):
        predefined_squares = [
            {"x": 100, "y": 100, "vx": 2, "vy": 3, "size": 40, "mass": 1, "color": (255, 0, 0)},
            {"x": 300, "y": 200, "vx": -3, "vy": 2, "size": 50, "mass": 2, "color": (0, 255, 0)},
            {"x": 500, "y": 400, "vx": 1, "vy": -2, "size": 30, "mass": 1.5, "color": (0, 0, 255)}
        ]

        for square_data in predefined_squares:
            square = Square(
                x=square_data["x"],
                y=square_data["y"],
                vx=square_data["vx"],
                vy=square_data["vy"],
                size=square_data["size"],
                mass=square_data["mass"],
                color=square_data["color"]
            )
            self.squares.append(square)

    def update(self):
        for square in self.squares:
            square.move()
            square.check_collision_with_walls(self.width, self.height)

        for i, square1 in enumerate(self.squares):
            for square2 in self.squares[i + 1:]:
                square1.check_collision_with_square(square2)

    def render(self):
        self.screen.fill((0, 0, 0))  # Очистка экрана

        for square in self.squares:
            square.render(self.screen)

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

# --- Точка входа ---
if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()
