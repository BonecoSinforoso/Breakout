# gerenciador de particulas
init 1 python:

    import random
    import math
    
    class ParticlesManager:
        
        def __init__(self) -> None:
            self.particles = []
            
            self.colors_neon = ["#FF3333", "#33FF33", "#3333FF", "#FFFF33", "#FF33FF", "#00FFFF"]
            self.solid_cache = {color: Solid(color) for color in self.colors_neon}

        def spawn_burst(self, x: float, y: float, amount: int = 10, color: str = None, speed_min: float = 50.0, speed_max: float = 200.0) -> None:
            for _ in range(amount):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(speed_min, speed_max)
                
                dx = math.cos(angle) * speed
                dy = math.sin(angle) * speed
                lifetime = random.uniform(0.2, 0.5)
                
                particle_color = color if color is not None else random.choice(self.colors_neon)
                
                if particle_color not in self.solid_cache:
                    self.solid_cache[particle_color] = Solid(particle_color)
                
                self.particles.append(Particle(x, y, dx, dy, lifetime, particle_color))

        def update_and_render(self, r, width: int, height: int, st: float, at: float, delta_time: float) -> None:
            for particle in self.particles[:]:
                particle.x += particle.dx * delta_time
                particle.y += particle.dy * delta_time
                particle.lifetime -= delta_time

                if particle.lifetime <= 0:
                    self.particles.remove(particle)
                else:
                    max_life = getattr(particle, 'max_lifetime', 0.5) 
                    size = max(1, int(6 * (particle.lifetime / max_life)))
                    
                    solid = self.solid_cache[particle.color]
                    p_rend = renpy.render(solid, size, size, st, at)
                    r.blit(p_rend, (int(particle.x - size/2), int(particle.y - size/2)))
