havoc x;
while x > 5 do {
    x := 4
}
________
sym_state:
x: x!64
pc: [Not(5 < x!64)]

concrete_state:
x: 0
________
sym_state:
x: 4
pc: [Not(Not(5 < x!64))]

concrete_state:
x: 4
________
num_states: 2