init python:

    class PowerUpBasicProjectile(PowerUp):

        SPRITES = [
            "images/powerups/powerup_basic_projectile_00.png",
            "images/powerups/powerup_basic_projectile_01.png",
            "images/powerups/powerup_basic_projectile_02.png",
            "images/powerups/powerup_basic_projectile_03.png",
            "images/powerups/powerup_basic_projectile_04.png",
            "images/powerups/powerup_basic_projectile_05.png"
        ]

        def apply_effect(self, game):
            game.projectiles_manager.ammo_basic += 5
