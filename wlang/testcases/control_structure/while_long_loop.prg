havoc x;
while x < 7 do {
    x :=  x + 1
};
x := x + 1
________
x: 11 + x!215
pc: [7 > x!215, 7 > 1 + x!215, 7 > 2 + x!215, 7 > 3 + x!215, 7 > 4 + x!215, 7 > 5 + x!215, 7 > 6 + x!215, 7 > 7 + x!215, 7 > 8 + x!215, 7 > 9 + x!215, Not(7 > 10 + x!215)]
________
x: 1 + x!215
pc: [Not(7 > x!215)]
________
x: 2 + x!215
pc: [7 > x!215, Not(7 > 1 + x!215)]
________
x: 3 + x!215
pc: [7 > x!215, 7 > 1 + x!215, Not(7 > 2 + x!215)]
________
x: 4 + x!215
pc: [7 > x!215, 7 > 1 + x!215, 7 > 2 + x!215, Not(7 > 3 + x!215)]
________
x: 5 + x!215
pc: [7 > x!215, 7 > 1 + x!215, 7 > 2 + x!215, 7 > 3 + x!215, Not(7 > 4 + x!215)]
________
x: 6 + x!215
pc: [7 > x!215, 7 > 1 + x!215, 7 > 2 + x!215, 7 > 3 + x!215, 7 > 4 + x!215, Not(7 > 5 + x!215)]
________
x: 7 + x!215
pc: [7 > x!215, 7 > 1 + x!215, 7 > 2 + x!215, 7 > 3 + x!215, 7 > 4 + x!215, 7 > 5 + x!215, Not(7 > 6 + x!215)]
________
x: 8 + x!215
pc: [7 > x!215, 7 > 1 + x!215, 7 > 2 + x!215, 7 > 3 + x!215, 7 > 4 + x!215, 7 > 5 + x!215, 7 > 6 + x!215, Not(7 > 7 + x!215)]
________
x: 9 + x!215
pc: [7 > x!215, 7 > 1 + x!215, 7 > 2 + x!215, 7 > 3 + x!215, 7 > 4 + x!215, 7 > 5 + x!215, 7 > 6 + x!215, 7 > 7 + x!215, Not(7 > 8 + x!215)]
________
x: 10 + x!215
pc: [7 > x!215, 7 > 1 + x!215, 7 > 2 + x!215, 7 > 3 + x!215, 7 > 4 + x!215, 7 > 5 + x!215, 7 > 6 + x!215, 7 > 7 + x!215, 7 > 8 + x!215, Not(7 > 9 + x!215)]
________
num_states: 11