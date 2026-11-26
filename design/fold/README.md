# Fold: every drag as one jump

- `r.c` runs Jeff Ketchersid's machine with each filler run (3, 9, b) taken as one jump. Checked digit for digit against a plain run (862,559 digits).
- `fold.c LIMIT < tables` does the same for any table (a filler = a wire that points to its own state) and reports, for each digit, whether the gaps between its firings multiply.
- Blind spot: Pavel Kropitz's machine has two-digit fillers and fails this test.

## Results (26 Nov)

- BB5 champion (Marxen & Buntrock): 47,176,870 steps fold to 55,118 digits; rounds of `0 2 4 6`, then about 5/3 as many `1 5 9`.
- Jeff: tape at each visit to G is `1 0 [G] 0 1^n 00 1^m 0000 (1100)^k 1`; n -> 3n+6, m -> m-2, k -> k-1 when m runs out (observed, not proved).
- 84-start search, 5,577 tables with a laying of 100+ repeats (`top5577_fold.txt`): 6 halt, 282 run away, 2 too wide, 4,966 no growing digit, 321 grow.
- The 321 through Shawn Ligocki's Quick_Sim, 10 s each (`grow321_quicksim.txt`): 113 proved to run forever, 208 still running with only level 1 rules (188 with a tape of 10^4,000 to 10^13,000 ones, 20 not yet growing). None above level 1. No machine bigger than Jeff's.
