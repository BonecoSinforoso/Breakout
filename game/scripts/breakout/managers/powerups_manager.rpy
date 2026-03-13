# Gerenciador do ciclo de vida e colisao dos power ups na tela
init 1 python:
    
    class PowerUpsManager:

        def __init__(self) -> None:
            self.active_powerups = []

        def add(self, new_powerups: list) -> None:
            self.active_powerups.extend(new_powerups)

        def clear(self) -> None:
            self.active_powerups.clear()

        def update_and_render(self, r, width: int, height: int, st: float, at: float, delta_time: float, paddle, game, particles_manager) -> None:
            for powerup in self.active_powerups[:]:
                powerup.update(delta_time)
                powerup.render(r, width, height, st, at)
                
                powerup_left = powerup.x - powerup.WIDTH / 2
                powerup_right = powerup.x + powerup.WIDTH / 2
                powerup_bottom = powerup.y + powerup.HEIGHT / 2
                
                paddle_left = paddle.x - paddle.width / 2
                paddle_right = paddle.x + paddle.width / 2
                paddle_top = PADDLE_Y - PADDLE_HEIGHT / 2
                paddle_bottom = PADDLE_Y + PADDLE_HEIGHT / 2
                
                # checagem de colisao
                if (powerup_right >= paddle_left and powerup_left <= paddle_right and 
                    powerup_bottom >= paddle_top and powerup.y - powerup.HEIGHT / 2 <= paddle_bottom):
                    
                    powerup.apply_effect(game)
                    self.active_powerups.remove(powerup)
                    renpy.sound.play("powerup_collected.wav", channel=1)
                    particles_manager.spawn_burst(powerup.x, PADDLE_Y, amount=20, speed_min=150, speed_max=400)
                
                elif powerup.y > SCREEN_HEIGHT:
                    self.active_powerups.remove(powerup)
