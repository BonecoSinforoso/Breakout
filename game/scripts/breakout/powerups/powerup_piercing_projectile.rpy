init python:

    class PowerUpPiercingProjectile(PowerUp):

        SPRITES = [
            "images/powerups/powerup_piercing_projectile_00.png",
            "images/powerups/powerup_piercing_projectile_01.png",
            "images/powerups/powerup_piercing_projectile_02.png",
            "images/powerups/powerup_piercing_projectile_03.png",
            "images/powerups/powerup_piercing_projectile_04.png",
            "images/powerups/powerup_piercing_projectile_05.png"
        ]

        def apply_effect(self, game):
            game.arsenal.ammo_piercing += 1
