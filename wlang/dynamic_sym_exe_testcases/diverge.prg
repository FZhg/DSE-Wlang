havoc x, y;
if y * y = -1 + x * x *x - x  then {
    x := 1
}
________
sym_state:
x: x!41
y: y!42
pc: [Not(y!42*y!42 == -1 + x!41*x!41*x!41 - x!41)]

concrete_state:
x: 0
y: 0
________
num_states: 1