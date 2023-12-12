import numpy as np
import element as e


class Process(e.Element):
    def __init__(self, path_for_type=None, **kwargs):
        super().__init__(**kwargs)
        self.types = [-1] * self.channel
        self.queue_types = []
        self.path_for_type = path_for_type
        self.prior_types = []

        self.delta_t_following_to_the_lab_reception = 0
        self.tprev_following_to_the_lab_reception = 0

        self.t_starts = [-1] * self.channel
        self.t_starts_queue = []

        self.delta_t_finish_reception = 0
        self.count_type2 = 0

    def in_act(self, next_type_element, t_start):
        self.next_type_element = next_type_element

        if self.name == 'TO_THE_LAB':
            self.delta_t_following_to_the_lab_reception += self.t_curr - self.tprev_following_to_the_lab_reception
            self.tprev_following_to_the_lab_reception = self.t_curr

        if self.name == 'TO_THE_RECEPTION_DOCTOR' and next_type_element == 2:
            self.delta_t_finish_reception += self.t_curr - t_start
            self.count_type2 += 1

        free_channels = self.get_free_channels()
        for i in free_channels:
            self.state[i] = 1
            self.t_next[i] = self.t_curr + super().get_delay()
            self.types[i] = self.next_type_element
            self.t_starts[i] = t_start
            break
        else:
            if self.queue < self.max_queue:
                self.queue += 1
                self.queue_types.append(self.next_type_element)
                self.t_starts_queue.append(t_start)
            else:
                self.failure += 1

    def out_act(self):
        super().out_act()

        current_channels = self.get_current_channel()

        for i in current_channels:
            self.t_next[i] = np.inf
            self.state[i] = 0
            prev_next_type_element = self.types[i]
            prev_t_start = self.t_starts[i]
            self.types[i] = -1
            self.t_starts[i] = -1

            if self.queue > 0:
                self.queue -= 1
                prior_index = self.get_prior_index_from_queue()
                self.next_type_element = self.queue_types.pop(prior_index)

                self.state[i] = 1
                self.t_next[i] = self.t_curr + super().get_delay()
                self.types[i] = self.next_type_element
                self.t_starts[i] = self.t_starts_queue.pop(prior_index)
            if self.next_element is not None:
                self.next_type_element = 1 if self.name == 'TO_THE_RECEPTION_DOCTOR' else prev_next_type_element

                print('next_type_element:', self.next_type_element)
                if self.path_for_type is None:
                    next_element = np.random.choice(self.next_element, p=self.probability)
                    next_element.in_act(self.next_type_element, prev_t_start)
                else:
                    for idx, path in enumerate(self.path_for_type):
                        print('Path ', path)
                        if self.next_type_element in path:
                            next_element = self.next_element[idx]
                            print(f'\n\nType {self.next_type_element} and have process {next_element.name}\n\n')
                            next_element.in_act(self.next_type_element, prev_t_start)
                            break

    def get_prior_index_from_queue(self):
        for prior_types_i in self.prior_types:
            for type_i in np.unique(self.queue_types):
                if type_i == prior_types_i:
                    return self.queue_types.index(type_i)
        else:
            return 0

    def print_info(self):
        super().print_info()
        print(f'queue={self.queue}; failure={self.failure}')
        print(f'types of elements={self.types}')

    def calculate(self, delta):
        self.mean_queue_length = + delta * self.queue
