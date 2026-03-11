init python:

    class PowerUpFireball(PowerUp):

        SPRITES = [
            "images/powerups/powerup_fire_ball_00.png",
            "images/powerups/powerup_fire_ball_01.png",
            "images/powerups/powerup_fire_ball_02.png",
            "images/powerups/powerup_fire_ball_03.png",
            "images/powerups/powerup_fire_ball_04.png",
            "images/powerups/powerup_fire_ball_05.png"
        ]

        def apply_effect(self, game):
            game.balls_manager.timer_fire_ball += 8.0
            game.balls_manager.timer_giant_ball = 0
