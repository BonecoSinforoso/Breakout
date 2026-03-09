# gerente dos cheats
# TODO: nome seguindo o padrao nn seria cheatManager?
init python:

    import pygame

    class Debugger:
        
        def handle_input(self, ev, game):
            if ev.type == pygame.KEYDOWN:
                # Q: forca derrota
                if ev.key == pygame.K_q:
                    game.lives = 0
                    game.balls_manager.balls.clear()
                
                # W: forca vitoria
                elif ev.key == pygame.K_w:
                    for block in game.blocks_manager.blocks:
                        while block.active:
                            destroyed, points = block.hit()
                            game.score += points
                    store.player_score = game.score
