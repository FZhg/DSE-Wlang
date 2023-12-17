havoc x;
assume x>1000;
assert x>100
________
sym_state:
x: x!33
pc: [1000 < x!33, 100 < x!33]

concrete_state:
x: 1001
________
num_states: 1