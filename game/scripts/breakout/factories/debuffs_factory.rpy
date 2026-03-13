# responsavel por instanciar e sortear os debuffs
init 1 python:

    import random

    class DebuffsFactory:        

        CATALOG = {
            "decrease_size":
            {
                "class": DebuffDecreaseSize,
                "active": True
            }
        }

        @classmethod
        def get_random_debuff(cls, x: float, y: float):
            active_list = [data["class"] for key, data in cls.CATALOG.items() if data["active"]]
            
            if not active_list:
                return None
            
            chosen_debuff = random.choice(active_list)
            return chosen_debuff(x, y)
            
        @classmethod
        def set_active(cls, debuff_name: str, is_active: bool) -> None:
            if debuff_name in cls.CATALOG:
                cls.CATALOG[debuff_name]["active"] = is_active
