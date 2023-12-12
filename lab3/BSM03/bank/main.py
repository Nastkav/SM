from create import Create
from process import Process
import fun_rand as fun
from model import Model

c = Create(0.5)
p1 = Process(0.3)
p2 = Process(0.3)

c.next_element = [p1, p2]

c.distribution = 'exp'
p1.distribution = 'exp'
p2.distribution = 'exp'

p1.max_queue = 3
p2.max_queue = 3

p1.queue = 2
p2.queue = 2

p1.state[0] = 1
p2.state[0] = 1

c.t_next[0] = 0.1
p1.t_next[0] = fun.norm(1, 0.3)
p2.t_next[0] = fun.norm(1, 0.3)

c.name = 'CLIENT'
p1.name = 'CASHIER-1'
p2.name = 'CASHIER-2'

elements = [c, p1, p2]
model = Model(elements, cashiers=[p1, p2], num=2)
model.simulate(1000)
