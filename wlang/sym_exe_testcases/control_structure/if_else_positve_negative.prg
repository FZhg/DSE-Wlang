havoc x;
if x > 1 then {
    x := 7
} else {
    x := 5
}
________
x: 7
pc: [1 < x!271]
________
x: 5
pc: [Not(1 < x!271)]
________
num_states: 2