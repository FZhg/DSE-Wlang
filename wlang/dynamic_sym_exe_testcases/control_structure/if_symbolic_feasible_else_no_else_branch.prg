havoc x;
if x > -2  then {
    x := 1
} ;
x := 2
________
sym_state:
x: 2
pc: [-2 < x!59]

concrete_state:
x: 2
________
sym_state:
x: 2
pc: [Not(-2 < x!59)]

concrete_state:
x: 2
________
num_states: 2