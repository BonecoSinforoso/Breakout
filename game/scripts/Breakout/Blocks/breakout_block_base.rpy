# breakout_block_base.rpy
init python:

    class BlockBase:
        WIDTH  = 32
        HEIGHT = 16
        HP     = 1

        BLOCK_FPS      = 8
        ANIM_DURATION  = 1.0
        ANIM_DELAY     = 3.0

        # Subclasses devem preencher: { "color": ["sprite_00.png", ...] }
        BLOCK_SPRITES = {}

        def __init__(self, x, y, color):
            self.x      = x
            self.y      = y
            self.color  = color
            self.hp     = self.HP
            self._frames = {
                key: [Image(p) for p in paths]
                for key, paths in self.BLOCK_SPRITES.items()
            }

        @property
        def active(self):
            return self.hp > 0

        def hit(self):
            """Recebe um hit. Retorna True se o bloco foi destruido."""
            self.hp -= 1
            return not self.active

        def get_frames(self):
            return self._frames[self.color]

        def render(self, r, width, height, st, at):
            cycle = self.ANIM_DURATION + self.ANIM_DELAY
            t = st % cycle
            if t < self.ANIM_DURATION:
                frame_index = int(t * self.BLOCK_FPS) % len(self.get_frames())
            else:
                frame_index = 0

            surf    = self.get_frames()[frame_index]
            rendered = renpy.render(surf, self.WIDTH, self.HEIGHT, st, at)
            r.blit(rendered, (int(self.x), int(self.y)))
