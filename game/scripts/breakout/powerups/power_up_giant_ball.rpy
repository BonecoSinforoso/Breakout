init python:

    class PowerUpGiantBall:

        WIDTH = 32
        HEIGHT = 32
        SPEED = 150
        FPS = 6
        
        SPRITES = [
            "images/powerups/power_up_giant_ball_00.png",
            "images/powerups/power_up_giant_ball_01.png",
            "images/powerups/power_up_giant_ball_02.png",
            "images/powerups/power_up_giant_ball_03.png",
            "images/powerups/power_up_giant_ball_04.png",
            "images/powerups/power_up_giant_ball_05.png"
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
            game.timer_giant_ball = 10.0