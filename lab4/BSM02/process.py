from copy import deepcopy
import numpy as np
import element as e

class Process(e.Element):
    def __init__(self, delay, channels=1):
        super().__init__(delay)
        self.queue = 0
        self.max_queue = float('inf')
        self.mean_queue = 0.0
        self.failure = 0
        self.mean_load = 0
        self.channel = channels
        self.state = [0]*self.channel
        self.t_next = [np.inf]*self.channel
        self.probability = [1]
        self.priority = [1]

    # lab3
    def choose_by_priority(self):
        priorities = deepcopy(self.priority)
        min_queue = float('inf')
        with_min_q_index = 0
        for p in range(len(priorities)):
            if min(priorities) == float('inf'):
                break
            pr_index = priorities.index(min(priorities))
            if 0 in self.next_element[pr_index].state:
                return self.next_element[pr_index]
            else:
                if min_queue > self.next_element[pr_index].queue:
                    min_queue = self.next_element[pr_index].queue
                    with_min_q_index = self.next_element.index(self.next_element[pr_index])

            priorities[pr_index] = float('inf')
        return self.next_element[with_min_q_index]

    def choose_next_el(self):
        if self.probability == [1] and self.priority == [1]:
            return self.next_element[0]
        elif self.probability != [1] and self.priority != [1]:
            raise Exception('Error: Probability and priority are both defined.')
        elif self.probability != [1]:
            next_element = np.random.choice(a=self.next_element, p=self.probability)
            return next_element
        elif self.priority != [1]:
            next_element = self.choose_by_priority()
            return next_element

    def in_act_mono(self):
        if self.get_state() == 0:
            self.set_state(1)
            self.set_tnext(self.get_tcurr() + self.get_delay())
        else:
            if self.queue < self.max_queue:
                self.queue += 1
            else:
                self.failure += 1

    def get_free_channels(self):
        free_channels = []
        for i in range(self.channel):
            if self.state[i] == 0:
                free_channels.append(i)
        return free_channels

    def in_act(self):
        free_channels = self.get_free_channels()
        if len(free_channels) > 0:
            for i in free_channels:
                self.state[i] = 1
                self.t_next[i] = self.t_curr + self.get_delay()
                break
        else:
            if self.queue < self.max_queue:
                self.queue += 1
            else:
                self.failure += 1

    def get_occupied_channels(self):
        current_channels = []
        for i in range(self.channel):
            if self.t_next[i] == self.t_curr:
                current_channels.append(i)
        return current_channels

    def out_act(self):
        current_channel = self.get_occupied_channels()
        for i in current_channel:
            super().out_act()
            self.t_next[i] = np.inf
            self.state[i] = 0
            if self.queue > 0:
                self.queue -= 1
                self.state[i] = 1
                self.t_next[i] = self.t_curr + self.get_delay()
            if self.next_element is not None:
                #lab3
                next_el = self.choose_next_el()
                #next_el = np.random.choice(a=self.next_element, p=self.probability)
                next_el.in_act()

    def get_failure(self):
        return self.failure

    def get_queue(self):
        return self.queue

    def set_queue(self, queue):
        self.queue = queue

    def get_max_queue(self):
        return self.max_queue

    def set_max_queue(self, max_queue):
        self.max_queue = max_queue

    def print_info(self):
        super().print_info()
        print(f'failure= {str(self.failure)}, queue= {str(self.queue)}')

    def get_mean_queue(self):
        return self.mean_queue
    # zmin. pid task 2
    def do_statistics(self, delta):

        self.mean_queue = self.get_mean_queue() + self.queue * delta

        for i in range(self.channel):
            self.mean_load += self.state[i] * delta

        self.mean_load = self.mean_load / self.channel


