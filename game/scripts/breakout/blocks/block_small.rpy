init python:

    class BlockSmall(BlockBase):
        
        WIDTH = 32
        HEIGHT = 16
        HP = 1

        POINTS_HIT = 5
        POINTS_DESTROY = 10
        DROP_CHANCE = 0.2

        ANIM_DELAY = 0.0

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
