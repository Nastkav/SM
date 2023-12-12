import numpy as np

from element import Element


class Create(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def out_act(self):
        super().out_act()
        self.next_type_element = np.random.choice([1, 2, 3], p=[0.5, 0.1, 0.4])
        self.t_next[0] = self.t_curr + super().get_delay_for_type_create()
        next_element = self.choose_next_element()
        next_element.in_act(self.next_type_element, self.t_curr)
