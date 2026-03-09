screen leaderboard_screen():
    
    tag menu

    use game_menu(_("Leaderboard"), scroll=None):

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            text _("Top 10 Scores:") size 40 xalign 0.5

            null height 30

            if not persistent.highscores:
                text _("No scores yet!") xalign 0.5
            else:
                for i, (name, score) in enumerate(persistent.highscores[:10]):
                    $ text_color = "#FFFFFF"
                    if i == 0:
                        $ text_color = "#FFD700"
                    elif i == 1:
                        $ text_color = "#C0C0C0"
                    elif i == 2:
                        $ text_color = "#CD7F32"

                    hbox:
                        text f"#{i+1} " xalign 0.0 color text_color
                        text f"{name}: {score}" xalign 0.5 color text_color
