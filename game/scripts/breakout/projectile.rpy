# classe do projetil base
init 1 python:

    class Projectile:
        
        ANIM_FPS = 4

        def __init__(self, x: float, y: float, speed: float, is_piercing: bool, frames_list: list) -> None:
            self.x = x
            self.y = y
            self.speed = speed
            self.is_piercing = is_piercing
            self.frames = [Image(f) for f in frames_list]
            
            self.width = 16
            self.height = 16

        def update(self, delta_time: float) -> None:
            self.y -= self.speed * delta_time

        def render(self, r, width: int, height: int, st: float, at: float) -> None:
            num_frames = len(self.frames)
            duration = num_frames / float(self.ANIM_FPS)
            t = st % duration
            frame_index = int(t * self.ANIM_FPS)
            frame_index = min(frame_index, num_frames - 1)

            surf = self.frames[frame_index]
                        
            img = renpy.render(surf, self.width, self.height, st, at)
            r.blit(img, (int(self.x - self.width / 2), int(self.y - self.height / 2)))