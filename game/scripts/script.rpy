# TODO: mudar aparencia da Eileen, colocar uma sprite minha
define eileen = Character("Eileen")
default player_name = ""
default player_score = 0
default persistent.highscores = []

label start:

    scene bg room
    show eileen happy

    jump ask_name    

    return

label ask_name:
    $ player_name = renpy.input("What is your name?", length = 20)
    $ player_name = player_name.strip()
        
    if player_name == "":
        jump ask_name
    else:
        jump play_pong
    
label after_pong:

    eileen "That was fun! I hope you enjoyed it."

    return
