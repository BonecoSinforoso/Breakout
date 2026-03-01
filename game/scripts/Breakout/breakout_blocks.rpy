init python:

    class BreakoutBlocks:

        BLOCK_COLS = 8
        BLOCK_ROWS = 4
        BLOCK_WIDTH = 70
        BLOCK_HEIGHT = 25
        BLOCK_PADDING = 5
        BLOCK_OFFSET_Y = 80
        ROW_COLORS = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71"]

        def __init__(self, court_left, court_top):
            self.court_left = court_left
            self.court_top = court_top
            self.blocks = []
            self.reset()

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
                        "row": row
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
            for block in self.blocks:
                if not block["active"]:
                    continue

                color = self.ROW_COLORS[block["row"] % len(self.ROW_COLORS)]
                surf = Solid(color, xsize=int(self.BLOCK_WIDTH), ysize=int(self.BLOCK_HEIGHT))
                rendered = renpy.render(surf, width, height, st, at)
                r.blit(rendered, (int(block["x"]), int(block["y"])))
