havoc x, y;
assume x > 20;
z := 7;
if (x > 10) and (z >= 7) then {
    y := 1;
    x := x + 1
} else {
    y := 0;
    x := x + 2
};
assert y = 1;
assert x >= 22
________
sym_state:
x: 1 + x!0
y: 1
z: 7
pc: [20 < x!0, And(10 < x!0, 7 >= 7), 22 <= 1 + x!0]

concrete_state:
x: 22
y: 1
z: 7
________
num_states: 1