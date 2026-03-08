# responsavel por controlar cd e spawn dos projeteis
init python:

    import pygame

    class Arsenal:

        def __init__(self):
            self.ammo_basic = 0
            self.ammo_piercing = 0
            self.cd_basic = 0.0
            self.cd_piercing = 0.0

        def update(self, delta_time):
            if self.cd_basic > 0: self.cd_basic -= delta_time
            if self.cd_piercing > 0: self.cd_piercing -= delta_time

        def handle_input(self, ev, game):
            if game.stuck or game.winner:
                return

            if ev.type == pygame.KEYDOWN:
                # Z: projetil basico
                if ev.key == pygame.K_z:
                    if self.ammo_basic > 0 and self.cd_basic <= 0:
                        self.ammo_basic -= 1
                        self.cd_basic = 0.3
                        
                        renpy.sound.play("projectile_basic.wav", channel=3)
                        
                        frames = ["images/projectiles/projectile_basic_{:02d}.png".format(i) for i in range(4)]
                        game.projectiles.append(Projectile(game.paddle.x, PADDLE_Y - PADDLE_HEIGHT, 500, False, frames))

                # X: projetil perfurante
                elif ev.key == pygame.K_x:
                    if self.ammo_piercing > 0 and self.cd_piercing <= 0:
                        self.ammo_piercing -= 1
                        self.cd_piercing = 0.6

                        renpy.sound.play("projectile_piercing.wav", channel=3)
                        
                        frames = ["images/projectiles/projectile_piercing_{:02d}.png".format(i) for i in range(4)]
                        game.projectiles.append(Projectile(game.paddle.x, PADDLE_Y - PADDLE_HEIGHT, 600, True, frames))
