init python:

    def spawn_cheat_pu(game, pu_class):
        new_pu = pu_class(game.paddle.x, PADDLE_Y - 150)
        game.powerups_manager.add([new_pu])
