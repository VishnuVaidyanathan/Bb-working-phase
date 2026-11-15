"""The boot of the claimed BB(7) champion, written by hand from the words of the big run.
   python3 boot_by_hand.py     -> 319 digits, equal to the machine: True"""
D = "0123456789abcd"

def machine(n):
    tm = "1RB0RG_1RC1RB_0RD1RZ_0LE0LD_0LF1LE_1RA1LF_1LC0RB".split("_"); T = {}
    for s in range(7):
        for r in range(2):
            x = tm[s][3 * r:3 * r + 3]; T[(s, r)] = (int(x[0]), 1 if x[1] == "R" else -1, ord(x[2]) - 65)
    tape = {}; p = 0; s = 0; out = ""
    for _ in range(n):
        r = tape.get(p, 0); out += D[2 * s + r]; w, m, q = T[(s, r)]; tape[p] = w; p += m; s = q
    return out

# the words (one digit per step, 2*state + symbol read)
def Round(n): return "2476" + "9" * n + "8a0" + "3" * n            # one build round
def Close(n): return "2468" + "b" * n                              # close of a block
def Count(k): return "a1d" + "3" * k + "2468" + "b" * (k + 1)      # one countdown line (lays one pair)
def Carry(i): return "a1c476" + "9" * i + "8b"                     # gate visit and carry (pairs -> unit)
def Down(a):  return Close(a) + "".join(Count(k) for k in range(a - 2, -1, -1))   # a block of a, counted down

boot = ("0"
        + Down(2)                        # cycle 1: block of 2 counted down
        + Carry(1)
        + "a1c47698a03"                  #          last carry opens a build
        + Round(4)
        + Down(7)                        # cycle 2: block of 7 counted down
        + Carry(1) + Carry(2) + Carry(2)
        + "a1c476998a033"                #          last carry opens a build
        + Round(5) + Round(8)
        + Close(11) + Count(9)           # cycle 3: a countdown starts ...
        + "a1d" + "3" * 8 + Round(9)     #          ... and turns into a build
        + "2476" + "9" * 13 + "8ba1")    #          walk to the gate: P = 13

if __name__ == "__main__":
    print(len(boot), "digits, equal to the machine:", boot == machine(len(boot)))
