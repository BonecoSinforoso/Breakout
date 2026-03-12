init 1 python:

    import random
   
    class DebuffsManager:

        def __init__(self):
            self.active_debuffs = []
            
            self.spawn_timer = random.uniform(5.0, 15.0)

        def update_and_render(self, r, width, height, st, at, delta_time, paddle, game, particles_manager):
            if not game.stuck and not game.winner:
                self.spawn_timer -= delta_time

                if self.spawn_timer <= 0:
                    self.spawn_timer = random.uniform(15.0, 30.0)
                    spawn_x = random.randint(int(COURT_LEFT + 50), int(COURT_RIGHT - 50))
                    self.active_debuffs.append(DebuffDecreaseSize(spawn_x, 0))

            for debuff in self.active_debuffs[:]:
                debuff.update(delta_time, paddle.x)
                debuff.render(r, width, height, st, at)
                
                hitbox_w = debuff.WIDTH * 0.6
                hitbox_h = debuff.HEIGHT * 0.6
                
                db_left = debuff.x - hitbox_w / 2
                db_right = debuff.x + hitbox_w / 2
                db_bottom = debuff.y + hitbox_h / 2
                
                paddle_left = paddle.x - paddle.width / 2
                paddle_right = paddle.x + paddle.width / 2
                paddle_top = PADDLE_Y - PADDLE_HEIGHT / 2
                paddle_bottom = PADDLE_Y + PADDLE_HEIGHT / 2
                
                if (db_right >= paddle_left and db_left <= paddle_right and 
                    db_bottom >= paddle_top and debuff.y - hitbox_h / 2 <= paddle_bottom):
                    
                    debuff.apply_effect(game)
                    self.active_debuffs.remove(debuff)
                    renpy.sound.play("debuff_collected.wav", channel=4)
                    particles_manager.spawn_burst(debuff.x, PADDLE_Y, amount=20, speed_min=150, speed_max=400)
                    
                elif debuff.y > 1080:
                    self.active_debuffs.remove(debuff)
