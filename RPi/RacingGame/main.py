import math
import sys

import pygame


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
LAPS_TO_WIN = 3
TRACK_CENTER = (1000.0, 800.0)
TRACK_RADII = (720.0, 420.0)
ROAD_INNER = 0.84
ROAD_OUTER = 1.16

CONTROLS = (
    {
        "left": pygame.K_a,
        "right": pygame.K_d,
        "accelerate": pygame.K_w,
        "brake": pygame.K_s,
        "boost": pygame.K_LSHIFT,
        "drift": pygame.K_SPACE,
        "item": pygame.K_e,
        "horn": pygame.K_q,
        "reset": pygame.K_r,
    },
    {
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "accelerate": pygame.K_UP,
        "brake": pygame.K_DOWN,
        "boost": pygame.K_RSHIFT,
        "drift": pygame.K_RALT,
        "item": pygame.K_RCTRL,
        "horn": pygame.K_RIGHTBRACKET,
        "reset": pygame.K_BACKSPACE,
    },
)

PLAYER_COLORS = ((66, 190, 255), (255, 105, 78))
PICKUP_ANGLES = (math.pi / 2, math.pi, math.pi * 1.5)


def track_position(angle, lane=0.0):
    radius_x = TRACK_RADII[0] * (1 + lane)
    radius_y = TRACK_RADII[1] * (1 + lane)
    return (
        TRACK_CENTER[0] + math.cos(angle) * radius_x,
        TRACK_CENTER[1] + math.sin(angle) * radius_y,
    )


def track_radius(position):
    x = (position[0] - TRACK_CENTER[0]) / TRACK_RADII[0]
    y = (position[1] - TRACK_CENTER[1]) / TRACK_RADII[1]
    return math.sqrt(x * x + y * y)


class Player:
    def __init__(self, number, lane):
        self.number = number
        self.controls = CONTROLS[number - 1]
        self.color = PLAYER_COLORS[number - 1]
        self.lane = lane
        self.reset()

    def reset(self):
        start_angle = 0.14
        self.x, self.y = track_position(start_angle, self.lane)
        self.angle = start_angle + math.pi / 2
        self.previous_track_angle = start_angle
        self.speed = 0.0
        self.laps = 0
        self.boost_time = 0.0
        self.boost_cooldown = 0.0
        self.has_item = False
        self.boost_was_pressed = False
        self.item_was_pressed = False
        self.horn_was_pressed = False
        self.horn_time = 0.0

    def update(self, keys, dt, pickups):
        controls = self.controls
        accelerating = keys[controls["accelerate"]]
        braking = keys[controls["brake"]]
        drifting = keys[controls["drift"]]
        boost_pressed = keys[controls["boost"]]
        item_pressed = keys[controls["item"]]
        horn_pressed = keys[controls["horn"]]

        if boost_pressed and not self.boost_was_pressed and self.boost_cooldown <= 0:
            self.boost_time = 0.9
            self.boost_cooldown = 2.5
        if item_pressed and not self.item_was_pressed and self.has_item:
            self.has_item = False
            self.boost_time = 1.4
        if horn_pressed and not self.horn_was_pressed:
            self.horn_time = 0.3
        self.boost_was_pressed = boost_pressed
        self.item_was_pressed = item_pressed
        self.horn_was_pressed = horn_pressed

        self.boost_time = max(0.0, self.boost_time - dt)
        self.boost_cooldown = max(0.0, self.boost_cooldown - dt)
        self.horn_time = max(0.0, self.horn_time - dt)

        on_road = ROAD_INNER <= track_radius((self.x, self.y)) <= ROAD_OUTER
        maximum_speed = 540.0 if self.boost_time > 0 else 420.0
        acceleration = 390.0 if on_road else 190.0

        if accelerating:
            self.speed += acceleration * dt
        elif braking:
            self.speed -= 520.0 * dt
        else:
            self.speed -= math.copysign(min(abs(self.speed), 48.0 * dt), self.speed)

        if not on_road:
            self.speed -= math.copysign(min(abs(self.speed), 180.0 * dt), self.speed)
        self.speed = max(-110.0, min(maximum_speed, self.speed))

        steering = int(keys[controls["right"]]) - int(keys[controls["left"]])
        if abs(self.speed) > 4:
            turn_rate = 0.75 + min(abs(self.speed) / 250.0, 1.0)
            if drifting:
                turn_rate *= 1.3
            self.angle += steering * turn_rate * dt * (1 if self.speed >= 0 else -1)

        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt

        current_angle = math.atan2(
            (self.y - TRACK_CENTER[1]) / TRACK_RADII[1],
            (self.x - TRACK_CENTER[0]) / TRACK_RADII[0],
        ) % (math.pi * 2)
        if self.previous_track_angle > math.pi * 1.75 and current_angle < math.pi / 4:
            self.laps += 1
        self.previous_track_angle = current_angle

        for pickup in pickups:
            if pickup["available"]:
                dx = self.x - pickup["position"][0]
                dy = self.y - pickup["position"][1]
                if dx * dx + dy * dy < 52 * 52:
                    self.has_item = True
                    pickup["available"] = False
                    pickup["respawn"] = 6.0


def reset_pickups():
    return [
        {
            "position": track_position(angle),
            "available": True,
            "respawn": 0.0,
        }
        for angle in PICKUP_ANGLES
    ]


def draw_player(view, player, camera, scale, font):
    center_x = view.get_width() // 2
    center_y = view.get_height() // 2
    car_x = center_x + int((player.x - camera[0]) * scale)
    car_y = center_y + int((player.y - camera[1]) * scale)
    car_surface = pygame.Surface((38, 22), pygame.SRCALPHA)
    pygame.draw.rect(car_surface, player.color, (2, 1, 34, 20), border_radius=6)
    pygame.draw.rect(car_surface, (220, 235, 245), (21, 4, 9, 14), border_radius=3)
    pygame.draw.rect(car_surface, (28, 36, 44), (6, 2, 5, 5), border_radius=2)
    pygame.draw.rect(car_surface, (28, 36, 44), (6, 15, 5, 5), border_radius=2)
    rotated = pygame.transform.rotate(car_surface, -math.degrees(player.angle))
    view.blit(rotated, rotated.get_rect(center=(car_x, car_y)))

    label = "P{}  Lap {}/{}  {:3.0f} km/h".format(
        player.number,
        min(player.laps + 1, LAPS_TO_WIN),
        LAPS_TO_WIN,
        abs(player.speed) * 0.28,
    )
    if player.has_item:
        label += "  ITEM"
    elif player.boost_time > 0:
        label += "  BOOST!"
    view.blit(font.render(label, True, (255, 255, 255)), (14, 12))

    if player.horn_time > 0:
        view.blit(font.render("HONK!", True, player.color), (14, 42))


def draw_view(screen, viewport, player, players, pickups, font, small_font):
    view = screen.subsurface(viewport)
    view.fill((49, 125, 55))

    scale = min(view.get_width() / 1450, view.get_height() / 1120)
    center_x = view.get_width() // 2
    center_y = view.get_height() // 2
    camera = (player.x, player.y)

    def ellipse_rect(radius_x, radius_y, factor):
        width = int(radius_x * factor * 2 * scale)
        height = int(radius_y * factor * 2 * scale)
        x = center_x + int((TRACK_CENTER[0] - camera[0]) * scale) - width // 2
        y = center_y + int((TRACK_CENTER[1] - camera[1]) * scale) - height // 2
        return pygame.Rect(x, y, width, height)

    outer = ellipse_rect(*TRACK_RADII, ROAD_OUTER)
    inner = ellipse_rect(*TRACK_RADII, ROAD_INNER)
    pygame.draw.ellipse(view, (36, 39, 43), outer)
    pygame.draw.ellipse(view, (91, 94, 98), outer.inflate(-8, -8))
    pygame.draw.ellipse(view, (49, 125, 55), inner)
    pygame.draw.ellipse(view, (224, 224, 207), outer, max(2, int(3 * scale)))
    pygame.draw.ellipse(view, (224, 224, 207), inner, max(2, int(3 * scale)))

    for index in range(32):
        angle = math.pi * 2 * index / 32
        if index % 2:
            continue
        wx, wy = track_position(angle)
        sx = center_x + int((wx - camera[0]) * scale)
        sy = center_y + int((wy - camera[1]) * scale)
        pygame.draw.circle(view, (184, 187, 184), (sx, sy), max(2, int(4 * scale)))

    start_x = center_x + int((TRACK_CENTER[0] + TRACK_RADII[0] - camera[0]) * scale)
    start_y = center_y + int((TRACK_CENTER[1] - camera[1]) * scale)
    half_line = int(TRACK_RADII[0] * (ROAD_OUTER - ROAD_INNER) * 0.5 * scale)
    pygame.draw.line(view, (255, 255, 255), (start_x - half_line, start_y), (start_x + half_line, start_y), max(2, int(3 * scale)))

    for pickup in pickups:
        if pickup["available"]:
            x = center_x + int((pickup["position"][0] - camera[0]) * scale)
            y = center_y + int((pickup["position"][1] - camera[1]) * scale)
            pygame.draw.circle(view, (30, 30, 30), (x, y), max(7, int(17 * scale)))
            pygame.draw.circle(view, (255, 210, 58), (x, y), max(5, int(13 * scale)))
            pygame.draw.circle(view, (255, 245, 180), (x, y), max(2, int(5 * scale)))

    for other in players:
        draw_player(view, other, camera, scale, font)

    view.blit(small_font.render("A boost   B drift   X item   Y horn", True, (245, 245, 245)), (14, view.get_height() - 28))


def main():
    pygame.init()
    pygame.display.set_caption("Pico Kart - local split-screen")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 26)
    small_font = pygame.font.Font(None, 20)
    players = (Player(1, -0.035), Player(2, 0.035))
    pickups = reset_pickups()
    paused = False
    winner = None
    elapsed = 0.0
    running = True

    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    paused = not paused
                elif event.key in (pygame.K_r, pygame.K_BACKSPACE):
                    for player in players:
                        player.reset()
                    pickups = reset_pickups()
                    winner = None
                    elapsed = 0.0

        keys = pygame.key.get_pressed()
        if not paused and winner is None:
            elapsed += dt
            for pickup in pickups:
                if not pickup["available"]:
                    pickup["respawn"] -= dt
                    if pickup["respawn"] <= 0:
                        pickup["available"] = True
            for player in players:
                player.update(keys, dt, pickups)
                if player.laps >= LAPS_TO_WIN and winner is None:
                    winner = player

        screen.fill((15, 15, 18))
        half_width = screen.get_width() // 2
        for index, player in enumerate(players):
            viewport = pygame.Rect(index * half_width, 0, half_width, screen.get_height())
            draw_view(screen, viewport, player, players, pickups, font, small_font)
        pygame.draw.line(screen, (235, 235, 235), (half_width, 0), (half_width, screen.get_height()), 3)

        if paused or winner is not None:
            text = "PAUSED - Enter or Esc to continue" if paused else "PLAYER {} WINS!  R to race again".format(winner.number)
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 155))
            screen.blit(overlay, (0, 0))
            message = pygame.font.Font(None, 48).render(text, True, (255, 255, 255))
            screen.blit(message, message.get_rect(center=screen.get_rect().center))

        pygame.display.flip()

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
