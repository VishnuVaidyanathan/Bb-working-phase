# Tools used in the study

Plain Python 3, no packages, unless noted. Run them from this folder.

| script | what it does |
|---|---|
| `read.py TABLE STEPS` | digit counts, first appearance of each wire, the opening in blocks, the tape at the rare wires |
| `hand.py` | run a table from a hand-made tape (used from other scripts) |
| `profile.py FILE` | one-line profile of each machine in a file: fillers, storage, when all wires have appeared |
| `wire_jobs.py TABLE` or `--all ../machines.txt` | the jobs of every wire, read from its surroundings in the transcript |
| `t15_boot.py` | the opening of Pavel Kropitz's 6-state tower written by hand, compared with the machine |
| `pavel.py STEPS` | Pavel Kropitz's 7-state machine followed as groups and units |
| `pavel_gate.py trace/depth/gate` | Pavel's machine at its gate wire: the real run as numbers, the depth word, hand-tape tests of the gate |
| `pavel_compress.py STEPS` | Pavel's decimal transcript compressed, one line per gate visit (output for 100,000 steps is in `../pavel_first_100000_digits.txt`) |
| `pavel_plain.py STEPS [out.pdf]` | Pavel's decimal transcript with repeats folded as x(n) and nothing else, as text or a PDF |
| `catalogue.py` | builds the catalogue table from the profiles and from Quick_Sim outputs `qs_ID.out` in the current folder |
| `d1_from_stack.py "4,3"` | Quick_Sim on the 4-arrow machine, paused after the boot, with the stack changed |
| `d1_from_tape.py "01:1 11:1 10:4 11:1 10:3 11:1 01:8"` | the same, with the whole left side of the tape given |
| `late_wires_gen.py K [ids]` | each machine of `../machines.txt` with its last K wires freed |
| `late_wires_pipe.sh NAME` | plain run, never-halts prover, then Quick_Sim on a list of tables |
| `quick_sim_batch.py IN OUT SECONDS [flags]` | Quick_Sim on each table of a file; resumable |

The scripts that use Quick_Sim need Shawn Ligocki's `sligocki/busy-beaver` (`pip install gmpy2 psutil`) and

    export QUICK_SIM_DIR=/path/to/busy-beaver/Code

`late_wires_pipe.sh` needs `longrun` and `ncps` compiled from `../../cousins/bb7/src/` (`gcc -O2 -o longrun longrun.c`).
