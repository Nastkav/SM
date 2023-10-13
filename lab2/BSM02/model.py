from process import Process
import numpy as np

class Model:
    def __init__(self, elements):
        self.list = elements
        self.t_next = 0.0
        self.event = 0
        self.t_curr = self.t_next

    def simulate(self, time):
        while self.t_curr < time:
            self.t_next = float('inf')

            for e in self.list:
                t_next_val = np.min(e.t_next)
                if t_next_val < self.t_next:
                    self.t_next = t_next_val
                    self.event = e.id

            for e in self.list:
                e.do_statistics(self.t_next - self.t_curr)

            self.t_curr = self.t_next

            for e in self.list:
                e.t_curr = self.t_curr

            if len(self.list) > self.event:
                self.list[self.event].out_act()

            for e in self.list:
                if np.any(self.t_curr == e.t_next):
                    e.out_act()

            self.print_info()

        return self.print_result()

    def print_info(self):
        for e in self.list:
            e.print_info()

    def print_result(self):
        print("\n-------------RESULTS-------------")
        result = list()
        for e in self.list:
            e.print_result()
            result.append(e.get_quantity())
            if isinstance(e, Process):
                p = e
                # task 2
                p.mean_load = e.mean_load / self.t_curr

                print(f"mean length of queue = {str(p.get_mean_queue() / self.t_curr)}")
                print(f"failure probability = {str(p.get_failure() / float(p.get_quantity()))}")
                print(f'mean load = {p.mean_load}')
                print()
                result.append([p.get_mean_queue() / self.t_curr, p.get_failure() / float(p.get_quantity()), p.mean_load])
        return result


