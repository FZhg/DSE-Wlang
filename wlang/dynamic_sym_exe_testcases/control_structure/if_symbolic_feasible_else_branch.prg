havoc x;
if x > -2  then {
    x := 1
} else {
    x := 2
}
________
sym_state:
x: 1
pc: [-2 < x!40]

concrete_state:
x: 1
________
sym_state:
x: 2
pc: [Not(-2 < x!40)]

concrete_state:
x: 2
________
num_states: 2