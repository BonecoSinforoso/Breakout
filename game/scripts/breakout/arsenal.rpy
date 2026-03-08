# TODO: ate q ponto ele nn seria um manager dos projeteis?
init python:

    import pygame

    class Arsenal:

        def __init__(self):
            self.ammo_basic = 0
            self.ammo_piercing = 0
            self.cd_basic = 0.0
            self.cd_piercing = 0.0
            
            self.projectiles = []

        def update_and_render(self, r, width, height, st, at, delta_time, block_grid):
            if self.cd_basic > 0: self.cd_basic -= delta_time
            if self.cd_piercing > 0: self.cd_piercing -= delta_time

            points_earned = 0

            for projectile in self.projectiles[:]:
                projectile.update(delta_time)
                projectile.render(r, width, height, st, at)
                
                if projectile.y < 0:
                    self.projectiles.remove(projectile)
                    continue
                                
                p_left = projectile.x - projectile.width / 2
                p_right = projectile.x + projectile.width / 2
                p_top = projectile.y - projectile.height / 2
                p_bottom = projectile.y + projectile.height / 2

                hit_something = False

                for block in block_grid.blocks:
                    if not block.active: continue
                    
                    b_left, b_top = block.x, block.y
                    b_right, b_bottom = block.x + block.WIDTH, block.y + block.HEIGHT
                    
                    if (p_right >= b_left and p_left <= b_right and 
                        p_bottom >= b_top and p_top <= b_bottom):
                        
                        renpy.sound.play("ball_collision.wav", channel=0)
                        
                        if projectile.is_piercing:
                            while block.active:
                                destroyed, points = block.hit()
                                points_earned += points
                        else:
                            destroyed, points = block.hit()
                            points_earned += points
                            hit_something = True
                            break
                
                if hit_something:
                    self.projectiles.remove(projectile)

            return points_earned

        def handle_input(self, ev, game):
            if game.stuck or game.winner: return

            if ev.type == pygame.KEYDOWN:
                # tiro basico (tecla Z)
                if ev.key == pygame.K_z:
                    if self.ammo_basic > 0 and self.cd_basic <= 0:
                        self.ammo_basic -= 1
                        self.cd_basic = 0.3
                        renpy.sound.play("projectile_basic.wav", channel=3)
                        frames = ["images/projectiles/projectile_basic_{:02d}.png".format(i) for i in range(4)]
                        
                        self.projectiles.append(Projectile(game.paddle.x, PADDLE_Y - PADDLE_HEIGHT, 500, False, frames))

                # tiro perfurante (tecla X)
                elif ev.key == pygame.K_x:
                    if self.ammo_piercing > 0 and self.cd_piercing <= 0:
                        self.ammo_piercing -= 1
                        self.cd_piercing = 0.6
                        renpy.sound.play("projectile_piercing.wav", channel=3)
                        frames = ["images/projectiles/projectile_piercing_{:02d}.png".format(i) for i in range(4)]
                        
                        self.projectiles.append(Projectile(game.paddle.x, PADDLE_Y - PADDLE_HEIGHT, 600, True, frames))
