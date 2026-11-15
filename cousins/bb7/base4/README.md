# A base-4 tower machine that never halts

    1RB0LG_1LC1LB_0RD1LE_1RE1RD_0RF0RE_1LA1RF_---1LB

Found in the cousins search on the claimed BB(7) champion (the champion was found by Jeff Ketchersid).
Shawn Ligocki's Quick_Sim stopped on it with a power tower more than 500 levels high, which is why we looked at it.

## Transcript (one digit per step, `2*state + symbol`, `0-9` then `a b c d`)

Build round `R(n) = 2 4 7(n) 6 8 a 0 3(n+3)`, build chain `B(k) = R(3) R(7) ... R(4k-1)`.

    0258bba1d2477698a033  259(5)8a033  B(4)
    258b(20) a1d 3(18) 247(20)698a033  259(5)8a033  B(4)
    259(21)8a033    B(20)
    259(85)8a033    B(84)
    259(341)8a033   B(340)
    259(1365)8a033  B(1364)
    259(5461)8a033  ...

## The two rules

Tape shape `1^L [C reads 1] 1^(n-1)`, written (L, n).

| | when | digits | what happens |
|---|---|---|---|
| layer | L is 2 or more | `2 5 9(n+1) 8 a 0 3 3 B(n)` | L -> L - 2, n -> 4n + 4 |
| gate | L = 0 | `2 5 8 b(n) a 1 d ...` | L -> n, n -> 4 |

From a blank tape the machine is at (0, 2) after 2 steps. L and n stay even, so the gate is always met with
L = 0 exactly, and the halt wire (G reads 0) is never used. Each gate visit puts the old block in the
exponent, so the growth is a power tower with no end.

## Proof

`Base4Tower.v` (Coq 8.18, no axioms, compiles in a few seconds): theorem `never_halts`.
It proves the layer and the gate for all sizes, and that the shape is kept for ever.

The gate has only two sides and neither halts. A halting version needs a third side
(for example a layer rule that can make n odd, so that the countdown can land on 1).

## Changes of this machine (one and two wires)

56,862 tables. Halters are all tiny (biggest 2,736 steps). 30 got no answer (`base4_changes_no_answer.txt`).
Five of the 30 keep the layer shape. The best one is

    1RB0LG_1LC1LB_0RD0LF_1RE1RD_0RF0RE_1LA1RF_---1LD      ("number 1")

| when | what happens |
|---|---|
| L is 3 or more | L -> L - 1, n -> 4n |
| L = 2 (gate) | `011` becomes `100`, then L -> n - 1, n -> 4 |
| L = 1 | halts (`5 b a 1 c`) |

It has a working halt wire, but the gate at L = 2 always comes first, so it runs forever (tested, not proved).

One and two wire changes of number 1 (55,837 more tables): 5 new halters found with Quick_Sim
(`variant1_changes_halters_from_quick_sim.txt`), biggest about 1.9 x 10^30 steps; 10 with no answer
(`variant1_changes_no_answer.txt`).
