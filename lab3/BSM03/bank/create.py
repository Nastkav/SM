from bank import element as e


class Create(e.Element):
    def __init__(self, delay):
        super().__init__(delay)

    def out_act(self):
        super().out_act()

        self.set_tnext(self.get_tcurr() + self.get_delay())
        p1 = self.next_element[0]
        p2 = self.next_element[1]
        if p1.queue == p2.queue or (p1.queue == 0 and p2.queue == 0) or p1.queue < p2.queue:
            p1.in_act()
        else:
            p2.in_act()

