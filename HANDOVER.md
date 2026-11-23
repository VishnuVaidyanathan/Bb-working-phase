# Handover (23 Nov 2026, evening) — read this first

Written by the outgoing Claude session for the next one. Vishnu Vaidyanathan
directs the work; he does not code. Write to him in plain, simple English,
short, result first.

## Goal
A 7-state Turing machine, started from a **blank tape**, that halts with more
ones than Jeff Ketchersid's BB(7) champion
`1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB`.

## Standing rules (all still in force)
- Never use the affiliation "EDGI Research Lab". Commit as
  `Vishnu Vaidyanathan <vishnu@edgi.in>`; commit and push every new file.
- Do not cite Dennis Koshta unless he publishes.
- Credit: Jeff Ketchersid, mxdys, Shawn Ligocki (Quick_Sim), Pavel Kropitz,
  Andrew Ducharme, Marxen & Buntrock, Polygon (Discord, 711-holdout list),
  prurq (Discord, TM 721 analysis).
- Shawn's code is never in this repo (only called from scratch through
  `calc/quick_sim_with_remainders.py`). Polygon's list is never in the repo.
- Do not modify the BB5 repo. A machine counts only from a blank tape.
- Mark every statement proved / tested / observed. Report zeros with reasons.
  Record every failure.
- No foreground waiting: long jobs go in the background (2 h limit).
- Do not copy another machine's mechanism; do not edit Jeff's table. Search
  is allowed only inside a frame designed by hand. "Near" means near in the
  **transcript**, not within a few wires of a table.

## The method as it stands (Vishnu's)
story → **transcript** → table.
- Digits: A0=0 A1=1 B0=2 B1=3 … F0=a F1=b G0=c G1=d. Even digit = read a 0.
- The even digits make **one closed loop from A0**; on a blank tape the
  machine starts by walking it, so the start costs no wire.
- After a turn the head meets a cell the loop wrote; what the loop digits
  write decides where the first odd digit comes in.
- A repeated digit is a filler and points to its own state; its end is its
  even partner on the loop.
- A **door** = an odd half of a loop state, fired when the loop is one digit
  out of phase (e.g. the take was missing because a store was empty).
- States off the loop sit behind the door. A **gate** behind the door should
  be entered rarely; the halt rarer still.
- Even digits give, odd non-filler digits take; the round's arithmetic can be
  read off its digits.
Files: `compile/transcript_bb5.md`, `compile/round_transcript.md`,
`compile/overlap_grammar.md`, `jeff/transcript.md`, `pavel/transcript.md`.

## Tools (all in the repo)
- `compile/sheet.py` + `compile/batch.c`: a hand sheet → every table → run.
- `compile/transcript.py`, `compile/tape2.py`: run a table on a hand tape and
  print the transcript in digits (one- or two-cell gaps).
- `design/transcript_class/cls.c` (loop of six), `cls5g.c` (loop of five,
  door → F → G, halt on G), `frame5.py` (hand round fixed, halt on C1, F and
  G free), `pay.c`, `gate.c`; `design/counter/gatelog.py`, `runout*.py`;
  `design/eight/show.c`, `nbn.c`.
- Quick_Sim: env `QUICK_SIM_DIR=<scratch>/tools/busy-beaver/Code`, run
  `calc/quick_sim_with_remainders.py TABLE --no-steps -r --exp-linear-rules
  --exp-meta-linear-rules [-n 4]`. The scratch folder may be gone in a new
  session; then Shawn's code must be fetched again into scratch.
- Known traps: a C tape must be longer than twice the step count; clear tape
  buffers between tables (a bug of this kind cost an hour on 23 Nov).

## Results that matter
- Jeff's machine: closed even loop of six, three fillers, one take (D1), one
  door (A1) into G, halt on C1. Two rows: a short first row ends with a lone
  block of 40 → a row of twenty stores of 2 (about 20 arrows) → halt, because
  a new row starts with an odd block (a one-tick clock, not luck).
- Tables within two wires of Jeff's: nothing bigger (57,214 tables).
- Transcript class, loop of six (18,977,338 tables): Jeff's table, its
  disguise (G0 `0LD`), one smaller cousin
  `1RB1RA_0RC1RZ_0LD0LC_0LE1LD_0RF1LE_1RA1RG_1LC0RA` (steps of two arrows,
  end unknown). Nothing bigger.
- Gate class, loop of five (578,417 kept): 4,220 pass the gate test; Quick_Sim
  on the 1,245 rarest was running at handover.
- Hand machine of the loop-of-five type, starts from blank, triples for ever:
  `1RB1LF_1RC1RB_0RD---_0LE0LD_1LA1LE_0LG1LF_0LA1RZ`. Round, door, landing
  fit; the row is never used (landing is free). See
  `design/transcript_class/hand5.md`.
- 8 states: `1RB1RG_1RC1RB_0LD0LH_0RA1LD_1LA1RF_1RZ1RA_0RH0RB_1LC1LH` and
  `1RB1LF_1LC1LF_1LD1LC_0RE0RH_0LA1RE_0LH0LC_1RZ1LB_1RD1RH` start from blank
  and reach four arrows in Quick_Sim. Three nested counters (fast 16, slow
  row of single cells, slow refilled from the block). No halt seen; probably
  infinite (not proved). See `design/counter/README.md`.
- 9 states: tower of towers that halts from blank, by arithmetic only (see
  `design/squeeze/`).

## Open at handover
1. Quick_Sim screening of the gate class (1,245 tables, then 2,975 more).
2. `frame5.py` frame: hand round + halt on C1 + F and G free (2,458,624
   tables): can **pay** and **lay** both fit in F and G? By hand: pay fits in
   4 wires, land fits in 4, not both in 5 yet.
3. The idea to design next: the halt one level above the rarest repeating
   event — "when the slow counter runs out, take one cell from a small third
   counter beside home; halt when it is empty".
Outputs of 1 and 2 were in the scratch folder `…/scratchpad/eight/`
(gq*.qs, f5.*); if scratch is gone, rerun from the tools above.

## Added just before the session ended (tested)
- `frame5.py` frame result: 2,458,624 tables from a blank tape. 745,141 halt
  by 20,000 steps (largest: step 1,231, 35 ones). 10,731 keep 3 to 60 runs;
  of those, 4,039 show a store paying at 15+ of 40 checks over 2,000,000
  steps (3,993 with 6 or more runs). **Not yet screened by Quick_Sim.**
  The 4,039 tables are saved in
  `design/transcript_class/frame5_candidates.txt`. This is the first thing
  to do next: Quick_Sim on them, then read the deep ones by transcript.
- The 1,245 rare-gate tables of the gate class are saved in
  `design/transcript_class/gate_class_rare_candidates.txt`. Their Quick_Sim
  screening was still running when the session ended; rerun it.

- Gate class, the 1,245 rare-gate tables: Quick_Sim done, **nothing deep** (498 infinite, 744 shallow and undecided, 3 gap-growers with 7 ones, no halts). Left: the 2,975 tables with 301-2,000 gate entries.
- Quick_Sim on the frame5 candidates: first 2,020 (strongest first) started 23 Nov evening; see design/transcript_class/README.md for what came out.

- frame5 candidates fully screened (23 Nov, night): **no row machine**. 4,019 of 4,039 proved infinite; 14 single-exponential growers undecided; details in design/transcript_class/hand5.md section 7. Conclusion: pay and lay do not both fit behind the door on top of this hand round; change the round next (where the door fires, who does the take).
- Last group of the gate class (2,975 tables, gate entered 301-2,000 times): Quick_Sim was started 23 Nov night; result, if finished, is at the end of design/transcript_class/README.md.
