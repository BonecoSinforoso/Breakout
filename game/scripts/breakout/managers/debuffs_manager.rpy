# gerenciador do ciclo de vida e colisao dos debuffs na tela
init 1 python:

    import random
   
    class DebuffsManager:

        def __init__(self) -> None:
            self.active_debuffs = []
            self.spawn_timer = random.uniform(5.0, 15.0)

        def update_and_render(self, r, width: int, height: int, st: float, at: float, delta_time: float, paddle, game, particles_manager) -> None:
            if not game.stuck and not game.winner:
                self.spawn_timer -= delta_time

                if self.spawn_timer <= 0:
                    self.spawn_timer = random.uniform(15.0, 30.0)
                    spawn_x = random.randint(int(COURT_LEFT + 50), int(COURT_RIGHT - 50))
                    
                    new_debuff = DebuffsFactory.get_random_debuff(spawn_x, 0)
                    if new_debuff:
                        self.active_debuffs.append(new_debuff)

            for debuff in self.active_debuffs[:]:
                debuff.update(delta_time, paddle.x)
                debuff.render(r, width, height, st, at)
                
                # hitbox mais razoavel
                hitbox_w = debuff.WIDTH * 0.6
                hitbox_h = debuff.HEIGHT * 0.6
                
                db_left = debuff.x - hitbox_w / 2
                db_right = debuff.x + hitbox_w / 2
                db_bottom = debuff.y + hitbox_h / 2
                
                paddle_left = paddle.x - paddle.width / 2
                paddle_right = paddle.x + paddle.width / 2
                paddle_top = PADDLE_Y - PADDLE_HEIGHT / 2
                paddle_bottom = PADDLE_Y + PADDLE_HEIGHT / 2
                
                # checagem de colisao
                if (db_right >= paddle_left and db_left <= paddle_right and 
                    db_bottom >= paddle_top and debuff.y - hitbox_h / 2 <= paddle_bottom):
                    
                    debuff.apply_effect(game)
                    self.active_debuffs.remove(debuff)
                    renpy.sound.play("debuff_collected.wav", channel=4)
                    particles_manager.spawn_burst(debuff.x, PADDLE_Y, amount=20, speed_min=150, speed_max=400)
                    
                # destruicao ao sair da tela
                elif debuff.y > SCREEN_HEIGHT:
                    self.active_debuffs.remove(debuff)
