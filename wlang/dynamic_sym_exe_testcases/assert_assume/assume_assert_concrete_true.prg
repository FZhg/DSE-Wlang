x := 1;
assume x > 0;
x := x + 8;
assert x < 10;
x := x + 1
________
sym_state:
x: 10
pc: []

concrete_state:
x: 10
________
num_states: 1