# gerente dos power ups
# TODO: separar o factory do manager
init 1 python:
    
    import random

    class PowerUpsManager:

        CATALOG = {
            "increase_size": {
                "class": PowerUpIncreaseSize, 
                "active": False
            },
            "slow_down": {
                "class": PowerUpSlowDown, 
                "active": False
            },
            "extra_ball": {
                "class": PowerUpExtraBall,
                "active": False
            },
            "fire_ball": {
                "class": PowerUpFireball,
                "active": False
            },
            "giant_ball": {
                "class": PowerUpGiantBall,
                "active": False
            },
            "basic_projectile": {
                "class": PowerUpBasicProjectile,
                "active": False
            },
            "piercing_projectile": {
                "class": PowerUpPiercingProjectile,
                "active": True
            }
        }

        @classmethod
        def get_random_drop(cls, x, y):
            active_list = [data["class"] for key, data in cls.CATALOG.items() if data["active"]]
            
            if not active_list:
                return None
            
            chosen_powerup = random.choice(active_list)
            
            return chosen_powerup(x, y)
            
        @classmethod
        def set_active(cls, powerup_name, is_active):            
            if powerup_name in cls.CATALOG:
                cls.CATALOG[powerup_name]["active"] = is_active

        def __init__(self):
            self.active_powerups = []

        def add(self, new_powerups):
            self.active_powerups.extend(new_powerups)

        def clear(self):
            self.active_powerups.clear()

        def update_and_render(self, r, width, height, st, at, delta_time, paddle, game):
            for pu in self.active_powerups[:]:
                pu.update(delta_time)
                pu.render(r, width, height, st, at)
                
                pu_left = pu.x - pu.WIDTH / 2
                pu_right = pu.x + pu.WIDTH / 2
                pu_bottom = pu.y + pu.HEIGHT / 2
                
                paddle_left = paddle.x - paddle.width / 2
                paddle_right = paddle.x + paddle.width / 2
                paddle_top = PADDLE_Y - PADDLE_HEIGHT / 2
                paddle_bottom = PADDLE_Y + PADDLE_HEIGHT / 2
                
                if (pu_right >= paddle_left and pu_left <= paddle_right and 
                    pu_bottom >= paddle_top and pu.y - pu.HEIGHT/2 <= paddle_bottom):
                    
                    pu.apply_effect(game)
                    self.active_powerups.remove(pu)
                    renpy.sound.play("powerup_collected.wav", channel=1)
                
                elif pu.y > 1080:
                    self.active_powerups.remove(pu)
