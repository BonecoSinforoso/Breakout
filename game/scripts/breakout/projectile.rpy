init python:

    class Projectile:
    
        def __init__(self, x, y, speed, is_piercing, image_path):
            self.x = x
            self.y = y
            self.speed = speed
            self.is_piercing = is_piercing
            self.image = Image(image_path)
                        
            self.width = 16
            self.height = 16

        def update(self, delta_time):
            self.y -= self.speed * delta_time

        def render(self, r, width, height, st, at):
            img = renpy.render(self.image, width, height, st, at)
            r.blit(img, (int(self.x - self.width / 2), int(self.y - self.height / 2)))
