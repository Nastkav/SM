import numpy as np

from element import Element


class Exit(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.t_next = [np.inf]
        self.delta_t_finish1 = 0
        self.delta_t_finish3 = 0
        self.count_type1 = 0
        self.count_type3 = 0

    def in_act(self, next_type_element, t_start):
        if next_type_element == 1:
            self.delta_t_finish1 += self.t_curr - t_start
            self.count_type1 += 1
        elif next_type_element == 3:
            self.delta_t_finish3 += self.t_curr - t_start
            self.count_type3 += 1
        super().out_act()
