init python:

    class Paddle:

        def __init__(self, x):
            
            self.x = x
            self.y = PADDLE_Y
                        
            self.size_level = 0
            
            self.default_width = 64
            self.default_image = Image("images/paddles/paddle_red_02.png")
            self.height = PADDLE_HEIGHT
                        
            self.width = self.default_width
            self.image = self.default_image
                        
            self.timer_increase_size = 0.0
            self.timer_decrease_size = 0.0

        def _update_sprite(self):
            if self.size_level == -2:
                self.width = 32
                self.image = Image("images/paddles/paddle_red_00.png")
            elif self.size_level == -1:
                self.width = 48
                self.image = Image("images/paddles/paddle_red_01.png")
            elif self.size_level == 0:
                self.width = 64
                self.image = Image("images/paddles/paddle_red_02.png")
            elif self.size_level == 1:
                self.width = 80
                self.image = Image("images/paddles/paddle_red_03.png")
            elif self.size_level == 2:
                self.width = 96
                self.image = Image("images/paddles/paddle_red_04.png")

        # --- ATUALIZAÇÃO POR FRAME ---
        def update(self, delta_time):
            # Conta o tempo do Buff
            if self.timer_increase_size > 0:
                self.timer_increase_size -= delta_time
                if self.timer_increase_size <= 0:
                    self.timer_increase_size = 0
                    self.size_level = 0
                    self._update_sprite()

            # Conta o tempo do Debuff
            if self.timer_decrease_size > 0:
                self.timer_decrease_size -= delta_time
                if self.timer_decrease_size <= 0:
                    self.timer_decrease_size = 0
                    self.size_level = 0
                    self._update_sprite()

        # reseta tudo
        def reset_effects(self):
            self.timer_increase_size = 0
            self.timer_decrease_size = 0
            self.size_level = 0
            self._update_sprite()

        # --- APLICA O BUFF ---
        def increase_size(self, duration=10.0):
            # Se estava encolhido, cancela o debuff e volta ao normal
            if self.timer_decrease_size > 0:
                self.timer_decrease_size = 0
                self.size_level = 0
            else:
                # Aumenta até no máximo o nível 2 (sprite 04)
                self.size_level = min(2, self.size_level + 1)
                self.timer_increase_size = duration
                
            self._update_sprite()

        # --- APLICA O DEBUFF ---
        def decrease_size(self, duration=10.0):
            # Se estava gigante, cancela o buff e volta ao normal
            if self.timer_increase_size > 0:
                self.timer_increase_size = 0
                self.size_level = 0
            else:
                # Diminui até no máximo o nível -2 (sprite 00)
                self.size_level = max(-2, self.size_level - 1)
                self.timer_decrease_size = duration
                
            self._update_sprite()

        def render(self, r, width, height, st, at):
            pi = renpy.render(self.image, width, height, st, at)
            r.blit(pi, (int(self.x - self.width / 2), int(self.y - self.height / 2)))
