import numpy as np

from hospital.exit import Exit
from hospital.process import Process


class Model:
    def __init__(self, elements: list):
        self.list = elements
        self.event = 0
        self.t_next = 0.0
        self.t_curr = self.t_next
        self.total_mean_interval_between_arriving_to_the_lab = 0

    def simulate(self, time):
        while self.t_curr < time:
            self.t_next = float('inf')
            for e in self.list:
                t_next_val = np.min(e.t_next)
                if t_next_val < self.t_next and not isinstance(e, Exit):
                    self.t_next = t_next_val
                    self.event = e.id_el

            # обраховуємо статистики
            for e in self.list:
                e.calculate(self.t_next - self.t_curr)

            # робимо переміщення до моменту завершення
            self.t_curr = self.t_next
            for e in self.list:
                e.t_curr = self.t_curr

            if len(self.list) > self.event:
                self.list[self.event].out_act()

            for e in self.list:
                if self.t_curr in e.t_next:
                    e.out_act()

            self.print_info()
        return self.print_result()

    def print_info(self):
        for e in self.list:
            e.print_info()

    def print_result(self):
        print("\n-------------RESULTS-------------")
        for e in self.list:
            e.print_result()
            if isinstance(e, Process):
                if e.name == 'TO_THE_LAB':
                    self.total_mean_interval_between_arriving_to_the_lab = e.delta_t_following_to_the_lab_reception / e.quantity
                if e.name == 'TO_THE_RECEPTION_DOCTOR':
                    print()
                    print(f'Mean_time_finish for type 2(next type1) = {e.delta_t_finish_reception / e.count_type2}' if e.count_type2 != 0 else 0)
                    print()

            elif isinstance(e, Exit):
                if e.count_type1 != 0:
                    print(f'Mean_time_finish for type 1 = {e.delta_t_finish1 / e.count_type1}')
                if e.count_type3 != 0:
                    print(f'Mean_time_finish for type 3 = {e.delta_t_finish3 / e.count_type3}')
                print()

        print(
            f'total_mean_interval_between_arriving_to_the_lab = {self.total_mean_interval_between_arriving_to_the_lab}')
        print()
