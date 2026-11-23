# Tables that look the same in the transcript, not in the TNF (23 Nov)

Vishnu's correction: a bigger machine is not "one or two wires near" Jeff
Ketchersid's table. It looks the same **in the transcript**. So the frame
must be written in transcript words, and the table is free inside it.

(For the record: the test of tables within two wire changes of Jeff's table
gave 57,214 tables, 517 of 533 survivors proved infinite by Quick_Sim, and
nothing bigger. Wrong kind of nearness.)

## The class (cls.c)

Every 7-state table with this grammar, as Vishnu read it from the transcript:
- the even digits make one closed loop A0→B0→C0→D0→E0→F0→A
  (A0 = `1RB`; the other five may write 0 or 1 and move L or R);
- the odd halves of the six loop states are three fillers (write 1, point to
  their own state), one take (write 0, points to its own state), one door
  (goes to G), one halt — in any arrangement, any directions;
- G is only behind the door; G0 and G1 are free and go back to the loop.

Tables are built only as far as a run from a blank tape needs them, so two
tables that behave the same are not counted twice.

Count (budget 3,000 steps while wires are still open):
- 18,977,338 full tables (every wire reached);
- 10,802,505 halt while a wire is still unchosen (small halters);
- 12,963,817 never reach some wire in 3,000 steps (loops and runaways).
Check: Jeff's table is in the set.

Running: all 18,977,338 from a blank tape.

## Stages so far (tested)

1. 20,000 steps: 5,497,971 halt (largest: step 19,924, 180 ones);
   13,479,367 still running.
2. Kept tables with 4 to 40 runs of 1s: 686,756. At 60,000 steps, kept those
   where the number of runs did not grow and the ones did: 390,461.
3. At 400,000 steps, same test: 42 halt (largest: step 261,774, 1,043 ones);
   244,838 kept. Jeff's table is among them (22 runs).
   Number of runs among the kept: mostly 3 to 5 (about 228,000); 6 or more:
   about 16,000.
4. Running: pay.c — over 2,000,000 steps, count how often a run gets shorter
   while the number of runs stays the same (a store paying). A plain growing
   block never does that.

Caution: the "row stays, block grows" filter was set by looking at Jeff's
tape. A machine with a very different early shape could be dropped by it.

## Stage 4 and Quick_Sim on the first batch (tested)

pay.c, 2,000,000 steps, 40 checks: Jeff's table shows a store paying at 39
of 40 checks. Of 244,838 tables: about 230,000 fewer than 15 times; 4,189
show it 25 times or more.

First batch to Quick_Sim (Shawn Ligocki), 8 seconds each: the 1,607 strongest.
845 proved infinite; 737 running at rule level 0 or 1; 21 at level 2; 3 at
level 3 or 4; 1 halts.

- Halts: `1RB1RZ_1RC0RB_0RD1RC_1LE1RD_1LF1LE_1LA0LG_1LA1LC`, 5,242,879 ones
  (5 × 2^20 − 1). Small.
- Level 4: Jeff's table and its disguise (digit c `0LD`), same numbers after
  15 minutes: (10↑↑↑)^48 10↑↑ 26150882433.
- Level 3, new: `1RB1RA_0RC1RZ_0LD0LC_0LE1LD_0RF1LE_1RA1RG_1LC0RA`.
  Same grammar, different loop (writes 1,0,0,0,0,1; moves R R L L R R).
  After 15 minutes of Quick_Sim, still running, ones about
  (10↑↑)^77 10↑ 646456686. That is steps of two arrows, where Jeff's has
  steps of three arrows. So far smaller than Jeff's. Its end is not known.
- The 21 at level 2, 90 seconds each: none halts. Most stop with "expression
  too complex" after 500 levels of exponent: they add one level per cycle
  (for example `1RB1RA_1LC1LB_0RD0LG_0RE0LD_1RF1RZ_0RA1RF_0LC0LB` at
  10↑↑500). One arrow per cycle, no rows; whether they ever halt is unknown.

So far: nothing bigger than Jeff's in the class. Still to screen: second
batch (2,582), the 737 shallow undecided, and about 10,000 just under the
cut.

## Second batch (tested)

2,582 tables, Quick_Sim 5 seconds each: 1,509 proved infinite; 1,073 still
running at rule level 0 or 1; none halts; none reaches level 2 while running.
Nothing deep in this batch.

## Vishnu's changed grammar (23 Nov, afternoon): loop of five, one door, two states behind it, halt behind the door

"Loop has 5 states, exactly one door, two states must be behind the door and
one of that wire is halt." Then: "think of an arithmetic where, in the two
states behind the door, G is touched rarely as a gate and the halt must
happen very rarely."

### The arithmetic on paper (not tested)

Three levels of "rare", one behind the other:

| what fires | when | how often |
|---|---|---|
| the loop and its fillers | every round | always |
| the door into F | home meets the wrong cell: a store has run out | once per store |
| F's second wire, into G | F meets the wrong cell: the whole row has run out | once per row |
| G's second wire, the halt | G meets the wrong cell | must be rarer still |

For the halt to be very rare, G must not decide by odd or even of the block
(that is fixed when the row is born, so it fires at G's second visit — the
"one-slot clock" we found in Jeff Ketchersid's machine). G should instead
**take one cell from a small counter each time it is entered, and halt when
the counter is empty.** Then: number of rows = size of the counter; the halt
is certain; and it comes only after that many rows of rows.
G is entered from F, and F is entered at home, so the counter G reads sits
by home, on the far side from the stores ("the left counter").

### cls5g.c — the class

Even loop A0→B0→C0→D0→E0→A; odd halves: one door (to F), three fillers, one
take; F: one wire back (to the loop or to itself), the other on to G;
G: one wire is the halt, the other free. G may be reached late or never
(printed as `------` when never reached in 60,000 steps). For each kept
table the number of times G was entered is printed, so "G touched rarely"
can be read off.

(cls5.c is the wider version with F and G fully free; it was too slow and
was stopped unfinished.)

## Gate class, complete (cls5g.c, fixed) — tested

Kept after the 60,000-step test: 578,417 tables (four quarters: 131,945 +
193,358 + 121,101 + 132,013). Halters met on the way: small (largest step
59,487, 579 ones).

Note: an earlier run of cls5g.c had a bug (tape cells left over between
branches). Its output was wrong and was thrown away. The numbers here are
from the fixed tool, checked against direct runs.

### Hand reading of five tables with "G entered at most 5 times"

One has a row of stores of 3 that gains one store as the numbers double
(`1RB1RA_0LC0RF_0LD1LC_1LE1RD_1RA0RE_1RG0RD_1LB1RZ`, proved infinite by
Quick_Sim). Four are a single block growing in a straight line with a few
fixed small pieces; G is entered only in the first few hundred steps.
Lesson: "G entered few times" mostly means "G used at the start, then
never". A rare gate is one that keeps being entered, later and later.
(Jeff Ketchersid's table: G entered 109 times in 2,000,000 steps, first at
step 8, last at step 568,099.)

### gate.c on all 578,417 (2,000,000 steps)

103 halt (largest 1,626 ones). By last entry into G:
- before step 60,000: 226,581 tables (G is start-only);
- after step 500,000: 350,715 tables; of these 302,361 enter G more than
  2,000 times (G is part of the round); 4,220 enter G at most 2,000 times
  **and** stores pay at 15+ of 40 checks: 625 with G ≤ 30 entries, 620 with
  31–300, 2,975 with 301–2,000.

Example of a rare gate (gatelog.py):
`1RB1RA_1LC0RB_1LD1LC_1RE1LF_0RA1RE_1RG0LE_1RZ0RE` — G is entered at steps
68, 155, 458, 1,577, 5,864, 22,631, 88,934, 352,613, 1,404,260, 5,604,707
with the block at 9, 18, 35, 68, 133, 262, 519, 1,032, 2,057, 4,106.
Once per doubling; the wait grows four times each visit. Only doubling, no
rows, and G reads the same symbol every time, so its halt never fires.

Running: Quick_Sim on the 1,245 tables with G ≤ 300 entries.

### Quick_Sim on the 1,245 rare-gate tables (8 seconds each) — result: nothing deep

498 proved infinite; 744 still running at rule level 0 or 1; 3 stop with
"expression too complex" (for example
`1RB1LA_1RC1RB_1LD0RF_1LE0LD_0LA1LE_0LG1RE_0RB1RZ`: 7 ones and an empty gap
that gets one exponent wider per cycle — a huge span, almost no ones).
No halts. No row machine. Not yet screened: the 2,975 tables with 301 to
2,000 gate entries.

### Quick_Sim on the last 2,975 gate-class tables (gate entered 301–2,000 times, 4 seconds each) — nothing deep

2,198 proved infinite; 774 still running at rule level 0 or 1; 3 halt, all
small: `1RB1LA_1LC0RF_1RD1LC_1LE0LD_1RA1RE_1RG0RC_1LE1RZ` (19,458 ones),
`1RB1LA_1LC0RF_1RD1LC_1LE0LD_1RA1RE_0RG0RC_0LC1RZ` (19,457),
`1RB1RA_0LC1LB_1LD1LC_1RE0LD_0RA0RF_1RG0RC_1LD1RZ` (1,592).
The gate class is now fully screened: no row machine in it.
