init python:

    import math
    import random

    class PowerUpExtraBall:

        WIDTH = 32
        HEIGHT = 32
        SPEED = 150
        FPS = 6
        
        SPRITES = [
            "images/powerups/powerup_extra_ball_00.png",
            "images/powerups/powerup_extra_ball_01.png",
            "images/powerups/powerup_extra_ball_02.png",
            "images/powerups/powerup_extra_ball_03.png",
            "images/powerups/powerup_extra_ball_04.png",
            "images/powerups/powerup_extra_ball_05.png"
        ]

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.frames = [Image(p) for p in self.SPRITES]

        def update(self, delta_time):
            self.y += self.SPEED * delta_time

        def render(self, r, width, height, st, at):
            frame_index = int(st * self.FPS) % len(self.frames)
            surf = self.frames[frame_index]
            rendered = renpy.render(surf, self.WIDTH, self.HEIGHT, st, at)
            r.blit(rendered, (int(self.x - self.WIDTH / 2), int(self.y - self.HEIGHT / 2)))

        def apply_effect(self, game):
            angle = random.uniform(-0.785, 0.785)
            new_dx = math.sin(angle) * 0.707
            new_dy = -math.cos(angle) * 0.707

            game.balls_manager.spawn_ball(
                game.paddle.x, 
                PADDLE_Y - 20, 
                new_dx, 
                new_dy,
                stuck=False
            )
