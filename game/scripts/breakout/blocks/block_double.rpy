init python:

    class BlockDouble(BlockBase):
        
        WIDTH = 32
        HEIGHT = 16
        HP = 2

        POINTS_HIT = 4
        POINTS_DESTROY = 8
        DROP_CHANCE = 0.3

        COLORS = [
            "blue", "brown", "cyan", "gray", "green", "orange", "pink", "red", "shocking", "yellow",
        ]

        BLOCK_SPRITES = {
            color: [
                "images/blocks/double/block_double_{}_{:02d}.png".format(color, i)
                for i in range(2)
            ]

            for color in COLORS
        }

        def render(self, r, width, height, st, at):
            frame_index = self.hp - 1
            surf = self.get_frames()[frame_index]
            rendered = renpy.render(surf, self.WIDTH, self.HEIGHT, st, at)
            r.blit(rendered, (int(self.x), int(self.y)))
