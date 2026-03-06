init python:

    class BlockBase:
        
        WIDTH = 32
        HEIGHT = 16
        HP = 1
        
        POINTS_HIT = 1
        POINTS_DESTROY = 5
        DROP_CHANCE = 0.1

        BLOCK_FPS = 8
        ANIM_DELAY = 3.0

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
            self.hp -= 1
            destroyed = not self.active
            points = self.POINTS_DESTROY if destroyed else self.POINTS_HIT
            return destroyed, points

        def get_frames(self):
            return self._frames[self.color]

        def render(self, r, width, height, st, at):
            frames = self.get_frames()
            num_frames = len(frames)
            
            anim_duration = num_frames / float(self.BLOCK_FPS)
            
            cycle = anim_duration + self.ANIM_DELAY
            t = st % cycle
            
            if t < anim_duration:
                frame_index = int(t * self.BLOCK_FPS)
                frame_index = min(frame_index, num_frames - 1)
            else:
                frame_index = num_frames - 1

            surf = frames[frame_index]
            rendered = renpy.render(surf, self.WIDTH, self.HEIGHT, st, at)
            r.blit(rendered, (int(self.x), int(self.y)))
