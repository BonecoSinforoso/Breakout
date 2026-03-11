# TODO: separar fabric do manager
# TODO: blocos com diferente numero de spawn por linha
# TODO: contagem automatica de linhas/colunas (baseado no foi colocado no level_maps)
init python:

    import random

    class BlocksManager:

        BLOCK_COLS = 9
        BLOCK_ROWS = 5
        BLOCK_PADDING = 2
        BLOCK_OFFSET_Y = 2

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

        def __init__(self, court_left, court_top, level=1):
            self.court_left = court_left
            self.court_top  = court_top
            self.current_level = level
            self.blocks = []
            self.reset()

        def _make_block(self, row, col, x, y):
            level_map = self.LEVEL_MAPS[self.current_level]
            block_class, color, hex_color = level_map[row % len(level_map)]
            return block_class(x, y, color)

        def reset(self):
            self.blocks = []
            y = self.court_top + self.BLOCK_OFFSET_Y
            level_map = self.LEVEL_MAPS[self.current_level]

            for row in range(self.BLOCK_ROWS):
                block_class, color, hex_color = level_map[row % len(level_map)]
                bw = block_class.WIDTH
                bh = block_class.HEIGHT

                total_w = self.BLOCK_COLS * (bw + self.BLOCK_PADDING) - self.BLOCK_PADDING
                start_x = self.court_left + (640 - total_w) / 2

                for col in range(self.BLOCK_COLS):
                    x = start_x + col * (bw + self.BLOCK_PADDING)
                    self.blocks.append(block_class(x, y, color))

                y += bh + self.BLOCK_PADDING
                
        def all_destroyed(self):
            return all(not b.active for b in self.blocks)

        def get_all_frames(self):
            result = []

            for b in self.blocks:
                for frames in b._frames.values():
                    result.extend(frames)

            return result

        def check_collision(self, ball_x, ball_y, ball_w, ball_h, ball_dx, ball_dy, is_fireball=False, is_giantball=False):
            score = 0
            spawned_powerups = []
            hit_occurred = False

            collisions = []

            for block in self.blocks:
                if not block.active:
                    continue

                bx, by = block.x, block.y
                bw, bh = block.WIDTH, block.HEIGHT

                closest_x = max(bx, min(ball_x, bx + bw))
                closest_y = max(by, min(ball_y, by + bh))

                dist_x = ball_x - closest_x
                dist_y = ball_y - closest_y
                sq_dist = dist_x ** 2 + dist_y ** 2

                if sq_dist <= (ball_w / 2) ** 2:
                    collisions.append({
                        "block": block,
                        "dist": sq_dist,
                        "dx": dist_x,
                        "dy": dist_y
                    })

            if not collisions:
                return ball_x, ball_y, ball_dx, ball_dy, score, spawned_powerups

            collisions.sort(key=lambda c: c["dist"])

            for col in collisions:
                block = col["block"]
                if not block.active: continue

                damage = 100 if is_fireball or is_giantball else 1
                while damage > 0 and block.active:
                    destroyed, points = block.hit()
                    score += points
                    damage -= 1

                renpy.sound.play("ball_collision.wav", channel=0)

                if destroyed and random.random() < block.DROP_CHANCE:
                    new_pu = PowerUpsManager.get_random_drop(block.x + block.WIDTH/2, block.y + block.HEIGHT/2)
                    if new_pu is not None:
                        spawned_powerups.append(new_pu)

                if not hit_occurred:
                    hit_occurred = True
                    
                    if not is_fireball:
                        overlap_x = (ball_w / 2) - abs(col["dx"])
                        overlap_y = (ball_h / 2) - abs(col["dy"])

                        if overlap_x < overlap_y:
                            if col["dx"] > 0:
                                ball_dx = abs(ball_dx)
                                ball_x += overlap_x + 1
                            else:
                                ball_dx = -abs(ball_dx)
                                ball_x -= overlap_x + 1
                        else:
                            if col["dy"] > 0:
                                ball_dy = abs(ball_dy)
                                ball_y += overlap_y + 1
                            else:
                                ball_dy = -abs(ball_dy)
                                ball_y -= overlap_y + 1

                if not is_fireball:
                    break

            return ball_x, ball_y, ball_dx, ball_dy, score, spawned_powerups


        def render(self, r, width, height, st, at):
            for block in self.blocks:
                if not block.active:
                    continue
                block.render(r, width, height, st, at)
