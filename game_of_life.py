#!/usr/bin/env python3
"""Conway's Game of Life.

Implementacja Gry w Życie Conwaya w Pythonie z użyciem Pygame i NumPy.
"""

import numpy as np
import pygame

# Stałe
WIDTH: int = 800
HEIGHT: int = 600
BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)
GREEN: tuple[int, int, int] = (0, 200, 0)
CELL_SIZE: int = 10
GRID_WIDTH: int = WIDTH // CELL_SIZE
GRID_HEIGHT: int = HEIGHT // CELL_SIZE
FPS: int = 10


def create_random_grid() -> np.ndarray:
    """Tworzy losową siatkę złożoną z 0 i 1."""
    rng = np.random.default_rng()
    return rng.integers(
        0,
        2,
        size=(GRID_HEIGHT, GRID_WIDTH),
        dtype=np.int8,
    )


def create_empty_grid() -> np.ndarray:
    """Tworzy pustą siatkę złożoną z 0."""
    return np.zeros(
        (GRID_HEIGHT, GRID_WIDTH),
        dtype=np.int8,
    )


def get_next_generation(grid: np.ndarray) -> np.ndarray:
    """Oblicza następne pokolenie Gry w Życie."""
    new_grid: np.ndarray = np.copy(grid)
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            # Użyj max i min do obliczenia granic sąsiedztwa
            r_start = max(0, r - 1)
            r_end = min(GRID_HEIGHT, r + 2)
            c_start = max(0, c - 1)
            c_end = min(GRID_WIDTH, c + 2)

            # Policz żywych sąsiadów
            live_neighbors = (
                np.sum(grid[r_start:r_end, c_start:c_end]) - grid[r, c]
            )

            # Zastosuj reguły Gry w Życie
            if grid[r, c] == 1:  # Komórka żywa
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[r, c] = 0  # Umiera
            elif live_neighbors == 3:
                new_grid[r, c] = 1  # Ożywa
    return new_grid


def draw_grid(screen: pygame.Surface, grid: np.ndarray) -> None:
    """Rysuje siatkę na ekranie Pygame."""
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            color: tuple[int, int, int] = GREEN if grid[r, c] == 1 else BLACK
            pygame.draw.rect(
                screen,
                color,
                (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )


def game_event_loop() -> None:
    """Obsługuje główną pętlę gry, w tym zdarzenia, aktualizacje i rysowanie."""
    paused: bool = True
    running: bool = True
    clock: pygame.time.Clock = pygame.time.Clock()
    current_grid: np.ndarray = create_random_grid()
    fps = FPS
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_r:
                    current_grid = create_random_grid()
                    paused = True
                if event.key == pygame.K_c:
                    current_grid = create_empty_grid()
                    paused = True
                if event.key == pygame.K_UP:
                    fps = min(fps + 1, 60)
                if event.key == pygame.K_DOWN:
                    fps = max(fps - 1, 1)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                col: int = x // CELL_SIZE
                row: int = y // CELL_SIZE
                if 0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH:
                    current_grid[row, col] = 1 - current_grid[row, col]

        if not paused:
            current_grid = get_next_generation(current_grid)

        screen.fill(BLACK)
        draw_grid(screen, current_grid)
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


def main() -> None:
    """Główna funkcja uruchamiająca Grę w Życie."""
    pygame.init()
    pygame.display.set_caption("Conway's Game of Life")
    game_event_loop()


if __name__ == "__main__":
    main()
