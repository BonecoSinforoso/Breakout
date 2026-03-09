init python:

    import math

    class BallsManager:

        def __init__(self):
            self.balls = []
            self.timer_slow_down = 0.0
            self.timer_fire_ball = 0.0
            self.timer_giant_ball = 0.0

            self.ball_default_image = Image("images/balls/ball_white.png")
            self.ball_fire_image = Image("images/balls/ball_fire.png")
            self.ball_giant_image = Image("images/balls/ball_giant.png")

        def spawn_ball(self, x, y, dx=0, dy=0, stuck=False):
            import random
                        
            if dx == 0 and dy == 0:
                dx = 0.5 * random.choice([-1, 1])
                dy = -0.5
                
            self.balls.append(Ball(x, y, dx, dy, BALL_SPEED_DEFAULT, stuck=stuck))

        def clear(self):
            self.balls.clear()

        def is_empty(self):
            return len(self.balls) == 0

        def release_all(self):
            for ball in self.balls:
                ball.stuck = False

        def reset_effects(self):
            self.timer_slow_down = 0.0
            self.timer_fire_ball = 0.0
            self.timer_giant_ball = 0.0

        def update_and_render(self, r, width, height, st, at, delta_time, paddle, blocks_manager, particles_manager):
            if self.timer_slow_down > 0: self.timer_slow_down = max(0, self.timer_slow_down - delta_time)
            if self.timer_fire_ball > 0: self.timer_fire_ball = max(0, self.timer_fire_ball - delta_time)
            if self.timer_giant_ball > 0: self.timer_giant_ball = max(0, self.timer_giant_ball - delta_time)

            points_earned = 0
            new_powerups = []
            is_fireball = (self.timer_fire_ball > 0)
            is_giantball = (self.timer_giant_ball > 0)

            for ball in self.balls[:]: 
                current_ball_speed = ball.speed
                b_image = self.ball_default_image
                b_w = BALL_WIDTH
                b_h = BALL_HEIGHT
                
                if self.timer_slow_down > 0 and ball.dy > 0:
                    current_ball_speed *= 0.5
                
                if is_giantball:
                    current_ball_speed *= 1.5
                    b_image = self.ball_giant_image
                    b_w = 32
                    b_h = 32
                elif is_fireball:
                    b_image = self.ball_fire_image
                
                speed = delta_time * current_ball_speed
                old_ball_y = ball.y

                if ball.stuck:
                    ball.x = paddle.x
                    ball.y = PADDLE_Y - 20
                else:
                    ball.x += ball.dx * speed
                    ball.y += ball.dy * speed

                ball_top = COURT_TOP + b_h / 2
                ball_left = COURT_LEFT + b_w / 2
                ball_right = COURT_RIGHT - b_w / 2

                # Colisao com o Teto e Paredes
                if ball.y < ball_top:
                    ball.y = ball_top + (ball_top - ball.y)
                    ball.dy = -ball.dy
                    if not ball.stuck: renpy.sound.play("ball_collision.wav", channel=0)

                if ball.x < ball_left:
                    ball.x = ball_left + (ball_left - ball.x)
                    ball.dx = -ball.dx
                    if not ball.stuck: renpy.sound.play("ball_collision.wav", channel=0)

                if ball.x > ball_right:
                    ball.x = ball_right - (ball.x - ball_right)
                    ball.dx = -ball.dx
                    if not ball.stuck: renpy.sound.play("ball_collision.wav", channel=0)

                # Colisao com os Blocos
                if not hasattr(ball, 'hit_cooldown'):
                    ball.hit_cooldown = 0.0
                
                if ball.hit_cooldown > 0:
                    ball.hit_cooldown -= delta_time

                score = 0
                dropped_pups = []

                if ball.hit_cooldown <= 0 or is_fireball:
                    
                    old_dx = ball.dx
                    old_dy = ball.dy
                    
                    ball.x, ball.y, ball.dx, ball.dy, score, dropped_pups = blocks_manager.check_collision(
                        ball.x, ball.y, b_w, b_h, ball.dx, ball.dy, is_fireball, is_giantball
                    )
                    
                    if (old_dx != ball.dx or old_dy != ball.dy) and not is_fireball:
                        ball.hit_cooldown = 0.05
                    
                    if (old_dx != ball.dx or old_dy != ball.dy) or score > 0:
                        
                        if is_fireball:
                            particles_manager.spawn_burst(ball.x, ball.y, amount=15, color="#FF3333")
                        elif is_giantball:
                            particles_manager.spawn_burst(ball.x, ball.y, amount=15, color="#33FF33")
                        else:
                            particles_manager.spawn_burst(ball.x, ball.y, amount=8, color="#FFDD00")
                
                points_earned += score
                new_powerups.extend(dropped_pups)

                # Colisao com a Raquete
                paddle_left = paddle.x - paddle.width / 2
                paddle_right = paddle.x + paddle.width / 2
                paddle_top = PADDLE_Y - paddle.height / 2
                paddle_bottom = PADDLE_Y + paddle.height / 2

                ball_left = ball.x - b_w / 2
                ball_right = ball.x + b_w / 2
                ball_top = ball.y - b_h / 2
                ball_bottom = ball.y + b_h / 2

                if (ball.dy > 0 and 
                    ball_right >= paddle_left and ball_left <= paddle_right and 
                    ball_bottom >= paddle_top and ball_top <= paddle_bottom):
                    
                    renpy.sound.play("ball_collision.wav", channel=0)
                    
                    dist_from_center = ball.x - paddle.x
                    normalized_dist = max(-1.0, min(1.0, dist_from_center / (paddle.width / 2)))
                    bounce_angle = normalized_dist * 1.047 
                    
                    ball.dx = math.sin(bounce_angle) * 0.707
                    ball.dy = -abs(math.cos(bounce_angle) * 0.707)

                    ball.hit_cooldown = 0.05

                    particles_manager.spawn_burst(ball.x, paddle_top, amount=5, color="#00FFFF", speed_min=100, speed_max=300)

                # Renderiza a bola
                ball_img = renpy.render(b_image, width, height, st, at)
                r.blit(ball_img, (int(ball.x - b_w / 2), int(ball.y - b_h / 2)))

                # trail
                if not hasattr(ball, 'history'):
                    ball.history = []                
                
                if not ball.stuck:
                    ball.history.append((ball.x, ball.y))
                
                    if len(ball.history) > 6:
                        ball.history.pop(0)
                
                canvas = r.canvas()
                for i, (hx, hy) in enumerate(ball.history):
                    t = (i + 1) / float(len(ball.history))
                    size = int((b_w * 0.6) * t)
                    
                    if size > 0:                        
                        trail_color = "#AAAAAA"
                        if is_fireball: trail_color = "#FF3333"
                        elif is_giantball: trail_color = "#33FF33"
                        
                        canvas.rect(trail_color, (int(hx - size/2), int(hy - size/2), size, size))

                # destruicao da bola
                if ball.y > 1080:
                    self.balls.remove(ball)

            return points_earned, new_powerups
