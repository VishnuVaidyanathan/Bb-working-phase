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
