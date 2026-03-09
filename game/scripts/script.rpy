# TODO: mudar aparencia da Eileen, colocar uma sprite minha
# vai conter as labels

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
        jump play_game


label play_game:

    window hide

    $ quick_menu = False

    call screen game_screen

    $ quick_menu = True
    
    window show

    $ highscores = persistent.highscores + [(player_name, player_score)]
    $ highscores.sort(key=lambda x: x[1], reverse=True)
    $ persistent.highscores = highscores[:10]

    if _return == "eileen":
        "You lose."
        "[player_name] you scored [player_score] points"
    else:
        "You win! Congratulations!"
        "Block: [player_score - bonus_time - bonus_lives] points!"
        "Time Bonus: [bonus_time] points!"
        "Lives Bonus: [bonus_lives] points!"
        "[player_name] you scored a total of [player_score] points!"

    menu:
        "Would you like to play again?"
        "Yes":
            jump play_game
        "No":
            jump after_game

    return


label after_game:

    eileen "Thanks for playing! I hope you had fun!"

    return
