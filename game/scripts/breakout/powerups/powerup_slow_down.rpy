init python:

    class PowerUpSlowDown(PowerUp):
        
        SPRITES = [
            "images/powerups/powerup_slow_down_00.png",
            "images/powerups/powerup_slow_down_01.png",
            "images/powerups/powerup_slow_down_02.png",
            "images/powerups/powerup_slow_down_03.png",
            "images/powerups/powerup_slow_down_04.png",
            "images/powerups/powerup_slow_down_05.png"
        ]

        def apply_effect(self, game):
            game.balls_manager.timer_slow_down = 10.0
