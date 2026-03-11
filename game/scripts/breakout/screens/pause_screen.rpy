screen pause_screen():

    tag menu
    
    modal True
    
    add Solid("#000000CC")
    
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 40
        
        text "PAUSED" size 80 color "#FFD700" xalign 0.5 at title_tremble
        
        textbutton "Resume":
            xalign 0.5
            text_size 40
            text_hover_color "#33FF33"
            action Return()
            #hover_sound "audio/hover.flac"
            
        textbutton "Main Menu":
            xalign 0.5
            text_size 40
            text_hover_color "#FF3333"
            action MainMenu()
            #hover_sound "audio/hover.flac"
