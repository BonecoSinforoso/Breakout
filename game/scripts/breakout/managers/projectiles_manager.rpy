# gerenciador dos projeteis e municao
init 1 python:

    import pygame

    class ProjectilesManager:

        def __init__(self) -> None:
            self.ammo_basic = 0
            self.ammo_piercing = 0
            self.cd_basic = 0.0
            self.cd_piercing = 0.0
            
            self.projectiles = []

        def update_and_render(self, r, width: int, height: int, st: float, at: float, delta_time: float, blocks_manager) -> int:
            if self.cd_basic > 0: self.cd_basic -= delta_time
            if self.cd_piercing > 0: self.cd_piercing -= delta_time

            points_earned = 0

            for projectile in self.projectiles[:]:
                projectile.update(delta_time)
                projectile.render(r, width, height, st, at)
                
                # saiu da tela por cima
                if projectile.y < 0:
                    self.projectiles.remove(projectile)
                    continue
                                
                hit_something = False

                for block in blocks_manager.blocks:
                    if not block.active: continue
                    
                    block_center_x = block.x + block.WIDTH / 2
                    block_center_y = block.y + block.HEIGHT / 2
                    
                    if Physics.is_aabb_collision(
                        projectile.x, projectile.y, projectile.width, projectile.height,
                        block_center_x, block_center_y, block.WIDTH, block.HEIGHT
                    ):
                        
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

        def handle_input(self, ev, game) -> None:
            if game.stuck or game.winner: return

            if ev.type == pygame.KEYDOWN:
                # tiro basico (tecla Z)
                if ev.key == pygame.K_z:
                    if self.ammo_basic > 0 and self.cd_basic <= 0:
                        self.ammo_basic -= 1
                        self.cd_basic = 0.3
                        renpy.sound.play("projectile_basic.wav", channel=3)
                        
                        new_proj = ProjectilesFactory.create_basic(game.paddle.x, PADDLE_Y - PADDLE_HEIGHT)
                        self.projectiles.append(new_proj)

                # tiro perfurante (tecla X)
                elif ev.key == pygame.K_x:
                    if self.ammo_piercing > 0 and self.cd_piercing <= 0:
                        self.ammo_piercing -= 1
                        self.cd_piercing = 0.6
                        renpy.sound.play("projectile_piercing.wav", channel=3)
                        
                        new_proj = ProjectilesFactory.create_piercing(game.paddle.x, PADDLE_Y - PADDLE_HEIGHT)
                        self.projectiles.append(new_proj)
