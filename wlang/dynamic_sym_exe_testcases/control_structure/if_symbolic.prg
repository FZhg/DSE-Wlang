havoc x, y;
x := 10;
if x > 1 then {
    x := x + 1
};
if y > 1 then {
    x  := y + 1
} else {
    x := x - 1
}
________
sym_state:
x: 10
y: y!166
pc: [Not(1 < y!166)]

concrete_state:
x: 10
y: 0
________
sym_state:
x: 1 + y!166
y: y!166
pc: [Not(Not(1 < y!166))]

concrete_state:
x: 3
y: 2
________
num_states: 2