x := 3;
havoc y;
while x < 10 do {
    x := x + y;
    y := 4
}
________
sym_state:
x: 11 + y!0
y: 4
pc: [10 > 3 + y!0, 10 > 7 + y!0, Not(10 > 11 + y!0)]

concrete_state:
x: 11
y: 4
________
sym_state:
x: 15 + y!0
y: 4
pc: [10 > 3 + y!0, 10 > 7 + y!0, Not(Not(10 > 11 + y!0)), Not(10 > 15 + y!0)]

concrete_state:
x: 13
y: 4
________
sym_state:
x: 19 + y!0
y: 4
pc: [10 > 3 + y!0, 10 > 7 + y!0, Not(Not(10 > 11 + y!0)), Not(Not(10 > 15 + y!0)), Not(10 > 19 + y!0)]

concrete_state:
x: 13
y: 4
________
sym_state:
x: 23 + y!0
y: 4
pc: [10 > 3 + y!0, 10 > 7 + y!0, Not(Not(10 > 11 + y!0)), Not(Not(10 > 15 + y!0)), Not(Not(10 > 19 + y!0)), Not(10 > 23 + y!0)]

concrete_state:
x: 13
y: 4
________
sym_state:
x: 27 + y!0
y: 4
pc: [10 > 3 + y!0, 10 > 7 + y!0, Not(Not(10 > 11 + y!0)), Not(Not(10 > 15 + y!0)), Not(Not(10 > 19 + y!0)), Not(Not(10 > 23 + y!0)), Not(10 > 27 + y!0)]

concrete_state:
x: 13
y: 4
________
sym_state:
x: 31 + y!0
y: 4
pc: [10 > 3 + y!0, 10 > 7 + y!0, Not(Not(10 > 11 + y!0)), Not(Not(10 > 15 + y!0)), Not(Not(10 > 19 + y!0)), Not(Not(10 > 23 + y!0)), Not(Not(10 > 27 + y!0)), Not(10 > 31 + y!0)]

concrete_state:
x: 13
y: 4
________
sym_state:
x: 35 + y!0
y: 4
pc: [10 > 3 + y!0, 10 > 7 + y!0, Not(Not(10 > 11 + y!0)), Not(Not(10 > 15 + y!0)), Not(Not(10 > 19 + y!0)), Not(Not(10 > 23 + y!0)), Not(Not(10 > 27 + y!0)), Not(Not(10 > 31 + y!0)), Not(10 > 35 + y!0)]

concrete_state:
x: 13
y: 4
________
sym_state:
x: 39 + y!0
y: 4
pc: [10 > 3 + y!0, 10 > 7 + y!0, Not(Not(10 > 11 + y!0)), Not(Not(10 > 15 + y!0)), Not(Not(10 > 19 + y!0)), Not(Not(10 > 23 + y!0)), Not(Not(10 > 27 + y!0)), Not(Not(10 > 31 + y!0)), Not(Not(10 > 35 + y!0)), Not(10 > 39 + y!0)]

concrete_state:
x: 13
y: 4
________
sym_state:
x: 7 + y!0
y: 4
pc: [10 > 3 + y!0, Not(10 > 7 + y!0)]

concrete_state:
x: 10
y: 4
________
sym_state:
x: 3 + y!0
y: 4
pc: [Not(10 > 3 + y!0)]

concrete_state:
x: 10
y: 4
________
num_states: 10