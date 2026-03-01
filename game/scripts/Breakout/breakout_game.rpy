init python:

    class PongDisplayable(renpy.Displayable):

        def __init__(self):
            renpy.Displayable.__init__(self)

            ### State
            self.paddle = Image("images/paddles/paddle_red_02.png")
            self.ball = Image("images/balls/ball_white.png")

            self.stuck = True
            self.score = 0
            self.lives = 4
            self.player_x = 1920 / 2

            self.ball_x = self.player_x
            self.ball_y = 0
            self.ball_direction_x = 0.5
            self.ball_direction_y = -0.5
            self.ball_speed = 500.0

            self.old_st = None
            self.winner = None

            self.block_grid = BreakoutBlocks(COURT_LEFT, COURT_TOP)

        def visit(self):
            block_frames = [f for frames in self.block_grid._frames.values() for f in frames]
            return [self.paddle, self.ball] + block_frames

        def _lose_life(self):
            self.lives -= 1

            if self.lives <= 0:
                self.winner = "eileen"
                renpy.timeout(0)
            else:
                # Devolve a bola ao jogador
                self.stuck = True
                self.ball_speed = 500.0
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

            speed = delta_time * self.ball_speed
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

            # Colisão e render dos blocos
            self.ball_direction_x, self.ball_direction_y, hits = self.block_grid.check_collision(
                self.ball_x, self.ball_y,
                BALL_WIDTH, BALL_HEIGHT,
                self.ball_direction_x, self.ball_direction_y
            )

            self.score += hits * 10

            self.block_grid.render(r, width, height, st, at)

            # paddle_fn com corpo completo da colisão
            def paddle_fn(position_x, position_y, hotside):
                pi = renpy.render(self.paddle, width, height, st, at)
                r.blit(pi, (int(position_x - PADDLE_WIDTH / 2), int(position_y - PADDLE_HEIGHT / 2)))

                if position_x - PADDLE_WIDTH / 2 <= self.ball_x <= position_x + PADDLE_WIDTH / 2:
                    hit = False

                    if old_ball_y >= hotside >= self.ball_y:
                        self.ball_y = hotside - (self.ball_y - hotside)
                        self.ball_direction_y = -self.ball_direction_y
                        hit = True
                    elif old_ball_y <= hotside <= self.ball_y:
                        self.ball_y = hotside - (self.ball_y - hotside)
                        self.ball_direction_y = -self.ball_direction_y
                        hit = True
                    if hit:
                        renpy.sound.play("breakout_ball_collision.wav", channel=0)
                        self.ball_speed *= 1.10

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

label play_pong:
    window hide
    $ quick_menu = False

    call screen pong

    $ quick_menu = True
    window show

    if _return == "eileen":
        "You lose!"
    else:
        "You win! Congratulations."

    menu:
        "Play again?"
        "Yes.":
            jump play_pong
        "No.":
            jump after_pong

    return
