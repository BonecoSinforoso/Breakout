init python:

    class PongDisplayable(renpy.Displayable):

        def __init__(self):
            renpy.Displayable.__init__(self)

            self.PADDLE_WIDTH = 12
            self.PADDLE_HEIGHT = 95
            self.PADDLE_X = 240
            self.BALL_WIDTH = 15
            self.BALL_HEIGHT = 15
            self.COURT_TOP = 129
            self.COURT_BOTTOM = 650

            self.paddle = Image("images/paddles/paddle_red_02.png")
            self.ball = Image("images/balls/ball_white.png")

            self.stuck = True
            self.player_y = (self.COURT_BOTTOM - self.COURT_TOP) / 2
            self.computer_y = self.player_y
            self.computer_speed = 380.0

            self.ball_x = self.PADDLE_X + self.PADDLE_WIDTH + 10
            self.ball_y = self.player_y
            self.bdx = .5
            self.bdy = .5
            self.ball_speed = 1000.0

            self.oldst = None
            self.winner = None

        def visit(self):
            return [ self.paddle, self.ball ]

        def render(self, width, height, st, at):
            r = renpy.Render(width, height)

            if self.oldst is None:
                self.oldst = st

            dtime = st - self.oldst
            self.oldst = st

            speed = dtime * self.ball_speed
            oldbx = self.ball_x

            if self.stuck:
                self.ball_y = self.player_y
            else:
                self.ball_x += self.bdx * speed
                self.ball_y += self.bdy * speed

            cspeed = self.computer_speed * dtime

            if abs(self.ball_y - self.computer_y) <= cspeed:
                self.computer_y = self.ball_y
            else:
                self.computer_y += cspeed * (self.ball_y - self.computer_y) / abs(self.ball_y - self.computer_y)

            ball_top = self.COURT_TOP + self.BALL_HEIGHT / 2

            if self.ball_y < ball_top:
                self.ball_y = ball_top + (ball_top - self.ball_y)
                self.bdy = -self.bdy
                if not self.stuck:
                    renpy.sound.play("pong_beep.opus", channel=0)

            ball_bot = self.COURT_BOTTOM - self.BALL_HEIGHT / 2

            if self.ball_y > ball_bot:
                self.ball_y = ball_bot - (self.ball_y - ball_bot)
                self.bdy = -self.bdy
                if not self.stuck:
                    renpy.sound.play("pong_beep.opus", channel=0)

            def paddle(px, py, hotside):
                pi = renpy.render(self.paddle, width, height, st, at)
                r.blit(pi, (int(px), int(py - self.PADDLE_HEIGHT / 2)))

                if py - self.PADDLE_HEIGHT / 2 <= self.ball_y <= py + self.PADDLE_HEIGHT / 2:
                    
                    hit = False

                    if oldbx >= hotside >= self.ball_x:
                        self.ball_x = hotside + (hotside - self.ball_x)
                        self.bdx = -self.bdx
                        hit = True
                    elif oldbx <= hotside <= self.ball_x:
                        self.ball_x = hotside - (self.ball_x - hotside)
                        self.bdx = -self.bdx
                        hit = True
                    if hit:
                        renpy.sound.play("pong_boop.opus", channel=1)
                        self.ball_speed *= 1.10

            paddle(self.PADDLE_X, self.player_y, self.PADDLE_X + self.PADDLE_WIDTH)
            paddle(width - self.PADDLE_X - self.PADDLE_WIDTH, self.computer_y, width - self.PADDLE_X - self.PADDLE_WIDTH)

            ball = renpy.render(self.ball, width, height, st, at)
            r.blit(ball, (int(self.ball_x - self.BALL_WIDTH / 2), int(self.ball_y - self.BALL_HEIGHT / 2)))

            if self.ball_x < -50:
                self.winner = "eileen"
                renpy.timeout(0)
            elif self.ball_x > width + 50:
                self.winner = "player"
                renpy.timeout(0)

            renpy.redraw(self, 0)
            return r

        def event(self, ev, x, y, st):
            
            import pygame

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.stuck = False

            renpy.restart_interaction()

            y = max(y, self.COURT_TOP)
            y = min(y, self.COURT_BOTTOM)
            
            self.player_y = y

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
