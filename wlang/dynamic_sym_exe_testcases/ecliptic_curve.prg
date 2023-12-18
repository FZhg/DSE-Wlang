havoc x, y;
if y * y =  x * x *x + 17 then {
    x := 1
}
________
sym_state:
x: x!51
y: y!52
pc: [Not(y!52*y!52 == x!51*x!51*x!51 + 17)]

concrete_state:
x: 0
y: 0
________
sym_state:
x: 1
y: y!52
pc: [Not(Not(y!52*y!52 == x!51*x!51*x!51 + 17))]

concrete_state:
x: 1
y: 3
________
num_states: 2