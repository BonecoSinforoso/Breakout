init python:

    import math
    import random

    class PowerUpExtraBall(PowerUp):

        SPRITES = [
            "images/powerups/powerup_extra_ball_00.png",
            "images/powerups/powerup_extra_ball_01.png",
            "images/powerups/powerup_extra_ball_02.png",
            "images/powerups/powerup_extra_ball_03.png",
            "images/powerups/powerup_extra_ball_04.png",
            "images/powerups/powerup_extra_ball_05.png"
        ]

        def apply_effect(self, game):
            angle = random.uniform(-0.785, 0.785)
            new_dx = math.sin(angle) * 0.707
            new_dy = -math.cos(angle) * 0.707

            game.balls_manager.spawn_ball(
                game.paddle.x, 
                PADDLE_Y - 20, 
                new_dx, 
                new_dy,
                stuck=False
            )
