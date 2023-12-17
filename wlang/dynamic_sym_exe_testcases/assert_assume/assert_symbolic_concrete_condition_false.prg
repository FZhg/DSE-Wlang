havoc x;
assume x>1000;
assert x>100
________
sym_state:
x: x!23
pc: [1000 < x!23, 100 < x!23]

concrete_state:
x: 1001
________
num_states: 1