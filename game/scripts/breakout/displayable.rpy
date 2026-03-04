# TODO: desacoplar excessos
init python:

    import math

    class BreakoutDisplayable(renpy.Displayable):

        def __init__(self):
            renpy.Displayable.__init__(self)

            self.player_x = 1920 / 2

            # raquete
            self.paddle = Image("images/paddles/paddle_red_02.png")
            self.paddle_width = 64

            self.paddle_default_width = 64
            self.paddle_default_image = Image("images/paddles/paddle_red_02.png")

            # timers
            self.timer_increase_size = 0
            self.timer_slow_down = 0

            # bola
            self.ball = Image("images/balls/ball_white.png")
            self.ball_x = self.player_x
            self.ball_y = 0
            self.ball_direction_x = 0.5
            self.ball_direction_y = -0.5
            self.ball_speed = BALL_SPEED_DEFAULT

            # outros
            self.powerups = []

            self.stuck = True
            self.score = 0
            self.lives = 4

            self.old_st = None
            self.winner = None

            self.block_grid = BlocksManager(COURT_LEFT, COURT_TOP)

        def visit(self):
            block_frames = self.block_grid.get_all_frames()
            return [self.paddle, self.ball] + block_frames

        def _lose_life(self):
            self.lives -= 1

            if self.lives <= 0:
                self.winner = "eileen"
                renpy.timeout(0)
            else:
                # Devolve a bola ao jogador
                renpy.sound.play("breakou_ball_out.wav", channel=2)
                self.stuck = True
                self.ball_speed = BALL_SPEED_DEFAULT
                self.ball_direction_x = 0.5
                self.ball_direction_y = -0.5
                self.ball_x = self.player_x
                self.ball_y = PADDLE_Y - 20

        def render(self, width, height, st, at):
            r = renpy.Render(width, height)

            if self.old_st is None:
                self.old_st = st

            delta_time = st - self.old_st
            self.old_st = st

            # timer powerup increase size
            if self.timer_increase_size > 0:
                self.timer_increase_size -= delta_time
                if self.timer_increase_size <= 0:
                    self.timer_increase_size = 0
                    self.paddle_width = self.paddle_default_width
                    self.paddle = self.paddle_default_image

            # timer slow down
            if self.timer_slow_down > 0:
                self.timer_slow_down -= delta_time
                if self.timer_slow_down < 0:
                    self.timer_slow_down = 0

            current_ball_speed = self.ball_speed

            if self.timer_slow_down > 0 and self.ball_direction_y > 0:
                current_ball_speed = self.ball_speed * 0.5
            
            speed = delta_time * current_ball_speed
            old_ball_y = self.ball_y

            if self.stuck:
                self.ball_x = self.player_x
                self.ball_y = PADDLE_Y - 20
            else:
                self.ball_x += self.ball_direction_x * speed
                self.ball_y += self.ball_direction_y * speed

            ball_top = COURT_TOP + BALL_HEIGHT / 2
            ball_left = COURT_LEFT + BALL_WIDTH / 2
            ball_right = COURT_RIGHT - BALL_WIDTH / 2

            if self.ball_y < ball_top:
                self.ball_y = ball_top + (ball_top - self.ball_y)
                self.ball_direction_y = -self.ball_direction_y

                if not self.stuck:
                    renpy.sound.play("breakout_ball_collision.wav", channel=0)

            if self.ball_x < ball_left:
                self.ball_x = ball_left + (ball_left - self.ball_x)
                self.ball_direction_x = -self.ball_direction_x

                if not self.stuck:
                    renpy.sound.play("breakout_ball_collision.wav", channel=0)

            if self.ball_x > ball_right:
                self.ball_x = ball_right - (self.ball_x - ball_right)
                self.ball_direction_x = -self.ball_direction_x

                if not self.stuck:
                    renpy.sound.play("breakout_ball_collision.wav", channel=0)

            # Colisao e render dos blocos
            self.ball_direction_x, self.ball_direction_y, score, new_powerups = self.block_grid.check_collision(
                self.ball_x, self.ball_y,
                BALL_WIDTH, BALL_HEIGHT,
                self.ball_direction_x, self.ball_direction_y
            )

            self.powerups.extend(new_powerups)

            self.score += score
            store.player_score = self.score

            self.block_grid.render(r, width, height, st, at)

            # Logica dos PowerUps
            for pu in self.powerups[:]:
                pu.update(delta_time)
                pu.render(r, width, height, st, at)
                                
                pu_left = pu.x - pu.WIDTH / 2
                pu_right = pu.x + pu.WIDTH / 2
                pu_bottom = pu.y + pu.HEIGHT / 2
                
                paddle_left = self.player_x - self.paddle_width / 2
                paddle_right = self.player_x + self.paddle_width / 2
                paddle_top = PADDLE_Y - PADDLE_HEIGHT / 2
                paddle_bottom = PADDLE_Y + PADDLE_HEIGHT / 2
                
                # Se colidiu com o paddle
                if (pu_right >= paddle_left and pu_left <= paddle_right and 
                    pu_bottom >= paddle_top and pu.y - pu.HEIGHT/2 <= paddle_bottom):
                    pu.apply_effect(self)
                    self.powerups.remove(pu)
                    renpy.sound.play("breakout_powerup.wav", channel=1)
                
                # Se saiu pela parte inferior da tela
                elif pu.y > 1080:
                    self.powerups.remove(pu)

            def paddle_fn(position_x, position_y, hotside):
                pi = renpy.render(self.paddle, width, height, st, at)
                r.blit(pi, (int(position_x - self.paddle_width / 2), int(position_y - PADDLE_HEIGHT / 2)))

                if position_x - self.paddle_width / 2 <= self.ball_x <= position_x + self.paddle_width / 2:
                    hit = False

                    if old_ball_y >= hotside >= self.ball_y:
                        self.ball_y = hotside - (self.ball_y - hotside)
                        hit = True
                    elif old_ball_y <= hotside <= self.ball_y:
                        self.ball_y = hotside - (self.ball_y - hotside)
                        hit = True
                    
                    if hit:
                        renpy.sound.play("breakout_ball_collision.wav", channel=0)
                        
                        dist_from_center = self.ball_x - position_x
                        half_width = self.paddle_width / 2
                        
                        normalized_dist = dist_from_center / half_width
                        normalized_dist = max(-1.0, min(1.0, normalized_dist))
                        
                        max_angle = 1.047 
                        bounce_angle = normalized_dist * max_angle
                        
                        new_dx = math.sin(bounce_angle)
                        new_dy = -math.cos(bounce_angle)
                        
                        self.ball_direction_x = new_dx * 0.707
                        self.ball_direction_y = new_dy * 0.707

            paddle_fn(self.player_x, PADDLE_Y, PADDLE_Y - PADDLE_HEIGHT / 2)

            ball = renpy.render(self.ball, width, height, st, at)
            r.blit(ball, (int(self.ball_x - BALL_WIDTH / 2), int(self.ball_y - BALL_HEIGHT / 2)))

            # vitoria/derrota
            if self.ball_y > 1080 and not self.winner:
                self._lose_life()
                renpy.timeout(0)
            elif self.block_grid.all_destroyed():
                self.winner = "player"
                renpy.timeout(0)

            renpy.redraw(self, 0)
            return r

        def event(self, ev, x, y, st):
            import pygame

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.stuck = False

            # Tecla Q: desiste e vai pro You Lose
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_q:
                self.winner = "eileen"
                renpy.timeout(0)

            renpy.restart_interaction()

            x = max(x, COURT_LEFT)
            x = min(x, COURT_RIGHT)
            self.player_x = x

            if self.winner:
                return self.winner
            else:
                raise renpy.IgnoreEvent()

label play_breakout:
    window hide
    $ quick_menu = False

    call screen game

    $ quick_menu = True
    window show

    $ highscores = persistent.highscores + [(player_name, player_score)]
    $ highscores.sort(key=lambda x: x[1], reverse=True)  # ordena por score decrescente
    $ persistent.highscores = highscores[:10]  # top 10

    if _return == "eileen":
        "You lose!"
        "[player_name] you scored [player_score] points"
    else:
        "You win! Congratulations."
        "[player_name] you scored [player_score] points"

    menu:
        "Play again?"
        "Yes.":
            jump play_breakout
        "No.":
            jump after_breakout

    return
