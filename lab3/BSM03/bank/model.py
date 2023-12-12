from process import Process
import numpy as np


class Model:
    def __init__(self, elements, cashiers=None, num=1):
        self.list = elements
        self.t_next = 0.0
        self.event = 0
        self.t_curr = self.t_next
        self.cashiers = cashiers
        self.change_queue = 0
        self.average_client_in_bank = 0
        self.mean_load_cashier = 0
        self.mean_time_client_in_bank = 0.0
        self.mean_time_between_depart = 0.0
        self.num_of_cashiers = num
        self.num_of_p = 0
        self.fail = 0
        self.quantity = 0
        self.quantities = []



    def get_average_client_in_bank(self, delta):
        self.average_client_in_bank += delta * (
                self.cashiers[0].queue + self.cashiers[1].queue + self.cashiers[0].state[0] +
                self.cashiers[1].state[0])

    def check_diff_queues(self):
        queues = list()
        for element in self.list:
            if isinstance(element, Process):
                queues.append(element.queue)
        queue1 = queues[0] - queues[1]
        queue2 = queues[1] - queues[0]
        if queue1 >= 2:
            self.list[1].queue -= 1
            self.list[2].queue += 1
            print("Auto from CASHIER-1 to CASHIER-2")
            self.change_queue += 1
        elif queue2 >= 2:
            self.list[2].queue -= 1
            self.list[1].queue += 1
            print("Auto from CASHIER-2 to CASHIER-1")
            self.change_queue += 1

    # здійснення імітації на інтервалі часу time
    def simulate(self, time):
        # знаходимо найменший з моментів часу
        while self.t_curr < time:
            self.t_next = float('inf')

            for e in self.list:
                t_next_val = np.min(e.t_next)
                if t_next_val < self.t_next:
                    self.t_next = t_next_val
                    self.event = e.id

            for e in self.list:
                e.do_statistics(self.t_next - self.t_curr)
            self.get_average_client_in_bank(self.t_next - self.t_curr)

            # просунутися у часі вперед
            self.t_curr = self.t_next

            # оновити поточний час для кожного елементу
            for e in self.list:
                e.t_curr = self.t_curr

            if len(self.list) > self.event:
                self.list[self.event].out_act()

            for e in self.list:
                if np.any(self.t_curr == e.t_next):
                    e.out_act()

            self.print_info()
            self.check_diff_queues()
        self.print_result()


    def print_info(self):
        for e in self.list:
            e.print_info()

    def print_result(self):
        print("\n-------------RESULTS-------------")
        result = list()
        for e in self.list:
            self.quantities.append(e.print_result())

            if isinstance(e, Process):
                self.num_of_p += 1
                p = e
                # task 2
                p.mean_load = e.mean_load / self.t_curr
                self.mean_time_client_in_bank += e.delta_t_in_bank / e.quantity
                self.mean_time_between_depart += e.delta_t_depart / e.quantity
                self.fail += p.get_failure()
                print(f"(old)mean length of queue = {str(p.get_mean_queue() / self.t_curr)}")
                print(f"(old)failure probability = {str(p.get_failure() / float(p.get_quantity()))}")
                print(f'(old)mean load of cashier = {p.mean_load}')
                print()
                if self.num_of_p == self.num_of_cashiers:
                    print(' TOTAL RESULTS')
                    print(f"number of queue changes = {self.change_queue}")
                    print(f'failure probability = {self.fail/self.quantities[0]}')
                    print(f'mean_time_client_in_bank = {str(self.mean_time_client_in_bank / self.num_of_cashiers)}')
                    print(f'mean_time_between_depart = {str(self.mean_time_between_depart / self.num_of_cashiers)}')
                    print(f"average number of clients in bank = {self.average_client_in_bank / self.t_curr}")




        return result
