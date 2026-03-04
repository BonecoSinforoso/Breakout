# breakout_block_brick.rpy
init python:

    class BlockBrick(BlockBase):
        WIDTH = 64
        HEIGHT = 32
        HP = 5  # um frame por ponto de vida

        POINTS_HIT = 5
        POINTS_DESTROY = 50
        DROP_CHANCE = 0.3

        COLORS = [
            "blue", "brown", "cyan", "gray", "green", "orange", "pink", "red", "shocking", "yellow",
        ]

        BLOCK_SPRITES = {
            color: [
                "images/blocks/brick/block_brick_{}_{:02d}.png".format(color, i)
                for i in range(5)
            ]

            for color in COLORS
        }

        def render(self, r, width, height, st, at):
            frame_index = self.hp - 1
            surf = self.get_frames()[frame_index]
            rendered = renpy.render(surf, self.WIDTH, self.HEIGHT, st, at)
            r.blit(rendered, (int(self.x), int(self.y)))
