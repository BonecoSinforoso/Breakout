init python:

    class BlockBig(BlockBase):
        
        WIDTH = 32
        HEIGHT = 32
        HP = 1

        DROP_CHANCE = 0.2

        COLORS = [
            "blue", "brown", "cyan", "gray", "green", "orange", "pink", "red", "shocking", "yellow",
        ]

        BLOCK_SPRITES = {
            color: [
                "images/blocks/big/block_big_{}.png".format(color)
            ]
            
            for color in COLORS
        }
