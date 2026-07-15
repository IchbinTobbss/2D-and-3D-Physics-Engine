import subprocess
import sys
import importlib

packages = {
    "arcade": "arcade",
    "pymunk" : "pymunk"
}

for module, package in packages.items():
    try:
        importlib.import_module(module)
        print(f"✓ {package} ist installiert.")
    except ImportError:
        print(f"Installiere {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print("Dependencies are installed")




import arcade
import pymunk
import random
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

GRID = 32
BALL_RADIUS = 10

GRAVITY = (0, -900)

BLOCK_NORMAL = 1
BLOCK_SPAWNER = 2
BLOCK_REMOVER = 3


class Sandbox(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sandbox")

        arcade.set_background_color((18, 18, 24))

        self.space = pymunk.Space()
        self.space.gravity = GRAVITY
        self.space.damping = 0.995

        self.blocks = {}
        self.balls = []
        self.ball_grid = {}

        self.mx = 0
        self.my = 0

        self.space_held = False
        self.spawn_timer = 0

        self.selected_block = BLOCK_NORMAL

        self.frozen = False
        self.magnet_enabled = False

        self.create_walls()

    # ---------------- WALLS ----------------
    def create_walls(self):
        static = self.space.static_body

        walls = [
            pymunk.Segment(static, (0, 0), (SCREEN_WIDTH, 0), 3),
            pymunk.Segment(static, (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), 3),
            pymunk.Segment(static, (0, 0), (0, SCREEN_HEIGHT), 3),
            pymunk.Segment(static, (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), 3),
        ]

        for w in walls:
            w.friction = 1.0
            w.elasticity = 0.1

        self.space.add(*walls)

    # ---------------- HELPERS ----------------
    def cell(self, x, y):
        return int(x // GRID), int(y // GRID)

    # ---------------- BLOCKS ----------------
    def add_block(self, x, y):
        gx, gy = self.cell(x, y)

        if (gx, gy) in self.blocks:
            return

        px = gx * GRID + GRID / 2
        py = gy * GRID + GRID / 2

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (px, py)

        shape = pymunk.Poly.create_box(body, (GRID, GRID))
        shape.friction = 1.0
        shape.elasticity = 0.05

        self.space.add(body, shape)

        self.blocks[(gx, gy)] = {
            "body": body,
            "shape": shape,
            "type": self.selected_block
        }

    def remove_block(self, x, y):
        gx, gy = self.cell(x, y)

        if (gx, gy) not in self.blocks:
            return

        b = self.blocks[(gx, gy)]
        self.space.remove(b["body"], b["shape"])
        del self.blocks[(gx, gy)]

    # ---------------- BALLS ----------------
    def spawn_ball(self, x, y):

        gx, gy = self.cell(x, y)

        if (gx, gy) in self.blocks:
            return

        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, BALL_RADIUS)

        body = pymunk.Body(mass, moment)
        body.position = (x, y)

        shape = pymunk.Circle(body, BALL_RADIUS)
        shape.friction = 0.8
        shape.elasticity = 0.1

        self.space.add(body, shape)
        self.balls.append(body)

    # ---------------- FULL CLEAR (FIXED C KEY) ----------------
    def clear_all_balls(self):

        for ball in self.balls:

            try:
                self.space.remove(ball, *ball.shapes)
            except:
                pass

        self.balls.clear()
        self.ball_grid.clear()

    # ---------------- UPDATE ----------------
    def on_update(self, dt):

        if not self.frozen:
            for _ in range(2):
                self.space.step(1 / 120)

        # spawn hold
        if self.space_held:
            self.spawn_timer += dt
            while self.spawn_timer > 0.03:
                self.spawn_ball(self.mx, self.my)
                self.spawn_timer -= 0.03
        else:
            self.spawn_timer = 0

        # rebuild grid
        self.ball_grid.clear()
        for ball in self.balls:
            c = self.cell(ball.position.x, ball.position.y)
            self.ball_grid.setdefault(c, []).append(ball)

        # block logic
        for (gx, gy), b in list(self.blocks.items()):

            cx = gx * GRID + GRID / 2
            cy = gy * GRID + GRID / 2

            if b["type"] == BLOCK_SPAWNER:
                for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx, ny = gx + dx, gy + dy
                    if (nx, ny) not in self.blocks:
                        self.spawn_ball(nx * GRID + GRID/2, ny * GRID + GRID/2)
                        break

            elif b["type"] == BLOCK_REMOVER:

                to_delete = []

                for balls in self.ball_grid.values():
                    for ball in balls:

                        dx = ball.position.x - cx
                        dy = ball.position.y - cy

                        if self.magnet_enabled and dx*dx + dy*dy < 200*200:
                            dist = math.sqrt(dx*dx + dy*dy) + 0.001
                            force = 18000 / (dx*dx + dy*dy + 1)

                            ball.apply_force_at_world_point(
                                (dx/dist * force, dy/dist * force),
                                ball.position
                            )

                        if abs(dx) < GRID/2 and abs(dy) < GRID/2:
                            to_delete.append(ball)

                for ball in to_delete:
                    if ball in self.balls:
                        self.space.remove(ball, *ball.shapes)
                        self.balls.remove(ball)

        # delete balls inside blocks
        for ball in self.balls[:]:

            gx, gy = self.cell(ball.position.x, ball.position.y)

            if (gx, gy) in self.blocks:
                self.space.remove(ball, *ball.shapes)
                self.balls.remove(ball)

        for ball in self.blocks.values():
            if ball["type"] == BLOCK_REMOVER:
                self.space.remove(ball["body"], ball["shape"])
                del self.blocks[(gx, gy)]

    # ---------------- DRAW ----------------
    def on_draw(self):
        self.clear()

        for (gx, gy), b in self.blocks.items():

            x = gx * GRID + GRID / 2
            y = gy * GRID + GRID / 2

            color = (80, 80, 90)

            if b["type"] == BLOCK_SPAWNER:
                color = (80, 200, 80)

            if b["type"] == BLOCK_REMOVER:
                color = (220, 80, 80)

            arcade.draw_rect_filled(
                arcade.XYWH(x, y, GRID, GRID),
                color
            )

        for ball in self.balls:
            arcade.draw_circle_filled(
                ball.position.x,
                ball.position.y,
                BALL_RADIUS,
                (120, 200, 255)
            )

    # ---------------- INPUT ----------------
    def on_mouse_press(self, x, y, button, modifiers):

        if button == arcade.MOUSE_BUTTON_LEFT:
            self.add_block(x, y)

        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.remove_block(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):

        if buttons & arcade.MOUSE_BUTTON_LEFT:
            self.add_block(x, y)

        if buttons & arcade.MOUSE_BUTTON_RIGHT:
            self.remove_block(x, y)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mx = x
        self.my = y

    def on_key_press(self, key, modifiers):

        if key == arcade.key.SPACE:
            self.space_held = True

        if key == arcade.key.C:
            self.clear_all_balls()

        if key == arcade.key.R:
            self.frozen = not self.frozen

        if key == arcade.key.M:
            self.magnet_enabled = not self.magnet_enabled

        if key == arcade.key.KEY_1:
            self.selected_block = BLOCK_NORMAL

        if key == arcade.key.KEY_2:
            self.selected_block = BLOCK_SPAWNER

        if key == arcade.key.KEY_3:
            self.selected_block = BLOCK_REMOVER

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.space_held = False


Sandbox()
arcade.run()