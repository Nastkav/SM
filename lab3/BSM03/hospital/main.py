import fun_rand as fun
from hospital.create import Create
from hospital.exit import Exit
from hospital.model import Model
from hospital.process import Process

c = Create(name='CREATOR_1', delay=15.0)
p1 = Process(name='TO_THE_DOCTOR', channels=2)
p2 = Process(name='TO_THE_WARD', delay=3.0, delay_dev=8, channels=3)
p3 = Process(name='TO_THE_LAB', delay=2.0, delay_dev=5, channels=10)
p4 = Process(name='REGISTRY_IN_LAB', delay=4.5, delay_dev=3, channels=1)
p5 = Process(name='ANALYSES_IN_LAB', delay=4.0, delay_dev=2, channels=2)
p6 = Process(name='TO_THE_RECEPTION_DOCTOR', delay=2.0, delay_dev=5, channels=10)

c.distribution = 'exp'
p1.distribution = 'exp'
p2.distribution = 'uniform'
p3.distribution = 'uniform'
p4.distribution = 'erlang'
p5.distribution = 'erlang'
p6.distribution = 'uniform'

p1.max_queue = 100
p2.max_queue = 100
p3.max_queue = 0
p4.max_queue = 100
p5.max_queue = 100
p6.max_queue = 100

ex1 = Exit(name='EXIT1')
ex2 = Exit(name='EXIT2')

c.next_element = [p1]
p1.next_element = [p2, p3]
p2.next_element = [ex1]
p3.next_element = [p4]
p4.next_element = [p5]
p5.next_element = [ex2, p6]
p6.next_element = [p1]

p1.path_for_type = [[1], [2, 3]]
p5.path_for_type = [[3], [2]]

p1.prior_types = [1]

elements = [c, p1, p2, p3, p4, p5, p6, ex1, ex2]

model = Model(elements)
model.simulate(1000)

