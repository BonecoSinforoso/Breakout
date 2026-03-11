init 1 python:

    class DebuffDecreaseSize(Debuff):
    
        SPRITES = [
            "images/debuffs/debuff_decrease_size_00.png", 
            "images/debuffs/debuff_decrease_size_01.png" 
        ]        

        def apply_effect(self, game):
            game.paddle.decrease_size()
