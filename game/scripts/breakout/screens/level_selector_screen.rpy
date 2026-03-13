screen level_selector_screen():

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

        for level in range(1, 4):
            vbox:
                spacing 15
                xalign 0.5

                text "STAGE [level]" size 40 xalign 0.5

                button:
                    action [SetVariable("current_level", level), Return()]
                    
                    hovered SetScreenVariable("hovered_level", level)
                    unhovered SetScreenVariable("hovered_level", 0)
                    hover_sound "audio/ui/hover.flac" 
                    
                    frame:
                        background Solid("#111111CC")
                        xysize (250, 300)
                        padding (15, 15)
                        
                        vbox:
                            xalign 0.5
                            yalign 0.0
                            
                            spacing BlocksFactory.BLOCK_PADDING
                            
                            at transform:
                                zoom 0.35
                            
                            $ map_level = BlocksFactory.LEVEL_MAPS[level]
                            
                            for row in range(BlocksFactory.BLOCK_ROWS):
                                $ b_class, b_color, b_hex = map_level[row % len(map_level)]
                                hbox:
                                    spacing BlocksFactory.BLOCK_PADDING
                                    xalign 0.5
                                    
                                    for col in range(BlocksFactory.BLOCK_COLS):
                                        add Solid(b_hex):
                                            xysize (b_class.WIDTH, b_class.HEIGHT)

                fixed:
                    xysize (250, 40)
                    xalign 0.5
                    
                    if hovered_level == level:
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
        hover_sound "audio/ui/hover.flac"
