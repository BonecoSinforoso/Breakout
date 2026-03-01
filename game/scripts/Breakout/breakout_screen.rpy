# Define a screen principal do minigame Breakout.
# Responsável por montar a cena do jogo: fundo, quadra e
# a instância do PongDisplayable — além de elementos de
# sobreposição como mensagens e HUD futuro.
#
# Não contém lógica de jogo. Toda a física e estado
# ficam em breakout_game.rpy via PongDisplayable.
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
            ypos 540
            size 40

    add "images/heart/heart_0[pong.lives].png":
        xalign 0.5
        yalign 0.5
        xoffset -100
        yoffset -200

    text "Score: [pong.score]":
        xalign 0.5
        yalign 0.9
