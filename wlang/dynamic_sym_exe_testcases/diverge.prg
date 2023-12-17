havoc x, y;
if y * y = -1 + x * x *x - x  then {
    x := 1
}
________
sym_state:
x: x!23
y: y!24
pc: [Not(y!24*y!24 == -1 + x!23*x!23*x!23 - x!23)]

concrete_state:
x: 0
y: 0
________
num_states: 1