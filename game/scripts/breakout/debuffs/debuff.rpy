init 1 python:

    class Debuff:
        
        WIDTH = 96
        HEIGHT = 96
        
        SPRITES = []
        FPS = 8

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.dy = 150 # Velocidade de queda 
            self.dx_speed = 120 # Velocidade de perseguição 
            
            self.frames = [Transform(Image(p), size=(self.WIDTH, self.HEIGHT)) for p in self.SPRITES]

        def update(self, delta_time, target_x):
            self.y += self.dy * delta_time

            if self.x < target_x - 20:
                self.x += self.dx_speed * delta_time
            elif self.x > target_x + 20:
                self.x -= self.dx_speed * delta_time

        def render(self, r, width, height, st, at):
            pass

        def apply_effect(self, game):
            pass
