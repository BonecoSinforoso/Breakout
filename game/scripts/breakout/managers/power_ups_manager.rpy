# gerente dos power ups
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
            
            ativos = [dados["class"] for chave, dados in cls.CATALOG.items() if dados["active"]]
            
            if not ativos:
                return None
            
            powerup_escolhido = random.choice(ativos)
            
            return powerup_escolhido(x, y)
            
        @classmethod
        def set_active(cls, powerup_name, is_active):
            
            if powerup_name in cls.CATALOG:
                cls.CATALOG[powerup_name]["active"] = is_active
