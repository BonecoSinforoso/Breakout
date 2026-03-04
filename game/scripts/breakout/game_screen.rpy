# Define a screen principal do minigame Breakout.
# Responsavel por montar a cena do jogo: fundo, quadra e
# a instância do BreakoutDisplayable — alem de elementos de
# sobreposicao como mensagens e HUD futuro
screen game():
    default breakout = BreakoutDisplayable()

    add "#090070"

    add Solid("#d3e2ff"):
        xalign 0.5
        yalign 0.5
        xysize (640, 1080)

    add breakout

    if breakout.stuck:
        text "Click to begin":
            xalign 0.5
            ypos 540
            size 40

    add "images/heart/heart_0[breakout.lives].png":
        xalign 0.5
        yalign 0
        xoffset -350
        yoffset 10

    text "Score: [breakout.score]":
        xalign 0.5
        yalign 0.9
