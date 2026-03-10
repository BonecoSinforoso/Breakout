screen level_selector():

    tag menu
    
    # fundo
    add "rgb_animated_bg"
    add "menu_floating_blocks"

    # titulo
    vbox:
        xalign 0.5
        ypos 80
        text "SELECT STAGE" size 60 color "#FFD700" at title_tremble

    # grade dos niveis
    hbox:
        xalign 0.5
        yalign 0.55
        spacing 60

        for lvl in range(1, 4):
            vbox:
                spacing 15
                xalign 0.5

                text "STAGE [lvl]" size 40 xalign 0.5

                button:
                    action [SetVariable("current_level", lvl), Return()]
                    
                    hovered SetScreenVariable("hovered_level", lvl)
                    unhovered SetScreenVariable("hovered_level", 0)
                    hover_sound "audio/hover.flac" 
                    
                    frame:
                        background Solid("#111111CC")
                        xysize (250, 300)
                        padding (15, 15)
                        
                        vbox:
                            xalign 0.5
                            yalign 0.0
                            spacing BlocksManager.BLOCK_PADDING
                            
                            at transform:
                                zoom 0.35
                            
                            $ map_level = BlocksManager.LEVEL_MAPS[lvl]
                            
                            for row in range(BlocksManager.BLOCK_ROWS):
                                $ b_class, b_color, b_hex = map_level[row % len(map_level)]
                                hbox:
                                    spacing BlocksManager.BLOCK_PADDING
                                    xalign 0.5
                                    for col in range(BlocksManager.BLOCK_COLS):
                                        add Solid(b_hex):
                                            xysize (b_class.WIDTH, b_class.HEIGHT)

                fixed:
                    xysize (250, 40)
                    xalign 0.5
                    
                    if hovered_level == lvl:
                        add "images/paddles/paddle_red_04.png":
                            xalign 0.5
                            yalign 0.5
                            zoom 0.7 

    textbutton "Return to Main Menu":
        xalign 0.5
        yalign 0.95
        text_size 30
        text_hover_color "#FF0000"
        action MainMenu()
        hover_sound "audio/hover.flac"
