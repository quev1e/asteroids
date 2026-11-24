"""Симуляция столкновения шаров"""

# pylint: disable=no-member
# pylint: disable=import-error

import pygame
import pygame_gui

from quadtree import QuadTree
from physics import (
    generate_balls,
    intersects,
    resolve_ball_collision,
    resolve_wall_collision
)


def draw_tree(node, tree_surface):
    """
    Рекурсивно рисует границы всех узлов
    квадродерева на полупрозрачной поверхности
    """
    left, right, top, bottom = node.bounds

    pygame.draw.rect(
        tree_surface,
        (255, 161, 219, 90),
        (
            left,
            bottom,
            right - left,
            top - bottom
        ),
        1
    )

    if node.children[0] is not None:
        for child in node.children:
            draw_tree(child, tree_surface)


def build_world(config):
    """
    Создаёт квадродерево и список
    шаров по параметрам симуляции
    """
    width, height = config["area_sizes"]

    tree = QuadTree((0, width, height, 0), 4)

    balls = generate_balls(
        config["count"],
        config["ball_rs"],
        config["velicity"],
        config["area_sizes"]
    )

    return tree, balls, width, height


def run_simulation(
    config,
    screen,
    manager,
    clock,
    read_settings,
    error_label,
    control_buttons,
    colors,
    sim_size,
    show_start_button
):
    """Запускает и ведёт главный цикл симуляции шаров"""
    background_color, simulation_background_color, panel_color, border_color = colors
    sim_width, sim_height = sim_size

    start_button, restart_button, stop_button = control_buttons

    start_button.hide()
    restart_button.show()
    stop_button.show()

    simulation_running = True

    try:
        tree, balls, width, height = build_world(config)
    except ValueError as error:
        error_label.set_text(str(error))
        show_start_button()
        return True

    while simulation_running:
        dt = clock.tick(60) / 1000

        for current_event in pygame.event.get():
            if current_event.type == pygame.QUIT:
                return False

            manager.process_events(current_event)

            if current_event.type == pygame_gui.UI_BUTTON_PRESSED:
                if current_event.ui_element == stop_button:
                    simulation_running = False
                    break

                elif current_event.ui_element == restart_button:
                    try:
                        config = read_settings()
                        tree, balls, width, height = build_world(config)
                        error_label.set_text("")
                    except ValueError as error:
                        error_label.set_text(str(error))

        manager.update(dt)

        tree.clear()

        r_max = 0

        for ball in balls:
            tree.insert(ball)
            r_max = max(r_max, ball.r)

        for ball in balls:
            query = tree.get_query(
                ball.x,
                ball.y,
                ball.r + r_max
            )

            for other_ball in query:
                if (
                    ball is not other_ball
                    and other_ball.id > ball.id
                    and intersects(ball, other_ball)
                ):
                    resolve_ball_collision(ball, other_ball)

        for ball in balls:
            resolve_wall_collision(ball, width, height)
            ball.update(dt)

        screen.fill(background_color)

        pygame.draw.rect(
            screen,
            panel_color,
            (sim_width, 0, screen.get_width() - sim_width, sim_height)
        )

        pygame.draw.line(
            screen,
            border_color,
            (sim_width, 0),
            (sim_width, sim_height)
        )

        pygame.draw.rect(
            screen,
            simulation_background_color,
            (0, 0, width, height)
        )

        pygame.draw.rect(
            screen,
            border_color,
            (0, 0, width, height),
            1
        )

        tree_surface = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )

        draw_tree(tree.root, tree_surface)

        screen.blit(tree_surface, (0, 0))

        for ball in balls:
            pygame.draw.circle(
                screen,
                ball.color,
                (int(ball.x), int(ball.y)),
                int(ball.r)
            )

            pygame.draw.circle(
                screen,
                (0, 0, 0),
                (int(ball.x), int(ball.y)),
                int(ball.r),
                1
            )

        manager.draw_ui(screen)

        pygame.display.update()

    show_start_button()

    tree.clear()
    balls.clear()

    return True