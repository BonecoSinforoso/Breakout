init python:

    import math

    class Ball:

        def __init__(self, x, y, dx, dy, speed, stuck=False):            
            self.x = x
            self.y = y
            self.dx = dx
            self.dy = dy
            self.speed = speed
            self.stuck = stuck
