# TODO: desacoplar excessos (timers)
init python:

    import math

    class GameDisplayable(renpy.Displayable):

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
            self.timer_fire_ball = 0
            self.timer_giant_ball = 0

            # bola
            self.ball_default_image = Image("images/balls/ball_white.png")
            self.ball_fire_image = Image("images/balls/ball_fire.png")
            self.ball_giant_image = Image("images/balls/ball_giant.png")
            
            # Começa o jogo com uma bola travada na raquete
            self.balls = [
                Ball(self.player_x, PADDLE_Y - 20, 0.5, -0.5, BALL_SPEED_DEFAULT, stuck=True)
            ]

            # outros
            self.powerups = []

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
            return [self.paddle, self.ball_default_image] + block_frames

        def _lose_life(self):
            self.lives -= 1

            self.powerups.clear()
            self.reset_powerup_effects()

            if self.lives <= 0:
                self.winner = "eileen"
                renpy.timeout(0)
            else:
                self.stuck = True
                renpy.sound.play("ball_out.wav", channel=2)

                self.balls = [
                    Ball(self.player_x, PADDLE_Y - 20, 0.5, -0.5, BALL_SPEED_DEFAULT, stuck=True)
                ]

        def reset_powerup_effects(self):
            self.timer_increase_size = 0
            self.timer_slow_down = 0
            self.timer_fire_ball = 0
            self.timer_giant_ball = 0
            
            self.paddle_width = self.paddle_default_width
            self.paddle = self.paddle_default_image

        def render(self, width, height, st, at):
            r = renpy.Render(width, height)

            if self.old_st is None:
                self.old_st = st

            delta_time = st - self.old_st
            self.old_st = st

            if not self.stuck and not self.winner:
                self.time_elapsed += delta_time

            # timers
            if self.timer_increase_size > 0:
                self.timer_increase_size -= delta_time
                if self.timer_increase_size <= 0:
                    self.timer_increase_size = 0
                    self.paddle_width = self.paddle_default_width
                    self.paddle = self.paddle_default_image

            if self.timer_slow_down > 0:
                self.timer_slow_down -= delta_time
                if self.timer_slow_down < 0:
                    self.timer_slow_down = 0

            if self.timer_fire_ball > 0:
                self.timer_fire_ball -= delta_time
                if self.timer_fire_ball < 0:
                    self.timer_fire_ball = 0

            if self.timer_giant_ball > 0:
                self.timer_giant_ball -= delta_time
                if self.timer_giant_ball < 0:
                    self.timer_giant_ball = 0

            # Renderiza a raquete uma única vez
            pi = renpy.render(self.paddle, width, height, st, at)
            r.blit(pi, (int(self.player_x - self.paddle_width / 2), int(PADDLE_Y - PADDLE_HEIGHT / 2)))

            # Define os limites para quique da bola na parede
            ball_top = COURT_TOP + BALL_HEIGHT / 2
            ball_left = COURT_LEFT + BALL_WIDTH / 2
            ball_right = COURT_RIGHT - BALL_WIDTH / 2

            # Loop por cada bola ativa na tela
            for ball in self.balls[:]: 
                
                # Propriedades da Bola
                current_ball_speed = ball.speed
                b_image = self.ball_default_image
                b_w = BALL_WIDTH
                b_h = BALL_HEIGHT
                is_fireball = (self.timer_fire_ball > 0)

                if self.timer_slow_down > 0 and ball.dy > 0:
                    current_ball_speed *= 0.5
                
                if self.timer_giant_ball > 0:
                    current_ball_speed *= 1.5
                    b_image = self.ball_giant_image
                    b_w = 32
                    b_h = 32
                elif is_fireball:
                    b_image = self.ball_fire_image
                # --------------------------------------
                
                speed = delta_time * current_ball_speed
                old_ball_y = ball.y

                # Movimento
                if ball.stuck:
                    ball.x = self.player_x
                    ball.y = PADDLE_Y - 20
                else:
                    ball.x += ball.dx * speed
                    ball.y += ball.dy * speed

                # paredes usam b_w e b_h
                ball_top = COURT_TOP + b_h / 2
                ball_left = COURT_LEFT + b_w / 2
                ball_right = COURT_RIGHT - b_w / 2

                # Colisão com o Teto
                if ball.y < ball_top:
                    ball.y = ball_top + (ball_top - ball.y)
                    ball.dy = -ball.dy
                    if not ball.stuck:
                        renpy.sound.play("ball_collision.wav", channel=0)

                # Colisão Parede Esquerda
                if ball.x < ball_left:
                    ball.x = ball_left + (ball_left - ball.x)
                    ball.dx = -ball.dx
                    if not ball.stuck:
                        renpy.sound.play("ball_collision.wav", channel=0)

                # Colisão Parede Direita
                if ball.x > ball_right:
                    ball.x = ball_right - (ball.x - ball_right)
                    ball.dx = -ball.dx
                    if not ball.stuck:
                        renpy.sound.play("ball_collision.wav", channel=0)

                # Colisão com os Blocos (Agora passamos as dimensões atuais e o status de Fogo)
                ball.dx, ball.dy, score, new_powerups = self.block_grid.check_collision(ball.x, ball.y, b_w, b_h, ball.dx, ball.dy, is_fireball)

                self.score += score
                store.player_score = self.score
                self.powerups.extend(new_powerups)

                # --- COLISÃO COM A RAQUETE (Com Ângulo Dinâmico) ---
                paddle_left = self.player_x - self.paddle_width / 2
                paddle_right = self.player_x + self.paddle_width / 2
                hotside = PADDLE_Y - PADDLE_HEIGHT / 2

                if paddle_left <= ball.x <= paddle_right:
                    hit = False
                    if old_ball_y >= hotside >= ball.y:
                        ball.y = hotside - (ball.y - hotside)
                        hit = True
                    elif old_ball_y <= hotside <= ball.y:
                        ball.y = hotside - (ball.y - hotside)
                        hit = True

                    if hit:
                        renpy.sound.play("ball_collision.wav", channel=0)
                        
                        dist_from_center = ball.x - self.player_x
                        normalized_dist = max(-1.0, min(1.0, dist_from_center / (self.paddle_width / 2)))
                        bounce_angle = normalized_dist * 1.047 
                        
                        ball.dx = math.sin(bounce_angle) * 0.707
                        ball.dy = -math.cos(bounce_angle) * 0.707
                # ---------------------------------------------------

                # Renderiza a bola
                ball_img = renpy.render(b_image, width, height, st, at)
                r.blit(ball_img, (int(ball.x - b_w / 2), int(ball.y - b_h / 2)))

                # Verifica Morte desta bola específica
                if ball.y > 1080:
                    self.balls.remove(ball)

            # Render dos Blocos
            self.block_grid.render(r, width, height, st, at)

            # --- Logica dos PowerUps ---
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
                
                if (pu_right >= paddle_left and pu_left <= paddle_right and 
                    pu_bottom >= paddle_top and pu.y - pu.HEIGHT/2 <= paddle_bottom):
                    pu.apply_effect(self)
                    self.powerups.remove(pu)
                    renpy.sound.play("power_up_collected.wav", channel=1)
                elif pu.y > 1080:
                    self.powerups.remove(pu)
            # --------------------------

            # derrota/vitoria
            if len(self.balls) == 0 and not self.winner:
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

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.stuck = False
                
                for ball in self.balls:
                    ball.stuck = False

            # Tecla Q: desiste e vai pro You Lose
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_q:
                self.lives = 0
                self.balls.clear()

            # Tecla w: destroi todos os blocos
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_w:
                for block in self.block_grid.blocks:
                    while block.active:
                        destroyed, points = block.hit()
                        self.score += points
                                
                store.player_score = self.score

            renpy.restart_interaction()

            x = max(x, COURT_LEFT)
            x = min(x, COURT_RIGHT)
            self.player_x = x

            if self.winner:
                return self.winner
            else:
                raise renpy.IgnoreEvent()

label play_game:
    window hide
    $ quick_menu = False

    call screen game_screen

    $ quick_menu = True
    window show

    $ highscores = persistent.highscores + [(player_name, player_score)]
    $ highscores.sort(key=lambda x: x[1], reverse=True)
    $ persistent.highscores = highscores[:10]

    if _return == "eileen":
        "You lose."
        "[player_name] you scored [player_score] points"
    else:
        "You win! Congratulations!"
        "Block: [player_score - bonus_time - bonus_lives] points!"
        "Time Bonus: [bonus_time] points!"
        "Lives Bonus: [bonus_lives] points!"
        "[player_name] you scored a total of [player_score] points!"

    menu:
        "Would you like to play again?"
        "Yes.":
            jump play_game
        "No.":
            jump after_game

    return
