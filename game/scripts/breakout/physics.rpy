# responsavel apenas pelos calculos matematicos puros de colisao e repulsao vetorial
init 1 python:

    import math

    class Physics:
        
        # REBOTE RETO (usado para Blocos)
        @staticmethod
        def resolve_aabb_bounce(ball_x: float, ball_y: float, ball_w: float, ball_h: float, ball_dx: float, ball_dy: float, col_dx: float, col_dy: float):
            overlap_x = (ball_w / 2) - abs(col_dx)
            overlap_y = (ball_h / 2) - abs(col_dy)

            if overlap_x < overlap_y:
                if col_dx > 0:
                    ball_dx = abs(ball_dx)
                    ball_x += overlap_x + 1
                else:
                    ball_dx = -abs(ball_dx)
                    ball_x -= overlap_x + 1
            else:
                if col_dy > 0:
                    ball_dy = abs(ball_dy)
                    ball_y += overlap_y + 1
                else:
                    ball_dy = -abs(ball_dy)
                    ball_y -= overlap_y + 1
                    
            return ball_x, ball_y, ball_dx, ball_dy

        # REBOTE ANGULAR (usado para a Raquete)
        @staticmethod
        def calculate_paddle_bounce(ball_x: float, paddle_x: float, paddle_width: float, max_bounce_angle: float = 1.047):
            # calcula a distancia do centro para saber o angulo do quique
            dist_from_center = ball_x - paddle_x
            normalized_dist = max(-1.0, min(1.0, dist_from_center / (paddle_width / 2)))
            bounce_angle = normalized_dist * max_bounce_angle
            
            # converte o angulo em vetores x e y usando trigonometria
            new_dx = math.sin(bounce_angle) * 0.707
            new_dy = -abs(math.cos(bounce_angle) * 0.707)

            return new_dx, new_dy

        # DETECCAO DE COLISAO (AABB)
        @staticmethod
        def is_aabb_collision(x1: float, y1: float, w1: float, h1: float, x2: float, y2: float, w2: float, h2: float) -> bool:
            return (x1 + w1/2 >= x2 - w2/2 and
                    x1 - w1/2 <= x2 + w2/2 and
                    y1 + h1/2 >= y2 - h2/2 and
                    y1 - h1/2 <= y2 + h2/2)

        # COLISAO COM AS PAREDES E TETO
        @staticmethod
        def resolve_wall_collision(ball_x: float, ball_y: float, ball_w: float, ball_h: float, ball_dx: float, ball_dy: float, court_left: float, court_right: float, court_top: float):
            hit = False
            ball_top = court_top + ball_h / 2
            ball_left = court_left + ball_w / 2
            ball_right = court_right - ball_w / 2

            if ball_y < ball_top:
                ball_y = ball_top + (ball_top - ball_y)
                ball_dy = -ball_dy
                hit = True

            if ball_x < ball_left:
                ball_x = ball_left + (ball_left - ball_x)
                ball_dx = -ball_dx
                hit = True
            elif ball_x > ball_right:
                ball_x = ball_right - (ball_x - ball_right)
                ball_dx = -ball_dx
                hit = True

            return ball_x, ball_y, ball_dx, ball_dy, hit
