init python:

    class PowerUpSlowDown:
        
        WIDTH = 32
        HEIGHT = 32
        SPEED = 150
        FPS = 6
        
        SPRITES = [
            "images/powerups/power_up_slow_down_00.png",
            "images/powerups/power_up_slow_down_01.png",
            "images/powerups/power_up_slow_down_02.png",
            "images/powerups/power_up_slow_down_03.png",
            "images/powerups/power_up_slow_down_04.png",
            "images/powerups/power_up_slow_down_05.png"
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
            game.balls_manager.timer_slow_down = 10.0
