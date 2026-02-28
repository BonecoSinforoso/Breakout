init python:

    class PongDisplayable(renpy.Displayable):

        def __init__(self):
            renpy.Displayable.__init__(self)

            ### Constants
            self.PADDLE_WIDTH = 64
            self.PADDLE_HEIGHT = 32
            self.PADDLE_Y = 900

            self.BALL_WIDTH = 15
            self.BALL_HEIGHT = 15

            self.COURT_TOP = 10
            self.COURT_LEFT = 1920 / 2 - 320
            self.COURT_RIGHT = 1920 / 2 + 320

            # Blocos
            self.BLOCK_COLS = 8
            self.BLOCK_ROWS = 4
            self.BLOCK_WIDTH = 70
            self.BLOCK_HEIGHT = 25
            self.BLOCK_PADDING = 5
            self.BLOCK_OFFSET_Y = 80  # distância do topo da quadra

            ### State
            self.paddle = Image("images/paddles/paddle_red_02.png")
            self.ball = Image("images/balls/ball_white.png")

            self.stuck = True
            self.player_x = 1920 / 2

            self.ball_x = self.player_x
            self.ball_y = 0
            self.ball_direction_x = .5
            self.ball_direction_y = -0.5
            self.ball_speed = 500.0

            self.old_st = None
            self.winner = None

            # Inicializa a grade de blocos
            # Cada bloco é um dict: {x, y, active}
            self.blocks = []
            self._init_blocks()

        def _init_blocks(self):
            self.blocks = []
            total_grid_width = self.BLOCK_COLS * (self.BLOCK_WIDTH + self.BLOCK_PADDING) - self.BLOCK_PADDING
            grid_start_x = self.COURT_LEFT + (640 - total_grid_width) / 2

            for row in range(self.BLOCK_ROWS):
                for col in range(self.BLOCK_COLS):
                    bx = grid_start_x + col * (self.BLOCK_WIDTH + self.BLOCK_PADDING)
                    by = self.COURT_TOP + self.BLOCK_OFFSET_Y + row * (self.BLOCK_HEIGHT + self.BLOCK_PADDING)
                    self.blocks.append({"x": bx, "y": by, "active": True})

        def visit(self):
            return [ self.paddle, self.ball ]

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
                self.ball_y = self.PADDLE_Y - 20
            else:
                self.ball_x += self.ball_direction_x * speed
                self.ball_y += self.ball_direction_y * speed

            ball_top = self.COURT_TOP + self.BALL_HEIGHT / 2
            ball_left = self.COURT_LEFT + self.BALL_WIDTH / 2
            ball_right = self.COURT_RIGHT - self.BALL_WIDTH / 2

            if self.ball_y < ball_top:
                self.ball_y = ball_top + (ball_top - self.ball_y)
                self.ball_direction_y = -self.ball_direction_y
                if not self.stuck:
                    renpy.sound.play("pong_beep.opus", channel=0)

            if self.ball_x < ball_left:
                self.ball_x = ball_left + (ball_left - self.ball_x)
                self.ball_direction_x = -self.ball_direction_x
                if not self.stuck:
                    renpy.sound.play("pong_beep.opus", channel=0)

            if self.ball_x > ball_right:
                self.ball_x = ball_right - (self.ball_x - ball_right)
                self.ball_direction_x = -self.ball_direction_x
                if not self.stuck:
                    renpy.sound.play("pong_beep.opus", channel=0)

            # --- Colisão com blocos ---
            for block in self.blocks:
                if not block["active"]:
                    continue

                bx, by = block["x"], block["y"]
                bw, bh = self.BLOCK_WIDTH, self.BLOCK_HEIGHT

                # AABB entre bola (centro) e bloco (rect)
                closest_x = max(bx, min(self.ball_x, bx + bw))
                closest_y = max(by, min(self.ball_y, by + bh))

                dist_x = self.ball_x - closest_x
                dist_y = self.ball_y - closest_y

                if (dist_x ** 2 + dist_y ** 2) <= (self.BALL_WIDTH / 2) ** 2:
                    block["active"] = False
                    renpy.sound.play("pong_beep.opus", channel=0)

                    # Decide qual eixo inverter pelo overlap
                    overlap_x = (self.BALL_WIDTH / 2) - abs(dist_x)
                    overlap_y = (self.BALL_HEIGHT / 2) - abs(dist_y)

                    if overlap_x < overlap_y:
                        self.ball_direction_x = -self.ball_direction_x
                    else:
                        self.ball_direction_y = -self.ball_direction_y

            # --- Renderiza blocos ---
            # Cores por linha
            row_colors = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71"]
            for block in self.blocks:
                if not block["active"]:
                    continue
                row_idx = self.blocks.index(block) // self.BLOCK_COLS
                color = row_colors[row_idx % len(row_colors)]
                block_surf = Solid(color, xsize=int(self.BLOCK_WIDTH), ysize=int(self.BLOCK_HEIGHT))
                block_render = renpy.render(block_surf, width, height, st, at)
                r.blit(block_render, (int(block["x"]), int(block["y"])))

            def paddle_fn(position_x, position_y, hotside):
                pi = renpy.render(self.paddle, width, height, st, at)
                r.blit(pi, (int(position_x - self.PADDLE_WIDTH / 2), int(position_y - self.PADDLE_HEIGHT / 2)))

                if position_x - self.PADDLE_WIDTH / 2 <= self.ball_x <= position_x + self.PADDLE_WIDTH / 2:
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
                        renpy.sound.play("pong_boop.opus", channel=1)
                        self.ball_speed *= 1.10

            paddle_fn(self.player_x, self.PADDLE_Y, self.PADDLE_Y - self.PADDLE_HEIGHT / 2)

            ball = renpy.render(self.ball, width, height, st, at)
            r.blit(ball, (int(self.ball_x - self.BALL_WIDTH / 2), int(self.ball_y - self.BALL_HEIGHT / 2)))

            # fim de jogo
            if self.ball_y > 1080:
                self.winner = "eileen"
                renpy.timeout(0)
            elif all(not b["active"] for b in self.blocks):
                self.winner = "player"
                renpy.timeout(0)

            renpy.redraw(self, 0)
            return r

        def event(self, ev, x, y, st):
            import pygame

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.stuck = False

            renpy.restart_interaction()

            x = max(x, self.COURT_LEFT)
            x = min(x, self.COURT_RIGHT)
            self.player_x = x

            if self.winner:
                return self.winner
            else:
                raise renpy.IgnoreEvent()


screen pong():
    default pong = PongDisplayable()

    add "#090070"

    add Solid("#d3e2ff"):
        xalign 0.5
        yalign 0.5
        xysize (640, 1080)

    add pong

    if pong.stuck:
        text "Click to begin":
            xalign 0.5
            ypos 50
            size 40


label play_pong:
    window hide
    $ quick_menu = False

    call screen pong

    $ quick_menu = True
    window show

    if _return == "eileen":
        "I win!"
    else:
        "You win! Congratulations."

    menu:
        "Play again?"
        "Yes.":
            jump play_pong
        "No.":
            jump after_pong

    return
