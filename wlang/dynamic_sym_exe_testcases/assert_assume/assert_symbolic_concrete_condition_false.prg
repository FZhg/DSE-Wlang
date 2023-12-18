havoc x;
assume x>1000;
assert x>100
________
sym_state:
x: x!53
pc: [1000 < x!53, 100 < x!53]

concrete_state:
x: 1001
________
num_states: 1