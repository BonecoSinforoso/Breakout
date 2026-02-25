init python:

    class PongDisplayable(renpy.Displayable):

        def __init__(self):
            renpy.Displayable.__init__(self)

            ### Constants
            self.PADDLE_WIDTH = 64
            self.PADDLE_HEIGHT = 32
            self.PADDLE_Y = 500

            self.BALL_WIDTH = 15
            self.BALL_HEIGHT = 15
            
            self.COURT_TOP = 10
            self.COURT_LEFT = 1920 / 2 - 320
            self.COURT_RIGHT = 1920 / 2 + 320

            ### State
            self.paddle = Image("images/paddles/paddle_red_02.png")
            self.ball = Image("images/balls/ball_white.png")

            self.stuck = True
            self.player_x = 1920 / 2

            self.ball_x = self.player_x
            self.ball_y = self.PADDLE_Y - 10
            self.ball_direction_x = .5
            self.ball_direction_y = -0.5
            self.ball_speed = 1000.0

            self.old_st = None
            self.winner = None

        def visit(self):
            return [ self.paddle, self.ball ]

        def render(self, width, height, st, at):
            r = renpy.Render(width, height)

            if self.old_st is None:
                self.old_st = st

            delta_time = st - self.old_st
            self.old_st = st

            speed = delta_time * self.ball_speed
            old_ball_x = self.ball_x

            if self.stuck:
                self.ball_x = self.player_x
                self.ball_y = self.PADDLE_Y - 10
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

            def paddle(position_x, position_y, hotside):
                
                pi = renpy.render(self.paddle, width, height, st, at)
                r.blit(pi, (int(position_x), int(position_y - self.PADDLE_HEIGHT / 2)))

                if position_y - self.PADDLE_HEIGHT / 2 <= self.ball_y <= position_y + self.PADDLE_HEIGHT / 2:
                    
                    hit = False

                    if old_ball_x >= hotside >= self.ball_x:
                        self.ball_x = hotside + (hotside - self.ball_x)
                        self.ball_direction_x = -self.ball_direction_x
                        hit = True
                    elif old_ball_x <= hotside <= self.ball_x:
                        self.ball_x = hotside - (self.ball_x - hotside)
                        self.ball_direction_x = -self.ball_direction_x
                        hit = True
                    if hit:
                        renpy.sound.play("pong_boop.opus", channel=1)
                        self.ball_speed *= 1.10

            paddle(self.player_x, self.PADDLE_Y, self.PADDLE_Y - self.PADDLE_HEIGHT)

            ball = renpy.render(self.ball, width, height, st, at)
            r.blit(ball, (int(self.ball_x - self.BALL_WIDTH / 2), int(self.ball_y - self.BALL_HEIGHT / 2)))

            if self.ball_y > 1080:
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

            x = max (x, self.COURT_LEFT)
            x = min (x, self.COURT_RIGHT)
            
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
