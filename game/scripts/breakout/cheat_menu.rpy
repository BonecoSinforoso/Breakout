init python:

    def spawn_cheat_pu(game, pu_class):
        new_pu = pu_class(game.paddle.x, PADDLE_Y - 150)
        game.powerups_manager.add([new_pu])

screen cheat_menu(game):

    zorder 100

    key "c" action ToggleVariable("show_cheats")

    if show_cheats:
        frame:
            align (0.01, 0.5)
            background Solid("#000000CC")
            padding (20, 20)
            
            vbox:
                spacing 10
                text "--- CHEATS ---" color "#33FF33" size 24 bold True
                text "(Aperte 'C' para fechar)" color "#AAAAAA" size 14
                null height 10
                
                for key, data in PowerUpsManager.CATALOG.items():
                    $ button_name = key.replace("_", " ").title()
                    
                    textbutton button_name:
                        action Function(spawn_cheat_pu, game, data["class"])
                        text_size 20
                        text_hover_color "#FFFF00"
