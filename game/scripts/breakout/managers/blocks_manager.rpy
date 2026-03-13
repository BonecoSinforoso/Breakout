# gerenciador da vida dos blocos na tela e checagem de regras de jogo
# TODO: blocos com diferente numero de spawn por linha
# TODO: contagem automatica de linhas/colunas (baseado no foi colocado no level_maps)
init 1 python:

    import random

    class BlocksManager:

        def __init__(self, court_left: float, court_top: float, level: int = 1) -> None:
            self.blocks = BlocksFactory.generate_level(level, court_left, court_top)
                
        def all_destroyed(self) -> bool:
            return all(not b.active for b in self.blocks)

        def get_all_frames(self) -> list:
            result = []
            for b in self.blocks:
                for frames in b._frames.values():
                    result.extend(frames)
            return result

        def check_collision(self, ball_x: float, ball_y: float, ball_w: float, ball_h: float, ball_dx: float, ball_dy: float, is_fireball: bool = False, is_giantball: bool = False):
            score = 0
            spawned_powerups = []
            hit_occurred = False

            collisions = []

            # busca todos os blocos proximos primeiro
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
                    new_pu = PowerUpsFactory.get_random_powerup(block.x + block.WIDTH/2, block.y + block.HEIGHT/2)
                    if new_pu is not None:
                        spawned_powerups.append(new_pu)

                if not hit_occurred:
                    hit_occurred = True
                    
                    if not is_fireball:
                        ball_x, ball_y, ball_dx, ball_dy = Physics.resolve_aabb_bounce(
                            ball_x, ball_y, ball_w, ball_h, ball_dx, ball_dy, col["dx"], col["dy"]
                        )

                if not is_fireball:
                    break

            return ball_x, ball_y, ball_dx, ball_dy, score, spawned_powerups

        def render(self, r, width: int, height: int, st: float, at: float) -> None:
            for block in self.blocks:
                if not block.active:
                    continue
                block.render(r, width, height, st, at)
