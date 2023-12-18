havoc x;
while x < 20 do {
    havoc x;
    assume x > 30
}
________
sym_state:
x: x!66
pc: [20 > x!65, 30 < x!66, Not(20 > x!66)]

concrete_state:
x: 31
________
sym_state:
x: x!65
pc: [Not(20 > x!65)]

concrete_state:
x: 20
________
num_states: 2