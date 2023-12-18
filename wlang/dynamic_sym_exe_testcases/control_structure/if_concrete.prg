havoc x, y;
x := 10;
if x > 1 then {
    y := 2
};
if y > 1 then {
    havoc y
}
________
sym_state:
x: 10
y: y!70
pc: []

concrete_state:
x: 10
y: 0
________
num_states: 1