init python:

    import random
    import math
    
    class ParticlesManager:
        
        def __init__(self):
            self.particles = []

        def spawn_burst(self, x, y, amount=10, color=None, speed_min=50, speed_max=200):
            colors_neon = ["#FF3333", "#33FF33", "#3333FF", "#FFFF33", "#FF33FF", "#00FFFF"]

            for _ in range(amount):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(speed_min, speed_max)
                
                dx = math.cos(angle) * speed
                dy = math.sin(angle) * speed
                lifetime = random.uniform(0.2, 0.5)
                
                p_color = color if color is not None else random.choice(colors_neon)
                
                self.particles.append(Particle(x, y, dx, dy, lifetime, p_color))

        def update_and_render(self, r, delta_time):
            canvas = r.canvas()
            
            for p in self.particles[:]:
                particle.x += particle.dx * delta_time
                particle.y += particle.dy * delta_time
                particle.lifetime -= delta_time

                if particle.lifetime <= 0:
                    self.particles.remove(p)
                else:
                    size = max(1, int(6 * (particle.lifetime / particle.max_lifetime)))
                    canvas.rect(particle.color, (int(particle.x - size/2), int(particle.y - size/2), size, size))
