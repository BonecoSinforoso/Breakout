# breakout_block_small.rpy
init python:

    class BlockSmall(BlockBase):
        WIDTH = 32
        HEIGHT = 16
        HP = 1

        COLORS = [
            "blue", "brown", "cyan", "gray", "green", "orange", "pink", "red", "shocking", "yellow",
        ]

        BLOCK_SPRITES = {
            color: [
                "images/blocks/small/block_small_{}_{:02d}.png".format(color, i)
                for i in range(6)
            ]
            
            for color in COLORS
        }
