# TODO: mudar aparencia da Eileen, colocar uma sprite minha
# vai conter as labels e vozes

label start:

    $ renpy.music.set_volume(0.05, delay=2.0, channel='music')

    scene nigh
    
    show eileen happy

    jump ask_name

    hide eileen happy

    return


label ask_name:

    voice "audio/voices/sinfas/what_is_your_name.ogg"
    $ player_name = renpy.input("What is your name?", length = 20)
    $ player_name = player_name.strip()
        
    if player_name == "":
        jump ask_name
    else:
        jump choose_level


label choose_level:

    call screen level_selector_screen
    
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
        show eileen concerned
        voice "audio/voices/sinfas/you_lose.ogg"            
        eileen "You lose."
        
        "[player_name] you scored [player_score] points"

        hide eileen concerned
    else:
        show eileen vhappy

        voice "audio/voices/sinfas/you_win_congratulations.ogg"
        eileen "You win! Congratulations!"
        
        "Destroyed Blocks: [player_score - bonus_time - bonus_lives] points!"
        "Time Bonus: [bonus_time] points!"
        "Lives Bonus: [bonus_lives] points!"
        "[player_name] you scored a total of [player_score] points!"

        hide eileen vhappy

    show eileen happy
    voice "audio/voices/sinfas/would_you_like_to_play_again.ogg" # temq ser aq do contrario nn vai
    eileen "Would you like to play again?"

    menu:        
        "Yes":
            jump choose_level
        "No":
            jump after_game

    return


label after_game:

    voice "audio/voices/sinfas/thanks_for_playing.ogg"
    eileen "Thanks for playing! I hope you had fun!"

    return
