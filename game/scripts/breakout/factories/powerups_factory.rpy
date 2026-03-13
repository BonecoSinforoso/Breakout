# responsavel por instanciar e sortear os power ups
init 1 python:

    import random

    class PowerUpsFactory:        

        CATALOG = {
            "increase_size":
            {
                "class": PowerUpIncreaseSize,
                "active": True
            },
            "slow_down":
            {
                "class": PowerUpSlowDown,
                "active": True
            },
            "extra_ball":
            {
                "class": PowerUpExtraBall,
                "active": True
            },
            "fire_ball":
            {
                "class": PowerUpFireball,
                "active": True
            },
            "giant_ball":
            {
                "class": PowerUpGiantBall,
                "active": True
            },
            "basic_projectile":
            {
                "class": PowerUpBasicProjectile,
                "active": True
            },
            "piercing_projectile":
            {
                "class": PowerUpPiercingProjectile,
                "active": True
            }
        }

        @classmethod
        def get_random_powerup(cls, x: float, y: float):
            active_list = [data["class"] for key, data in cls.CATALOG.items() if data["active"]]
            
            if not active_list:
                return None
            
            chosen_powerup = random.choice(active_list)
            return chosen_powerup(x, y)
            
        @classmethod
        def set_active(cls, powerup_name: str, is_active: bool) -> None:
            if powerup_name in cls.CATALOG:
                cls.CATALOG[powerup_name]["active"] = is_active
