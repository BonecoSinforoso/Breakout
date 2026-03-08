# maestro do jogo
init python:

    import math

    class GameDisplayable(renpy.Displayable):

        def __init__(self):
            renpy.Displayable.__init__(self)

            # raquete
            self.paddle = Paddle(1920 / 2)

            # bola
            self.balls_manager = BallsManager()
            self.balls_manager.spawn_ball(self.paddle.x, PADDLE_Y - 20, 0.5, -0.5, BALL_SPEED_DEFAULT, stuck=True)
            
            # outros
            self.arsenal = Arsenal()
            self.debugger = Debugger()
            self.power_ups_manager = PowerUpsManager()
            
            self.projectiles = []

            self.stuck = True
            self.score = 0
            self.lives = 4

            self.time_elapsed = 0

            self.old_st = None
            self.winner = None

            self.block_grid = BlocksManager(COURT_LEFT, COURT_TOP)
        
        @property
        def formatted_time(self):
            minutes = int(self.time_elapsed) // 60
            seconds = int(self.time_elapsed) % 60
            return "{:02d}:{:02d}".format(minutes, seconds)

        def visit(self):
            block_frames = self.block_grid.get_all_frames()
            return [self.paddle.image, self.balls_manager.ball_default_image, self.balls_manager.ball_fire_image, self.balls_manager.ball_giant_image] + block_frames

        def _lose_life(self):
            self.lives -= 1
            self.power_ups_manager.clear()
            self.reset_powerup_effects()

            if self.lives <= 0:
                self.winner = "eileen"
                renpy.timeout(0)
            else:
                self.stuck = True
                renpy.sound.play("ball_out.wav", channel=2)
                
            self.balls_manager.clear()
            self.balls_manager.spawn_ball(self.paddle.x, PADDLE_Y - 20, 0.5, -0.5, BALL_SPEED_DEFAULT, stuck=True)

        def reset_powerup_effects(self):
            self.paddle.reset_effects()
            self.balls_manager.reset_effects()

        def render(self, width, height, st, at):
            r = renpy.Render(width, height)

            if self.old_st is None:
                self.old_st = st

            delta_time = st - self.old_st
            self.old_st = st

            if not self.stuck and not self.winner:
                self.time_elapsed += delta_time

            self.paddle.update(delta_time)

            projectile_points = self.arsenal.update_and_render(r, width, height, st, at, delta_time, self.block_grid)
            self.score += projectile_points

            # raquete
            self.paddle.render(r, width, height, st, at)

            points_earned, new_powerups = self.balls_manager.update_and_render(r, width, height, st, at, delta_time, self.paddle, self.block_grid)
            
            self.score += points_earned
            store.player_score = self.score

            self.power_ups_manager.add(new_powerups)

            # Render dos Blocos
            self.block_grid.render(r, width, height, st, at)

            self.power_ups_manager.update_and_render(r, width, height, st, at, delta_time, self.paddle, self)

            # derrota/vitoria
            if self.balls_manager.is_empty() and not self.winner:
                renpy.sound.play("result_lose.mp3", channel=0)
                self._lose_life()
                renpy.timeout(0)
            elif self.block_grid.all_destroyed() and not self.winner:
                renpy.sound.play("result_win.mp3", channel=0)
                self.winner = "player"

                bonus_lives = 100 * self.lives
                bonus_time = max(0, 300 - int(self.time_elapsed))

                store.bonus_lives = bonus_lives
                store.bonus_time = bonus_time

                store.player_score += bonus_lives
                store.player_score += bonus_time

                renpy.timeout(0)

            renpy.redraw(self, 0)
            return r

        def event(self, ev, x, y, st):
            import pygame

            x = max(x, COURT_LEFT)
            x = min(x, COURT_RIGHT)
            self.paddle.x = x

            # botao do mouse
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.stuck = False                
                self.balls_manager.release_all()

            self.arsenal.handle_input(ev, self)
            self.debugger.handle_input(ev, self)
            
            renpy.restart_interaction()            

            if self.winner:
                return self.winner
            else:
                raise renpy.IgnoreEvent()
