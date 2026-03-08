# Define a screen principal do minigame Breakout.
# Responsavel por montar a cena do jogo: fundo, quadra e
# a instância do GameDisplayable alem de elementos de
# sobreposicao como mensagens e HUD futuro
screen game_screen():
    
    default game = GameDisplayable()

    add "#090070"

    add Solid("#d3e2ff"):
        xalign 0.5
        yalign 0.5
        xysize (640, 1080)

    add game

    if game.stuck:
        text "Click to begin":
            xalign 0.5
            ypos 540
            size 40

    add "images/heart/heart_0[game.lives].png":
        xalign 0.5
        yalign 0
        xoffset -350
        yoffset 10

    text "Time: [game.formatted_time]":
        xpos 0.5
        xanchor 0
        yalign 0
        xoffset 350
        yoffset 10

    text "Score: [game.score]":
        xpos 0.5
        xanchor 0
        yalign 0
        xoffset 350
        yoffset 60
    
    # projeteis
    vbox:
        xalign 0.05
        yalign 0.95
        spacing 10
        
        hbox:
            spacing 10
            add "images/projectiles/projectile_basic_00.png" zoom 0.5
            text "Z: [game.arsenal.ammo_basic]" size 30
            
        hbox:
            spacing 10
            add "images/projectiles/projectile_piercing_00.png" zoom 0.5
            text "X: [game.arsenal.ammo_piercing]" size 30
