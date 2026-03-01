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

        # Frames por "tipo" de bloco.
        BLOCK_SPRITES = {
            "red": [
                "images/blocks/small/block_small_red_00.png",
                "images/blocks/small/block_small_red_01.png",
                "images/blocks/small/block_small_red_02.png",
                "images/blocks/small/block_small_red_03.png",
                "images/blocks/small/block_small_red_04.png",
                "images/blocks/small/block_small_red_05.png",
            ],
            "blue": [
                "images/blocks/small/block_small_blue_00.png",
                "images/blocks/small/block_small_blue_01.png",
                "images/blocks/small/block_small_blue_02.png",
                "images/blocks/small/block_small_blue_03.png",
                "images/blocks/small/block_small_blue_04.png",
                "images/blocks/small/block_small_blue_05.png",
            ],
        }

        ROW_TYPES = ["blue", "blue", "red", "red"]
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
