# maestro do jogo
# TODO: ficou imenso de novo (refatorar)
init python:

    import math

    class GameDisplayable(renpy.Displayable):

        def __init__(self):
            renpy.Displayable.__init__(self)

            # core
            self.stuck = True
            self.score = 0
            self.lives = 4
            self.winner = None
            self.time_elapsed = 0
            self.old_st = None

            # raquete
            self.paddle = Paddle(1920 / 2)

            # bola
            self.balls_manager = BallsManager()
            
            # shake
            self.shake_timer = 0.0
            self.shake_intensity = 0.0

            # outras classes
            self.arsenal = Arsenal()
            self.debuffs_manager = DebuffsManager()
            self.particles_manager = ParticlesManager()            
            self.powerups_manager = PowerUpsManager()

            # inicializacao de outras classes
            self.balls_manager.spawn_ball(self.paddle.x, PADDLE_Y - 20, stuck=True)
            self.blocks_manager = BlocksManager(COURT_LEFT, COURT_TOP, store.current_level)
        
        @property
        def formatted_time(self):
            minutes = int(self.time_elapsed) // 60
            seconds = int(self.time_elapsed) % 60
            return "{:02d}:{:02d}".format(minutes, seconds)

        def visit(self):
            block_frames = self.blocks_manager.get_all_frames()
            return [self.paddle.image, self.balls_manager.ball_default_image, self.balls_manager.ball_fire_image, self.balls_manager.ball_giant_image] + block_frames

        def _lose_life(self):
            self.lives -= 1
            self.powerups_manager.clear()
            self.reset_powerup_effects()

            self.shake_timer = 0.4
            self.shake_intensity = 15.0

            if self.lives <= 0:
                self.winner = "eileen"
                renpy.timeout(0)
            else:
                self.stuck = True
                renpy.sound.play("ball_out.wav", channel=2)
                
            self.balls_manager.clear()
            self.balls_manager.spawn_ball(self.paddle.x, PADDLE_Y - 20, stuck=True)

        def reset_powerup_effects(self):
            self.paddle.reset_effects()
            self.balls_manager.reset_effects()

        def render(self, width, height, st, at):
            r = renpy.Render(width, height)

            if self.old_st is None:
                self.old_st = st

            delta_time = st - self.old_st
            self.old_st = st

            # super importante para nao ter salto por conta do pause
            if delta_time > 0.1:
                delta_time = 0.016

            if not self.stuck and not self.winner:
                self.time_elapsed += delta_time

            self.paddle.update(delta_time)

            projectile_points = self.arsenal.update_and_render(r, width, height, st, at, delta_time, self.blocks_manager)
            self.score += projectile_points

            # raquete
            self.paddle.render(r, width, height, st, at)

            points_earned, new_powerups = self.balls_manager.update_and_render(r, width, height, st, at, delta_time, self.paddle, self.blocks_manager, self.particles_manager)
            
            self.score += points_earned
            store.player_score = self.score

            self.powerups_manager.add(new_powerups)

            # updates de outras classes
            self.blocks_manager.render(r, width, height, st, at)
            self.debuffs_manager.update_and_render(r, width, height, st, at, delta_time, self.paddle, self, self.particles_manager)
            self.particles_manager.update_and_render(r, delta_time)
            self.powerups_manager.update_and_render(r, width, height, st, at, delta_time, self.paddle, self, self.particles_manager)

            # derrota/vitoria
            if self.balls_manager.is_empty() and not self.winner:
                renpy.sound.play("result_lose.mp3", channel=0)
                self._lose_life()
                renpy.timeout(0)
            elif self.blocks_manager.all_destroyed() and not self.winner:
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

            if self.shake_timer > 0:
                import random
                
                self.shake_timer -= delta_time
                self.shake_intensity *= 0.9
                
                offset_x = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
                offset_y = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
                
                shaken_render = renpy.Render(width, height)
                shaken_render.blit(r, (offset_x, offset_y))
                
                return shaken_render

            return r

        def event(self, ev, x, y, st):

            import pygame

            if (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE) or \
                (ev.type == pygame.MOUSEBUTTONUP and ev.button == 3):
                return None

            x = max(x, COURT_LEFT)
            x = min(x, COURT_RIGHT)
            self.paddle.x = x

            # botao do mouse
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.stuck = False                
                self.balls_manager.release_all()

            # teclas
            self.arsenal.handle_input(ev, self)
            
            renpy.restart_interaction()            

            if self.winner:
                return self.winner
            else:
                raise renpy.IgnoreEvent()
