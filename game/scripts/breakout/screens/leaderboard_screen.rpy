screen leaderboard_screen():
    
    tag menu

    use game_menu(_("Leaderboard"), scroll=None):

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            text _("Top 10 Scores:") size 40 xalign 0.5

            if not persistent.highscores:
                text _("No scores yet!") xalign 0.5
            else:
                for i, (name, score) in enumerate(persistent.highscores[:10]):
                    hbox:
                        text f"#{i+1} " xalign 0.0
                        text f"{name}: {score}" xalign 0.5
