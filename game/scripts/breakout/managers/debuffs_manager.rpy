init 1 python:

    import random
   
    class DebuffsManager:

        SPAWN_INTERVAL = 15.0

        def __init__(self):
            self.active_debuffs = []
            self.spawn_timer = self.SPAWN_INTERVAL + random.uniform(0.0, 5.0)

        def update_and_render(self, r, width, height, st, at, delta_time, paddle, game, particles_manager):
            self.spawn_timer -= delta_time

            if self.spawn_timer <= 0:
                self.spawn_timer = self.SPAWN_INTERVAL + random.uniform(-2.0, 3.0)
                spawn_x = random.randint(int(COURT_LEFT + 50), int(COURT_RIGHT - 50))
                self.active_debuffs.append(DebuffDecreaseSize(spawn_x, 0))

            for debuff in self.active_debuffs[:]:
                debuff.update(delta_time, paddle.x)
                debuff.render(r, width, height, st, at)
                
                debuff_left = debuff.x - debuff.WIDTH / 2
                debuff_right = debuff.x + debuff.WIDTH / 2
                debuff_bottom = debuff.y + debuff.HEIGHT / 2
                
                paddle_left = paddle.x - paddle.width / 2
                paddle_right = paddle.x + paddle.width / 2
                paddle_top = PADDLE_Y - PADDLE_HEIGHT / 2
                paddle_bottom = PADDLE_Y + PADDLE_HEIGHT / 2
                
                if (debuff_right >= paddle_left and debuff_left <= paddle_right and 
                    debuff_bottom >= paddle_top and debuff.y - debuff.HEIGHT/2 <= paddle_bottom):
                    
                    debuff.apply_effect(game)
                    self.active_debuffs.remove(debuff)
                    # renpy.sound.play("powerup_collected.wav", channel=1)
                    particles_manager.spawn_burst(debuff.x, PADDLE_Y, amount=20, speed_min=150, speed_max=400)
                    
                elif debuff.y > 1080:
                    self.active_debuffs.remove(debuff)
