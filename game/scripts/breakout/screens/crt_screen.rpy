# tela do efeito de tv velha
screen crt_screen():

    zorder 1000
    
    if persistent.crt_effect:
        add "gui/crt_scanlines.png" alpha 0.3
