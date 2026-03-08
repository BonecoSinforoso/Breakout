init python:

    class Paddle:

        def __init__(self, x):
            
            self.x = x
            self.y = PADDLE_Y
                        
            self.default_width = 64
            self.default_image = Image("images/paddles/paddle_red_02.png")
            self.height = PADDLE_HEIGHT
                        
            self.width = self.default_width
            self.image = self.default_image
                        
            self.timer_increase_size = 0.0

        def update(self, delta_time):
            if self.timer_increase_size > 0:
                self.timer_increase_size -= delta_time

                if self.timer_increase_size <= 0:
                    self.timer_increase_size = 0
                    self.width = self.default_width
                    self.image = self.default_image

        def reset_effects(self):
            self.timer_increase_size = 0
            self.width = self.default_width
            self.image = self.default_image

        def render(self, r, width, height, st, at):
            pi = renpy.render(self.image, width, height, st, at)
            r.blit(pi, (int(self.x - self.width / 2), int(self.y - self.height / 2)))
