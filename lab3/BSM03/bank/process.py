import numpy as np
from bank import element as e


class Process(e.Element):
    def __init__(self, delay, channels=1):
        super().__init__(delay)
        self.queue = 0
        self.max_queue = float('inf')
        self.mean_queue = 0.0
        self.failure = 0
        self.mean_load = 0
        self.channel = channels
        self.state = [0] * self.channel
        self.t_next = [np.inf] * self.channel
        self.probability = [1]
        self.t_prev = 0
        self.delta_t_depart = 0
        self.t_prev_depart = 0
        self.delta_t_in_bank = 0

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
                self.t_prev = self.t_curr
                self.state[i] = 1
                self.t_next[i] = self.t_curr + super().get_delay()
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
        super().out_act()
        current_channel = self.get_occupied_channels()
        for i in current_channel:

            self.t_next[i] = np.inf
            self.state[i] = 0

            self.delta_t_depart += self.t_curr - self.t_prev_depart
            self.t_prev_depart = self.t_curr

            self.delta_t_in_bank += self.t_curr - self.t_prev

            if self.queue > 0:
                self.queue -= 1
                self.state[i] = 1
                self.t_next[i] = self.t_curr + super().get_delay()
            if self.next_element is not None:
                next_el = np.random.choice(a=self.next_element, p=self.probability)
                next_el.in_act()

    def get_mean_queue(self):
        return self.mean_queue

    def get_failure(self):
        return self.failure

    def print_info(self):
        super().print_info()
        print(f'failure= {str(self.failure)}, queue= {str(self.queue)}')

    def do_statistics(self, delta):
        self.mean_queue = self.get_mean_queue() + self.queue * delta

        for i in range(self.channel):
            self.mean_load += self.state[i] * delta

        self.mean_load = self.mean_load / self.channel
