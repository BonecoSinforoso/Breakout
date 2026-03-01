# atualmente responsavel por gerenciar os blocos
# TODO: futuramente, vai acessar os tipos de bloco
init python:

    class BreakoutBlocks:

        BLOCK_COLS = 8
        BLOCK_ROWS = 4
        BLOCK_WIDTH = 32
        BLOCK_HEIGHT = 16
        BLOCK_PADDING = 5
        BLOCK_OFFSET_Y = 5

        BLOCK_FPS = 8
        ANIM_DURATION = 1.0
        ANIM_DELAY = 3.0

        # Frames por cor de bloco pequeno
        BLOCK_SPRITES = {
            "blue": [
                "images/blocks/small/block_small_blue_00.png",
                "images/blocks/small/block_small_blue_01.png",
                "images/blocks/small/block_small_blue_02.png",
                "images/blocks/small/block_small_blue_03.png",
                "images/blocks/small/block_small_blue_04.png",
                "images/blocks/small/block_small_blue_05.png",
            ],
            "brown": [
                "images/blocks/small/block_small_brown_00.png",
                "images/blocks/small/block_small_brown_01.png",
                "images/blocks/small/block_small_brown_02.png",
                "images/blocks/small/block_small_brown_03.png",
                "images/blocks/small/block_small_brown_04.png",
                "images/blocks/small/block_small_brown_05.png",
            ],
            "cyan": [
                "images/blocks/small/block_small_cyan_00.png",
                "images/blocks/small/block_small_cyan_01.png",
                "images/blocks/small/block_small_cyan_02.png",
                "images/blocks/small/block_small_cyan_03.png",
                "images/blocks/small/block_small_cyan_04.png",
                "images/blocks/small/block_small_cyan_05.png",
            ],
            "gray": [
                "images/blocks/small/block_small_gray_00.png",
                "images/blocks/small/block_small_gray_01.png",
                "images/blocks/small/block_small_gray_02.png",
                "images/blocks/small/block_small_gray_03.png",
                "images/blocks/small/block_small_gray_04.png",
                "images/blocks/small/block_small_gray_05.png",
            ],
            "green": [
                "images/blocks/small/block_small_green_00.png",
                "images/blocks/small/block_small_green_01.png",
                "images/blocks/small/block_small_green_02.png",
                "images/blocks/small/block_small_green_03.png",
                "images/blocks/small/block_small_green_04.png",
                "images/blocks/small/block_small_green_05.png",
            ],
            "orange": [
                "images/blocks/small/block_small_orange_00.png",
                "images/blocks/small/block_small_orange_01.png",
                "images/blocks/small/block_small_orange_02.png",
                "images/blocks/small/block_small_orange_03.png",
                "images/blocks/small/block_small_orange_04.png",
                "images/blocks/small/block_small_orange_05.png",
            ],
            "pink": [
                "images/blocks/small/block_small_pink_00.png",
                "images/blocks/small/block_small_pink_01.png",
                "images/blocks/small/block_small_pink_02.png",
                "images/blocks/small/block_small_pink_03.png",
                "images/blocks/small/block_small_pink_04.png",
                "images/blocks/small/block_small_pink_05.png",
            ],
            "red": [
                "images/blocks/small/block_small_red_00.png",
                "images/blocks/small/block_small_red_01.png",
                "images/blocks/small/block_small_red_02.png",
                "images/blocks/small/block_small_red_03.png",
                "images/blocks/small/block_small_red_04.png",
                "images/blocks/small/block_small_red_05.png",
            ],
            "shocking": [
                "images/blocks/small/block_small_shocking_00.png",
                "images/blocks/small/block_small_shocking_01.png",
                "images/blocks/small/block_small_shocking_02.png",
                "images/blocks/small/block_small_shocking_03.png",
                "images/blocks/small/block_small_shocking_04.png",
                "images/blocks/small/block_small_shocking_05.png",
            ],
            "yellow": [
                "images/blocks/small/block_small_yellow_00.png",
                "images/blocks/small/block_small_yellow_01.png",
                "images/blocks/small/block_small_yellow_02.png",
                "images/blocks/small/block_small_yellow_03.png",
                "images/blocks/small/block_small_yellow_04.png",
                "images/blocks/small/block_small_yellow_05.png",
            ],
        }

        ROW_TYPES = ["blue", "brown", "yellow", "green"]
        # COL_TYPES = ["blue", "red", "blue", "red", "blue", "red", "blue", "red"]

        def __init__(self, court_left, court_top):
            self.court_left = court_left
            self.court_top = court_top
            self.blocks = []
            
            self._frames = {
                key: [Image(p) for p in paths]
                for key, paths in self.BLOCK_SPRITES.items()
            }
            self.reset()

        def _get_type(self, row, col):            
            return self.ROW_TYPES[row % len(self.ROW_TYPES)]
            # return self.COL_TYPES[col % len(self.COL_TYPES)]

        def reset(self):
            self.blocks = []
            total_w = self.BLOCK_COLS * (self.BLOCK_WIDTH + self.BLOCK_PADDING) - self.BLOCK_PADDING
            start_x = self.court_left + (640 - total_w) / 2

            for row in range(self.BLOCK_ROWS):
                for col in range(self.BLOCK_COLS):
                    self.blocks.append({
                        "x": start_x + col * (self.BLOCK_WIDTH + self.BLOCK_PADDING),
                        "y": self.court_top + self.BLOCK_OFFSET_Y + row * (self.BLOCK_HEIGHT + self.BLOCK_PADDING),
                        "active": True,
                        "row": row,
                        "col": col,
                        "type": self._get_type(row, col),
                    })

        def all_destroyed(self):
            return all(not b["active"] for b in self.blocks)

        def check_collision(self, ball_x, ball_y, ball_w, ball_h, ball_dx, ball_dy):
            hits = 0

            for block in self.blocks:
                if not block["active"]:
                    continue

                bx, by = block["x"], block["y"]
                bw, bh = self.BLOCK_WIDTH, self.BLOCK_HEIGHT

                closest_x = max(bx, min(ball_x, bx + bw))
                closest_y = max(by, min(ball_y, by + bh))

                dist_x = ball_x - closest_x
                dist_y = ball_y - closest_y

                if (dist_x ** 2 + dist_y ** 2) <= (ball_w / 2) ** 2:
                    block["active"] = False
                    renpy.sound.play("breakout_ball_collision.wav", channel=0)
                    hits += 1

                    overlap_x = (ball_w / 2) - abs(dist_x)
                    overlap_y = (ball_h / 2) - abs(dist_y)

                    if overlap_x < overlap_y:
                        ball_dx = -ball_dx
                    else:
                        ball_dy = -ball_dy

            return ball_dx, ball_dy, hits

        def render(self, r, width, height, st, at):
            cycle = self.ANIM_DURATION + self.ANIM_DELAY
            t = st % cycle

            if t < self.ANIM_DURATION:
                frame_index = int(t * self.BLOCK_FPS) % 6  # 6 = total de frames
            else:
                frame_index = 0

            for block in self.blocks:
                if not block["active"]:
                    continue

                frames = self._frames[block["type"]]
                surf = frames[frame_index % len(frames)]

                rendered = renpy.render(surf, self.BLOCK_WIDTH, self.BLOCK_HEIGHT, st, at)
                r.blit(rendered, (int(block["x"]), int(block["y"])))
