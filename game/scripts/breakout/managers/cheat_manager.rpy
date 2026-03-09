init python:

    def spawn_cheat_pu(game, pu_class):
        new_pu = pu_class(game.paddle.x, PADDLE_Y - 150)
        game.powerups_manager.add([new_pu])

    def force_win(game):
        for block in game.blocks_manager.blocks:
            while block.active:
                destroyed, points = block.hit()
                game.score += points
        store.player_score = game.score

    def force_lose(game):
        game.lives = 0
        game.balls_manager.clear()

    def add_1000_points(game):
        game.score += 1000
        store.player_score = game.score
