import element as e

class Create(e.Element):
    def __init__(self, delay):
        super().__init__(delay)

    def out_act(self):
        super().out_act()
        self.set_tnext(self.get_tcurr() + self.get_delay())
        self.next_element[0].in_act()




