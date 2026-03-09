screen cheat_screen(game):

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
                                
                textbutton "Force Win":
                    action Function(force_win, game)
                    text_size 20
                    text_hover_color "#33FF33"

                textbutton "Force Lose":
                    action Function(force_lose, game)
                    text_size 20
                    text_hover_color "#FF3333"

                null height 10
                text "--- POWER-UPS ---" color "#33FF33" size 20 bold True
                                
                for key, data in PowerUpsManager.CATALOG.items():
                    $ button_name = key.replace("_", " ").title()
                    
                    textbutton button_name:
                        action Function(spawn_cheat_pu, game, data["class"])
                        text_size 20
                        text_hover_color "#FFFF00"
