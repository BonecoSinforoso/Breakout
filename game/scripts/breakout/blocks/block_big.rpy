init python:

    class BlockBig(BlockBase):
        
        WIDTH = 32
        HEIGHT = 32
        HP = 1

        POINTS_HIT = 10
        POINTS_DESTROY = 20
        DROP_CHANCE = 1

        COLORS = [
            "blue", "brown", "cyan", "gray", "green", "orange", "pink", "red", "shocking", "yellow",
        ]

        BLOCK_SPRITES = {
            color: [
                "images/blocks/big/block_big_{}.png".format(color)
            ]
            
            for color in COLORS
        }
