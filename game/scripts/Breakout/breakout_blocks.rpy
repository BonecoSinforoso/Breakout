# breakout_blocks.rpy
# Gerencia o grid de blocos. Os tipos de bloco ficam em seus proprios arquivos.
init python:

    class BreakoutBlocks:

        BLOCK_COLS = 8
        BLOCK_ROWS = 4
        BLOCK_PADDING = 5
        BLOCK_OFFSET_Y = 5

        # Mapa: linha -> classe do bloco
        # Altere aqui para mudar quais tipos aparecem em cada linha
        ROW_BLOCK_TYPES = {
            0: (BlockSmall, "blue"),
            1: (BlockSmall, "brown"),
            2: (BlockBrick, "gray"),
            3: (BlockBrick, "red"),
        }

        def __init__(self, court_left, court_top):
            self.court_left = court_left
            self.court_top  = court_top
            self.blocks = []
            self.reset()

        def _make_block(self, row, col, x, y):
            block_class, color = self.ROW_BLOCK_TYPES[row % len(self.ROW_BLOCK_TYPES)]
            return block_class(x, y, color)

        def reset(self):
            self.blocks = []
            # Usa as dimensoes do primeiro tipo de bloco como referencia de grade
            ref_class, _ = self.ROW_BLOCK_TYPES[0]
            bw = ref_class.WIDTH
            bh = ref_class.HEIGHT

            total_w = self.BLOCK_COLS * (bw + self.BLOCK_PADDING) - self.BLOCK_PADDING
            start_x = self.court_left + (640 - total_w) / 2

            for row in range(self.BLOCK_ROWS):
                for col in range(self.BLOCK_COLS):
                    x = start_x + col * (bw + self.BLOCK_PADDING)
                    y = self.court_top + self.BLOCK_OFFSET_Y + row * (bh + self.BLOCK_PADDING)
                    self.blocks.append(self._make_block(row, col, x, y))

        def all_destroyed(self):
            return all(not b.active for b in self.blocks)

        def get_all_frames(self):
            """Usado pelo visit() em PongDisplayable."""
            result = []
            for b in self.blocks:
                for frames in b._frames.values():
                    result.extend(frames)
            return result

        def check_collision(self, ball_x, ball_y, ball_w, ball_h, ball_dx, ball_dy):
            hits = 0

            for block in self.blocks:
                if not block.active:
                    continue

                bx, by = block.x, block.y
                bw, bh = block.WIDTH, block.HEIGHT

                closest_x = max(bx, min(ball_x, bx + bw))
                closest_y = max(by, min(ball_y, by + bh))

                dist_x = ball_x - closest_x
                dist_y = ball_y - closest_y

                if (dist_x ** 2 + dist_y ** 2) <= (ball_w / 2) ** 2:
                    destroyed = block.hit()
                    renpy.sound.play("breakout_ball_collision.wav", channel=0)

                    if destroyed:
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
                if not block.active:
                    continue
                block.render(r, width, height, st, at)
