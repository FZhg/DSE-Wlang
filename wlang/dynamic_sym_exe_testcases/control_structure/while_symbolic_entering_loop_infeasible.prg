havoc x;
while x < 20 do {
    havoc x;
    assume x > 30
}
________
sym_state:
x: x!35
pc: [20 > x!34, 30 < x!35, Not(20 > x!35)]

concrete_state:
x: 31
________
sym_state:
x: x!34
pc: [Not(20 > x!34)]

concrete_state:
x: 20
________
num_states: 2