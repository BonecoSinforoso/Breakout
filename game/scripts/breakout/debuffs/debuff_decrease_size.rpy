init 1 python:

    class DebuffDecreaseSize(Debuff):
    
        SPRITES = [
            "images/debuffs/debuff_decrease_size_00.png", 
            "images/debuffs/debuff_decrease_size_01.png" 
        ]

        def render(self, r, width, height, st, at):
            frame_index = int(st * self.FPS) % len(self.frames) 
            surf = self.frames[frame_index] 
            
            rendered = renpy.render(surf, width, height, st, at)
            r.blit(rendered, (int(self.x - self.WIDTH / 2), int(self.y - self.HEIGHT / 2)))

        def apply_effect(self, game):
            game.paddle.decrease_size()
