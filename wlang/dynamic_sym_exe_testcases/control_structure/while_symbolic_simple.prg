havoc y;
while y < 0 do {
    y := y + 1
}
________
sym_state:
y: y!13
pc: [Not(0 > y!13)]

concrete_state:
y: 0
________
sym_state:
y: 1 + y!13
pc: [Not(Not(0 > y!13)), Not(0 > 1 + y!13)]

concrete_state:
y: 0
________
sym_state:
y: 2 + y!13
pc: [Not(Not(0 > y!13)), Not(Not(0 > 1 + y!13)), Not(0 > 2 + y!13)]

concrete_state:
y: 0
________
sym_state:
y: 3 + y!13
pc: [Not(Not(0 > y!13)), Not(Not(0 > 1 + y!13)), Not(Not(0 > 2 + y!13)), Not(0 > 3 + y!13)]

concrete_state:
y: 0
________
sym_state:
y: 4 + y!13
pc: [Not(Not(0 > y!13)), Not(Not(0 > 1 + y!13)), Not(Not(0 > 2 + y!13)), Not(Not(0 > 3 + y!13)), Not(0 > 4 + y!13)]

concrete_state:
y: 0
________
sym_state:
y: 5 + y!13
pc: [Not(Not(0 > y!13)), Not(Not(0 > 1 + y!13)), Not(Not(0 > 2 + y!13)), Not(Not(0 > 3 + y!13)), Not(Not(0 > 4 + y!13)), Not(0 > 5 + y!13)]

concrete_state:
y: 0
________
sym_state:
y: 6 + y!13
pc: [Not(Not(0 > y!13)), Not(Not(0 > 1 + y!13)), Not(Not(0 > 2 + y!13)), Not(Not(0 > 3 + y!13)), Not(Not(0 > 4 + y!13)), Not(Not(0 > 5 + y!13)), Not(0 > 6 + y!13)]

concrete_state:
y: 0
________
sym_state:
y: 7 + y!13
pc: [Not(Not(0 > y!13)), Not(Not(0 > 1 + y!13)), Not(Not(0 > 2 + y!13)), Not(Not(0 > 3 + y!13)), Not(Not(0 > 4 + y!13)), Not(Not(0 > 5 + y!13)), Not(Not(0 > 6 + y!13)), Not(0 > 7 + y!13)]

concrete_state:
y: 0
________
sym_state:
y: 8 + y!13
pc: [Not(Not(0 > y!13)), Not(Not(0 > 1 + y!13)), Not(Not(0 > 2 + y!13)), Not(Not(0 > 3 + y!13)), Not(Not(0 > 4 + y!13)), Not(Not(0 > 5 + y!13)), Not(Not(0 > 6 + y!13)), Not(Not(0 > 7 + y!13)), Not(0 > 8 + y!13)]

concrete_state:
y: 0
________
sym_state:
y: 9 + y!13
pc: [Not(Not(0 > y!13)), Not(Not(0 > 1 + y!13)), Not(Not(0 > 2 + y!13)), Not(Not(0 > 3 + y!13)), Not(Not(0 > 4 + y!13)), Not(Not(0 > 5 + y!13)), Not(Not(0 > 6 + y!13)), Not(Not(0 > 7 + y!13)), Not(Not(0 > 8 + y!13)), Not(0 > 9 + y!13)]

concrete_state:
y: 0
________
sym_state:
y: 10 + y!13
pc: [Not(Not(0 > y!13)), Not(Not(0 > 1 + y!13)), Not(Not(0 > 2 + y!13)), Not(Not(0 > 3 + y!13)), Not(Not(0 > 4 + y!13)), Not(Not(0 > 5 + y!13)), Not(Not(0 > 6 + y!13)), Not(Not(0 > 7 + y!13)), Not(Not(0 > 8 + y!13)), Not(Not(0 > 9 + y!13)), Not(0 > 10 + y!13)]

concrete_state:
y: 0
________
num_states: 11