"""Отрисовка интерфейса"""
# pylint: disable=no-member
# pylint: disable=import-error

import pygame
import pygame_gui
from simulation import run_simulation


pygame.init()

info = pygame.display.Info()

WINDOW_WIDTH = int(info.current_w * 0.75)
WINDOW_HEIGHT = int(info.current_h * 0.8)

SIMULATION_WIDTH = int(WINDOW_WIDTH * 0.7)
SIMULATION_HEIGHT = WINDOW_HEIGHT

PANEL_WIDTH = WINDOW_WIDTH - SIMULATION_WIDTH
PANEL_X = SIMULATION_WIDTH


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("Астероиды")

clock = pygame.time.Clock()
manager = pygame_gui.UIManager(
    (WINDOW_WIDTH, WINDOW_HEIGHT),
    "theme.json"
)

running = True

background_color = (12, 10, 16)
simulation_background_color = (22, 18, 27)
panel_color = (29, 23, 35)
border_color = (190, 65, 135)

panel_rect = pygame.Rect(
    SIMULATION_WIDTH,
    0,
    PANEL_WIDTH,
    WINDOW_HEIGHT
)

title = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(PANEL_X + 25, 10, 280, 35),
    text="Настройки симуляции",
    manager=manager
)

count_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(PANEL_X + 25, 50, 280, 25),
    text="Количество шаров",
    manager=manager
)

count_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(PANEL_X + 25, 75, 280, 30),
    initial_text="50",
    manager=manager
)

radius_min_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(PANEL_X + 25, 110, 280, 25),
    text="Минимальный радиус",
    manager=manager
)

radius_min_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(PANEL_X + 25, 135, 280, 30),
    initial_text="2",
    manager=manager
)

radius_max_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(PANEL_X + 25, 170, 280, 25),
    text="Максимальный радиус",
    manager=manager
)

radius_max_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(PANEL_X + 25, 195, 280, 30),
    initial_text="6",
    manager=manager
)

width_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(PANEL_X + 25, 230, 280, 25),
    text="Ширина области",
    manager=manager
)

width_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(PANEL_X + 25, 255, 280, 30),
    initial_text="806",
    manager=manager
)

height_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(PANEL_X + 25, 290, 280, 25),
    text="Высота области",
    manager=manager
)

height_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(PANEL_X + 25, 315, 280, 30),
    initial_text="691",
    manager=manager
)

velocity_min_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(PANEL_X + 25, 350, 280, 25),
    text="Минимальная скорость",
    manager=manager
)

velocity_min_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(PANEL_X + 25, 375, 280, 30),
    initial_text="150",
    manager=manager
)

velocity_max_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(PANEL_X + 25, 410, 280, 25),
    text="Максимальная скорость",
    manager=manager
)

velocity_max_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(PANEL_X + 25, 435, 280, 30),
    initial_text="500",
    manager=manager
)

start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(PANEL_X + 25, 480, 280, 40),
    text="Старт",
    manager=manager
)

restart_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(PANEL_X + 25, 480, 280, 40),
    text="Перезапуск с новыми параметрами",
    manager=manager
)

stop_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(PANEL_X + 25, 530, 280, 40),
    text="Стоп",
    manager=manager
)

restart_button.hide()
stop_button.hide()

error_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(PANEL_X + 25, 575, 280, 30),
    text="",
    manager=manager
)


def show_start_button():
    """
    Возвращает интерфейс в начальное состояние
    """
    start_button.show()
    restart_button.hide()
    stop_button.hide()


def show_running_buttons():
    """
    Переводит интерфейс в состояние 
    запущенной симуляции
    """
    start_button.hide()
    restart_button.show()
    stop_button.show()


def read_number(element, name, minimum=None, maximum=None):
    """
    Считывает число из текстового поля
    и проверяет его корректность
    """
    text = element.get_text().strip()

    try:
        value = float(text)
    except ValueError:
        raise ValueError(f"{name}: введите число")

    if minimum is not None and value < minimum:
        raise ValueError(f"{name}: не меньше {minimum}")

    if maximum is not None and value > maximum:
        raise ValueError(f"{name}: не больше {maximum}")

    return value


def read_settings():
    """
    Считывает и проверяет все
    параметры симуляции из полей ввода
    """
    count = int(
        read_number(
            count_input,
            "Количество шаров",
            1,
            2000
        )
    )

    radius_min = read_number(
        radius_min_input,
        "Минимальный радиус",
        1
    )

    radius_max = read_number(
        radius_max_input,
        "Максимальный радиус",
        1
    )

    area_width = read_number(
        width_input,
        "Ширина области",
        100,
        SIMULATION_WIDTH
    )

    area_height = read_number(
        height_input,
        "Высота области",
        100,
        SIMULATION_HEIGHT
    )

    velocity_min = read_number(
        velocity_min_input,
        "Минимальная скорость",
        0
    )

    velocity_max = read_number(
        velocity_max_input,
        "Максимальная скорость",
        0
    )

    if radius_min > radius_max:
        raise ValueError(
            "Минимальный радиус не может быть больше максимального"
        )

    if velocity_min > velocity_max:
        raise ValueError(
            "Минимальная скорость не может быть больше максимальной"
        )

    if 2 * radius_max > min(area_width, area_height):
        raise ValueError(
            "Шары слишком велики для выбранной области"
        )

    return {
        "count": count,
        "ball_rs": (radius_min, radius_max),
        "velicity": (velocity_min, velocity_max),
        "area_sizes": (area_width, area_height)
    }


def start_simulation():
    """
    Запускает симуляцию с параметрами
    из панели настроек
    """
    global running

    try:
        settings = read_settings()
    except ValueError as error:
        error_label.set_text(str(error))
        return True

    error_label.set_text("")

    show_running_buttons()

    result = run_simulation(
        config=settings,
        screen=screen,
        manager=manager,
        clock=clock,
        read_settings=read_settings,
        error_label=error_label,
        control_buttons=(
            start_button,
            restart_button,
            stop_button
        ),
        colors=(
            background_color,
            simulation_background_color,
            panel_color,
            border_color
        ),
        sim_size=(SIMULATION_WIDTH, SIMULATION_HEIGHT),
        show_start_button=show_start_button
    )

    try:
        settings = read_settings()
    except ValueError as error:
        print(error)
        error_label.set_text(str(error))
        return True

    show_start_button()

    return result


while running:
    dt = clock.tick(60) / 1000

    for current_event in pygame.event.get():
        if current_event.type == pygame.QUIT:
            running = False

        manager.process_events(current_event)

        if current_event.type == pygame_gui.UI_BUTTON_PRESSED:
            if current_event.ui_element in (
                start_button,
                restart_button
            ):
                running = start_simulation()

    manager.update(dt)

    screen.fill(background_color)

    pygame.draw.rect(
        screen,
        simulation_background_color,
        (0, 0, SIMULATION_WIDTH, SIMULATION_HEIGHT)
    )

    pygame.draw.rect(
        screen,
        border_color,
        (0, 0, SIMULATION_WIDTH, SIMULATION_HEIGHT),
        1
    )

    pygame.draw.rect(
        screen,
        panel_color,
        panel_rect
    )

    manager.draw_ui(screen)

    pygame.display.update()


pygame.quit()
