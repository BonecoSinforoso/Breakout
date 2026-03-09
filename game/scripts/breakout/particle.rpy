init python:

    class Particle:

        def __init__(self, x, y, dx, dy, lifetime, color):
            self.x = x
            self.y = y
            self.dx = dx
            self.dy = dy
            self.lifetime = lifetime
            self.max_lifetime = lifetime
            self.color = color
