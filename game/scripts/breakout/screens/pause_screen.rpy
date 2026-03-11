screen pause_screen():

    tag menu
    
    modal True
    
    add Solid("#000000CC")
    
    text "PAUSED" size 80 color "#FFD700" xalign 0.5 yalign 0.35 at title_tremble
    
    vbox:
        xalign 0.5
        yalign 0.6 
        spacing 40
        
        textbutton "Resume":
            xalign 0.5
            text_size 40
            text_hover_color "#33FF33"
            action Return()
            
        textbutton "Main Menu":
            xalign 0.5
            text_size 40
            text_hover_color "#FF3333"
            action MainMenu()
