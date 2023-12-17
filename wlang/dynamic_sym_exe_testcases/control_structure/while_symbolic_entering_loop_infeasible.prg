havoc x;
while x < 20 do {
    havoc x;
    assume x > 30
}
________
sym_state:
x: x!45
pc: [20 > x!44, 30 < x!45, Not(20 > x!45)]

concrete_state:
x: 31
________
sym_state:
x: x!44
pc: [Not(20 > x!44)]

concrete_state:
x: 20
________
num_states: 2