init python:

    import random
    import math
    
    class ParticlesManager:
        
        def __init__(self):
            self.particles = []

        def spawn_burst(self, x, y, amount=10, color="#FFFFFF", speed_min=50, speed_max=200):
            for _ in range(amount):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(speed_min, speed_max)
                
                dx = math.cos(angle) * speed
                dy = math.sin(angle) * speed
                lifetime = random.uniform(0.2, 0.5) # Dura entre 0.2 e 0.5 segundos
                
                self.particles.append(Particle(x, y, dx, dy, lifetime, color))

        def update_and_render(self, r, delta_time):
            canvas = r.canvas()
            
            for p in self.particles[:]:
                p.x += p.dx * delta_time
                p.y += p.dy * delta_time
                p.lifetime -= delta_time

                if p.lifetime <= 0:
                    self.particles.remove(p)
                else:
                    size = max(1, int(6 * (p.lifetime / p.max_lifetime)))
                    canvas.rect(p.color, (int(p.x - size/2), int(p.y - size/2), size, size))
