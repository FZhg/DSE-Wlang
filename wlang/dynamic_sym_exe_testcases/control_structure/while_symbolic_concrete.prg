x := 5;
havoc y;
while (x > 0 and y > 0) or x + y > 10 do {
    if x < 0 then x := y else x := x - 1;
    if y < 0 then y := x else y := y + x
}
________
sym_state:
x: 5
y: y!25
pc: [Not(Or(And(5 > 0, 0 < y!25), 10 < 5 + y!25))]

concrete_state:
x: 5
y: 0
________
sym_state:
x: -1
y: 9 + y!25
pc: [Not(Not(Or(And(5 > 0, 0 < y!25), 10 < 5 + y!25))), Not(0 > y!25), Or(And(4 > 0, 0 < 4 + y!25), 10 < 4 + 4 + y!25), Not(0 > 4 + y!25), Or(And(3 > 0, 0 < 7 + y!25), 10 < 3 + 7 + y!25), Not(0 > 7 + y!25), Or(And(2 > 0, 0 < 9 + y!25), 10 < 2 + 9 + y!25), Not(0 > 9 + y!25), Or(And(1 > 0, 0 < 10 + y!25), 10 < 1 + 10 + y!25), Not(0 > 10 + y!25), Or(And(0 > 0, 0 < 10 + y!25), 10 < 0 + 10 + y!25), Not(0 > 10 + y!25), Not(Or(And(-1 > 0, 0 < 9 + y!25), 10 < -1 + 9 + y!25))]

concrete_state:
x: -1
y: 10
________
sym_state:
x: 6 + y!25
y: 39 + 5*y!25
pc: [Not(Not(Or(And(-1 > 0, 0 < 9 + y!25), 10 < -1 + 9 + y!25))), Not(0 > 9 + y!25), Or(And(0 < 9 + y!25, 0 < 18 + 2*y!25),
   10 < 9 + y!25 + 18 + 2*y!25), Not(0 > 9 + y!25), Not(0 > 18 + 2*y!25), Or(And(0 < 8 + y!25, 0 < 26 + 3*y!25),
   10 < 8 + y!25 + 26 + 3*y!25), Not(0 > 8 + y!25), Not(0 > 26 + 3*y!25), Or(And(0 < 7 + y!25, 0 < 33 + 4*y!25),
   10 < 7 + y!25 + 33 + 4*y!25), Not(0 > 7 + y!25), Not(0 > 33 + 4*y!25), Or(And(0 < 6 + y!25, 0 < 39 + 5*y!25),
   10 < 6 + y!25 + 39 + 5*y!25)]

concrete_state:
x: 9
y: 54
________
num_states: 3