# Overlap of wires: the pusher is the cutter (21 Nov)

Reasoning: a loop that moves s cells per pass stops in a different state for each remainder mod s, so every two-state loop is a free tester.
A. The look is the gate: the end routine already looks at a cell; that look halts for free if the cell depends on a count
   (Jeff Ketchersid's halt is one wire of this kind).
B. The pusher is the cutter: the two-wire left pusher (read 0 write 1, read 1 write 0) run over a solid block, with one extra wire
   "read 1, keep it", cuts the block into words `10`; the state it leaves in is the leftover test.

fillgate.c: fills the open wires of a skeleton and keeps tables that use every wire, do not halt within 1,000,000 steps from a blank
tape, and halt on some small tapes of their own form.  Calibration: Jeff 9/20, Pavel Kropitz 91/180, the two holdouts read by hand 0/180.

Skeleton 1: `1RB???_???0RA_1LD1LD_???0LC_0LF???_0LG???_0RA---`
(left pusher C0 D1, cutter wire C1 = 1LD, right adding sweep A0 B1, end routine E0 F0 G0 with the halt on its look; five wires open).
Result (tested): 83,636 tables use every wire; 306 have a gate that fires.  Shawn Ligocki's Quick_Sim, 20 s each: 292 proved never to halt;
14 not settled, of which 4 grow with one arrow (plain exponential counters) and 10 grow slowly.  Tower builders: 0.  Towers over towers: 0.
So the cut-by-pusher gives live gates cheaply, but with the holdout's end routine fixed around it no filling keeps a stack.
