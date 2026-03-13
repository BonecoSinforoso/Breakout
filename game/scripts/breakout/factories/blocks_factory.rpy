# responsavel por ler o mapa do level e instanciar o grid de blocos
init 1 python:

    class BlocksFactory:

        BLOCK_COLS = 9
        BLOCK_ROWS = 5
        BLOCK_PADDING = 2
        BLOCK_OFFSET_Y = 2

        # configuracao das fases
        LEVEL_MAPS = {
            1: {
                0: (BlockBrick, "blue", "#2A52BE"),
                1: (BlockTriple, "gray", "#808080"),
                2: (BlockDouble, "brown", "#8B4513"),
                3: (BlockBig, "red", "#FF0000"),
                4: (BlockSmall, "yellow", "#FFD700")
            },
            2: {
                0: (BlockTriple, "gray", "#808080"),
                1: (BlockBrick, "blue", "#2A52BE"),
                2: (BlockDouble, "brown", "#8B4513"),
                3: (BlockBig, "red", "#FF0000"),
                4: (BlockTriple, "gray", "#808080")
            },
            3: {
                0: (BlockSmall, "red", "#FF0000"),
                1: (BlockSmall, "yellow", "#FFD700"),
                2: (BlockSmall, "blue", "#2A52BE"),
                3: (BlockSmall, "gray", "#808080"),
                4: (BlockSmall, "brown", "#8B4513")
            }
        }

        @classmethod
        def generate_level(cls, level: int, court_left: float, court_top: float) -> list:
            blocks = []
            y = court_top + cls.BLOCK_OFFSET_Y
            
            # pega o mapa ou o level 1 como fallback
            level_map = cls.LEVEL_MAPS.get(level, cls.LEVEL_MAPS[1])

            for row in range(cls.BLOCK_ROWS):
                block_class, color, hex_color = level_map[row % len(level_map)]
                bw = block_class.WIDTH
                bh = block_class.HEIGHT

                total_w = cls.BLOCK_COLS * (bw + cls.BLOCK_PADDING) - cls.BLOCK_PADDING
                
                # centraliza os blocos na tela
                start_x = court_left + (640 - total_w) / 2

                for col in range(cls.BLOCK_COLS):
                    x = start_x + col * (bw + cls.BLOCK_PADDING)
                    blocks.append(block_class(x, y, color))

                y += bh + cls.BLOCK_PADDING
                
            return blocks
