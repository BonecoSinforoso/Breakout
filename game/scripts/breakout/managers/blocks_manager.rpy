# TODO: separar fabric do manager
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
            map_do_nivel = self.LEVEL_MAPS[self.current_level]
            block_class, color, hex_color = map_do_nivel[row % len(map_do_nivel)]
            return block_class(x, y, color)

        def reset(self):
            self.blocks = []
            y = self.court_top + self.BLOCK_OFFSET_Y
            map_do_nivel = self.LEVEL_MAPS[self.current_level] # Pega o mapa atual

            for row in range(self.BLOCK_ROWS):
                block_class, color, hex_color = map_do_nivel[row % len(map_do_nivel)]
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
                            overlap_x = (ball_w / 2) - abs(dist_x)
                            overlap_y = (ball_h / 2) - abs(dist_y)

                            if overlap_x < overlap_y:
                                if dist_x > 0:
                                    ball_dx = abs(ball_dx)
                                    ball_x += overlap_x + 1
                                else:
                                    ball_dx = -abs(ball_dx)
                                    ball_x -= overlap_x + 1
                            else:                                
                                if dist_y > 0:
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
