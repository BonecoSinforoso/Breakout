# TODO mudar nome para BlocksManager
# Gerencia o grid de blocos. Os tipos de bloco ficam em seus proprios arquivos.
init python:

    import random

    class BlocksManager:

        BLOCK_COLS = 8
        BLOCK_ROWS = 4
        BLOCK_PADDING = 2
        BLOCK_OFFSET_Y = 2

        # Mapa: linha -> classe do bloco
        # Altere aqui para mudar quais tipos aparecem em cada linha
        ROW_BLOCK_TYPES = {
            0: (BlockSmall, "blue"),
            1: (BlockSmall, "brown"),
            2: (BlockSmall, "gray"),
            3: (BlockSmall, "red"),
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
            y = self.court_top + self.BLOCK_OFFSET_Y

            for row in range(self.BLOCK_ROWS):
                block_class, color = self.ROW_BLOCK_TYPES[row % len(self.ROW_BLOCK_TYPES)]
                bw = block_class.WIDTH
                bh = block_class.HEIGHT

                total_w = self.BLOCK_COLS * (bw + self.BLOCK_PADDING) - self.BLOCK_PADDING
                start_x = self.court_left + (640 - total_w) / 2

                for col in range(self.BLOCK_COLS):
                    x = start_x + col * (bw + self.BLOCK_PADDING)
                    self.blocks.append(block_class(x, y, color))

                y += bh + self.BLOCK_PADDING  # avança pelo bh REAL da linha atual

        def all_destroyed(self):
            return all(not b.active for b in self.blocks)

        def get_all_frames(self):
            result = []

            for b in self.blocks:
                for frames in b._frames.values():
                    result.extend(frames)

            return result

        def check_collision(self, ball_x, ball_y, ball_w, ball_h, ball_dx, ball_dy):
            score = 0
            hit_occurred = False
            spawned_powerups = []

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
                    destroyed, points = block.hit()
                    renpy.sound.play("breakout_ball_collision.wav", channel=0)
                    score += points
                    
                    if destroyed and random.random() < block.DROP_CHANCE:
                        new_pu = PowerUpsManager.get_random_drop(block.x + block.WIDTH/2, block.y + block.HEIGHT/2)
                        
                        if new_pu is not None:
                            spawned_powerups.append(new_pu)

                    if not hit_occurred:
                        hit_occurred = True
                        overlap_x = (ball_w / 2) - abs(dist_x)
                        overlap_y = (ball_h / 2) - abs(dist_y)

                        if overlap_x < overlap_y:
                            ball_dx = -ball_dx
                        else:
                            ball_dy = -ball_dy

                    break

            return ball_dx, ball_dy, score, spawned_powerups


        def render(self, r, width, height, st, at):
            for block in self.blocks:
                if not block.active:
                    continue
                block.render(r, width, height, st, at)
