init python:

    import pygame

    class Debugger:
        
        def handle_input(self, ev, game):
            if ev.type == pygame.KEYDOWN:
                # Q: forca derrota
                if ev.key == pygame.K_q:
                    game.lives = 0
                    game.balls.clear()
                
                # W: forca vitoria
                elif ev.key == pygame.K_w:
                    for block in game.block_grid.blocks:
                        while block.active:
                            destroyed, points = block.hit()
                            game.score += points
                    store.player_score = game.score