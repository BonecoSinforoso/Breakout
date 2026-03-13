init python:

    def spawn_powerup(game, powerup_class):
        new_powerup = powerup_class(game.paddle.x, PADDLE_Y - 150)
        game.powerups_manager.add([new_powerup])

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

    def spawn_debuff(game, debuff_class):
        new_debuff = debuff_class(game.paddle.x, 0)
        game.debuffs_manager.active_debuffs.append(new_debuff)
