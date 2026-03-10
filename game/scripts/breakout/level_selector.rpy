screen level_selector():

    tag menu
    
    add "rgb_animated_bg"
    add "menu_floating_blocks"

    vbox:
        xalign 0.5
        ypos 80
        text "SELECT STAGE" size 60 color "#FFD700" at title_tremble

    hbox:
        xalign 0.5
        yalign 0.6
        spacing 60

        for lvl in range(1, 4):
            vbox:
                spacing 20
                xalign 0.5

                text "STAGE [lvl]" size 40 xalign 0.5

                button:
                    action [SetVariable("current_level", lvl), Return()]
                    hover_sound "audio/hover.flac" 
                    
                    frame:
                        background Solid("#111111CC")
                        xysize (250, 300)
                        padding (15, 15)
                                                
                        fixed:
                            xalign 0.5
                            yalign 0.5
                            at transform:
                                zoom 0.35
                                
                            vbox:
                                spacing BlocksManager.BLOCK_PADDING
                                xalign 0.5
                                
                                $ map_level = BlocksManager.LEVEL_MAPS[lvl]
                                
                                for row in range(BlocksManager.BLOCK_ROWS):
                                    $ b_class, b_color, b_hex = map_level[row % len(map_level)]
                                    hbox:
                                        spacing BlocksManager.BLOCK_PADDING
                                        xalign 0.5
                                        for col in range(BlocksManager.BLOCK_COLS):
                                            add Solid(b_hex):
                                                xysize (b_class.WIDTH, b_class.HEIGHT)
