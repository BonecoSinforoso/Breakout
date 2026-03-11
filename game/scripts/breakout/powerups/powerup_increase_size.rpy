init python:

    class PowerUpIncreaseSize(PowerUp):

        SPRITES = [
            "images/powerups/powerup_increase_size_00.png",
            "images/powerups/powerup_increase_size_01.png",
            "images/powerups/powerup_increase_size_02.png",
            "images/powerups/powerup_increase_size_03.png",
            "images/powerups/powerup_increase_size_04.png",
            "images/powerups/powerup_increase_size_05.png"
        ]

        def apply_effect(self, game):
            game.paddle.increase_size(10.0)
