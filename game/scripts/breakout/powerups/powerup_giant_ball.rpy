init python:

    class PowerUpGiantBall(PowerUp):
        
        SPRITES = [
            "images/powerups/powerup_giant_ball_00.png",
            "images/powerups/powerup_giant_ball_01.png",
            "images/powerups/powerup_giant_ball_02.png",
            "images/powerups/powerup_giant_ball_03.png",
            "images/powerups/powerup_giant_ball_04.png",
            "images/powerups/powerup_giant_ball_05.png"
        ]

        def apply_effect(self, game):
            game.balls_manager.timer_giant_ball += 10.0
            game.balls_manager.timer_fire_ball = 0
