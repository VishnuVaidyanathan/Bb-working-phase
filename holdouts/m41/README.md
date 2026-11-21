# M41 : a holdout with a row of 41, read by hand (21 Nov 2026)

`1RB0LC_1LA1LE_0RD---_1LB1RE_0LA1LF_0RD0RG_0LD1RF` - one of Polygon's undecided 7-state holdouts (Discord BB community).
Its tape is written like Pavel Kropitz's: counters are runs of the word `10`, separators are `100`, and markers `1000`, `10000`, `100000`.

What it does (model41.py; rules read from thought experiments, rules41.py / learn41.py):
* last two counters: a | b -> a-1 | b+2 (transfer, so b + 2a);
* a counter c in front of a marker pays 1 per cycle and each cycle turns the last counter b into 2b+4;
* the marker widens (`1000` -> `10000` -> `100000`) as its counter runs out; at the widest, one separator of the row is used up and a
  fresh counter with four separators behind it appears - so each row word opens one more level;
* a counter left alone, B, becomes a NEW ROW: 2 and B+2 separators.  The boot does exactly this: 44 -> a row of 46.
Checked (tested): 34,224 steps between visits, from the real run (3 million steps) and 96 thought experiments, agree with the rules; 0 differ.
The tape builder reproduces 200 of 200 real steps.

Verdict (by this model, not a proof): there is no halting rule anywhere. 960 small starts were followed by the model; the only
situations without a rule were two more rewriting rules (now added), none a halt. When everything is used up, the last counter
becomes a fresh row again. So this machine most likely never halts: it is a stack without a gate, like our own 7-state stack.
Its halt (state C reading a 1) needs two 1s side by side at a visit, and its words never have that.
Not proved: that the rule set is complete for every reachable tape.
