havoc x;
assume x > 1;
if x < 0 then {
    x := 1
} else {
    x := 2
}
________
sym_state:
x: 2
pc: [1 < x!58, Not(0 > x!58)]

concrete_state:
x: 2
________
num_states: 1