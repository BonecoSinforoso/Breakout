# responsavel apenas pelos calculos matematicos puros de colisao e repulsao vetorial
init 1 python:

    class Physics:
        
        @staticmethod
        def resolve_aabb_bounce(ball_x: float, ball_y: float, ball_w: float, ball_h: float, ball_dx: float, ball_dy: float, col_dx: float, col_dy: float):
            # calcula o overlap da hitbox
            overlap_x = (ball_w / 2) - abs(col_dx)
            overlap_y = (ball_h / 2) - abs(col_dy)

            # inverte o vetor correto baseado em qual lado bateu
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
