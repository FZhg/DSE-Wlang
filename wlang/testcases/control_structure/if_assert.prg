havoc x;
if x > 1 then {
    x := x + 1;
    assert(x < -1)
} else {
    x := 5
};
assert(x > 4);
havoc x;
while x < 20 do {
    x := x + 4
};
if x = 21 then {
    havoc x
}
________
x: 1 + x!0
pc: [1 < x!0]
________
x: x!46
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, 20 > 12 + x!4, 20 > 16 + x!4, 20 > 20 + x!4, 20 > 24 + x!4, 20 > 28 + x!4, 20 > 32 + x!4, 20 > 36 + x!4, Not(20 > 40 + x!4), 21 == 40 + x!4]
________
x: x!55
pc: [Not(1 < x!0), 5 > 4, Not(20 > x!4), 21 == x!4]
________
x: x!61
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, Not(20 > 4 + x!4), 21 == 4 + x!4]
________
x: x!72
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, Not(20 > 8 + x!4), 21 == 8 + x!4]
________
x: x!83
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, Not(20 > 12 + x!4), 21 == 12 + x!4]
________
x: x!94
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, 20 > 12 + x!4, Not(20 > 16 + x!4), 21 == 16 + x!4]
________
x: x!104
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, 20 > 12 + x!4, 20 > 16 + x!4, Not(20 > 20 + x!4), 21 == 20 + x!4]
________
x: x!114
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, 20 > 12 + x!4, 20 > 16 + x!4, 20 > 20 + x!4, Not(20 > 24 + x!4), 21 == 24 + x!4]
________
x: x!125
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, 20 > 12 + x!4, 20 > 16 + x!4, 20 > 20 + x!4, 20 > 24 + x!4, Not(20 > 28 + x!4), 21 == 28 + x!4]
________
x: x!136
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, 20 > 12 + x!4, 20 > 16 + x!4, 20 > 20 + x!4, 20 > 24 + x!4, 20 > 28 + x!4, Not(20 > 32 + x!4), 21 == 32 + x!4]
________
x: x!147
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, 20 > 12 + x!4, 20 > 16 + x!4, 20 > 20 + x!4, 20 > 24 + x!4, 20 > 28 + x!4, 20 > 32 + x!4, Not(20 > 36 + x!4), 21 == 36 + x!4]
________
x: 40 + x!4
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, 20 > 12 + x!4, 20 > 16 + x!4, 20 > 20 + x!4, 20 > 24 + x!4, 20 > 28 + x!4, 20 > 32 + x!4, 20 > 36 + x!4, Not(20 > 40 + x!4), Not(21 == 40 + x!4)]
________
x: x!4
pc: [Not(1 < x!0), 5 > 4, Not(20 > x!4), Not(21 == x!4)]
________
x: 4 + x!4
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, Not(20 > 4 + x!4), Not(21 == 4 + x!4)]
________
x: 8 + x!4
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, Not(20 > 8 + x!4), Not(21 == 8 + x!4)]
________
x: 12 + x!4
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, Not(20 > 12 + x!4), Not(21 == 12 + x!4)]
________
x: 16 + x!4
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, 20 > 12 + x!4, Not(20 > 16 + x!4), Not(21 == 16 + x!4)]
________
x: 20 + x!4
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, 20 > 12 + x!4, 20 > 16 + x!4, Not(20 > 20 + x!4), Not(21 == 20 + x!4)]
________
x: 24 + x!4
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, 20 > 12 + x!4, 20 > 16 + x!4, 20 > 20 + x!4, Not(20 > 24 + x!4), Not(21 == 24 + x!4)]
________
x: 28 + x!4
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, 20 > 12 + x!4, 20 > 16 + x!4, 20 > 20 + x!4, 20 > 24 + x!4, Not(20 > 28 + x!4), Not(21 == 28 + x!4)]
________
x: 32 + x!4
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, 20 > 12 + x!4, 20 > 16 + x!4, 20 > 20 + x!4, 20 > 24 + x!4, 20 > 28 + x!4, Not(20 > 32 + x!4), Not(21 == 32 + x!4)]
________
x: 36 + x!4
pc: [Not(1 < x!0), 5 > 4, 20 > x!4, 20 > 4 + x!4, 20 > 8 + x!4, 20 > 12 + x!4, 20 > 16 + x!4, 20 > 20 + x!4, 20 > 24 + x!4, 20 > 28 + x!4, 20 > 32 + x!4, Not(20 > 36 + x!4), Not(21 == 36 + x!4)]
________
num_states: 23