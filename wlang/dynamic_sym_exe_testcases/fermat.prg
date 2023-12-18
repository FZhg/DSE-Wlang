havoc x, y, z;
if (x > 0) and ((y > 0) and (z > 0)) then {
    if y*y*y = x * x *x + z* z *z then {
        print_state
    }
}
________
sym_state:
x: x!23
y: y!24
z: z!25
pc: [Not(And(0 < x!23, And(0 < y!24, 0 < z!25)))]

concrete_state:
x: 0
y: 0
z: 0
________
sym_state:
x: x!23
y: y!24
z: z!25
pc: [Not(Not(And(0 < x!23, And(0 < y!24, 0 < z!25)))), Not(y!24*y!24*y!24 == x!23*x!23*x!23 + z!25*z!25*z!25)]

concrete_state:
x: 1
y: 1
z: 1
________
num_states: 2