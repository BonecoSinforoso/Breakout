# responsavel por fabricar os projeteis com seus frames e velocidades
init 1 python:

    class ProjectilesFactory:
        
        @staticmethod
        def create_basic(x: float, y: float):
            frames = ["images/projectiles/projectile_basic_{:02d}.png".format(i) for i in range(4)]
            return Projectile(x, y, 500, False, frames)

        @staticmethod
        def create_piercing(x: float, y: float):
            frames = ["images/projectiles/projectile_piercing_{:02d}.png".format(i) for i in range(4)]
            return Projectile(x, y, 600, True, frames)
