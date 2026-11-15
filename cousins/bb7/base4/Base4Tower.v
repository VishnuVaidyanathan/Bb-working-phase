(* A base-4 tower machine with 7 states that never halts

       1RB0LG_1LC1LB_0RD1LE_1RE1RD_0RF0RE_1LA1RF_---1LB

   It came out of the cousins search on the claimed BB(7) champion (the
   champion was found by Jeff Ketchersid).  Shawn Ligocki's Quick_Sim stopped
   on it with a power tower more than 500 levels high.

   Tape shape:   1^L  [C reads 1]  1^(n-1)        written (L, n).

     layer   (L+2, n)  ->  (L, 4n+4)       digits  2 5 9(n+1) 8 a 0 3 3 B(n)
     gate    (0,   n)  ->  (n, 4)          digits  2 5 8 b(n) a 1 d ...

   From a blank tape the machine is at (0, 2) after 2 steps.  L and n stay
   even, so the two rules apply for ever, and the halt wire (G reads 0) is
   never used.  Theorem [never_halts].

   Vishnu Vaidyanathan.  Coq 8.18, no axioms. *)

Require Import List Lia Arith.
Import ListNotations.

(* ---------- 1. The machine ---------- *)

Inductive St := A | B | C | D | E | F | G | Hlt.

(* state, cells to the LEFT (nearest first), cell under the head,
   cells to the RIGHT (nearest first).  [] means blank from here on. *)
Definition conf : Type := (St * list bool * bool * list bool)%type.

Definition act (w goR : bool) (s' : St) (l r : list bool) : conf :=
  if goR then
    match r with
    | []      => (s', w :: l, false, [])
    | x :: r' => (s', w :: l, x, r')
    end
  else
    match l with
    | []      => (s', [], false, w :: r)
    | x :: l' => (s', l', x, w :: r)
    end.

Definition step (c : conf) : conf :=
  let '(s, l, h, r) := c in
  match s, h with
  | A, false => act true  true  B l r     (* A0 -> 1RB *)
  | A, true  => act false false G l r     (* A1 -> 0LG *)
  | B, false => act true  false C l r     (* B0 -> 1LC *)
  | B, true  => act true  false B l r     (* B1 -> 1LB *)
  | C, false => act false true  D l r     (* C0 -> 0RD *)
  | C, true  => act true  false E l r     (* C1 -> 1LE *)
  | D, false => act true  true  E l r     (* D0 -> 1RE *)
  | D, true  => act true  true  D l r     (* D1 -> 1RD *)
  | E, false => act false true  F l r     (* E0 -> 0RF *)
  | E, true  => act false true  E l r     (* E1 -> 0RE *)
  | F, false => act true  false A l r     (* F0 -> 1LA *)
  | F, true  => act true  true  F l r     (* F1 -> 1RF *)
  | G, false => (Hlt, l, true, r)         (* G0 -> halt *)
  | G, true  => act true  false B l r     (* G1 -> 1LB *)
  | Hlt, _   => c
  end.

Fixpoint steps (n : nat) (c : conf) : conf :=
  match n with
  | 0   => c
  | S k => steps k (step c)
  end.

Definition state (c : conf) : St := let '(s, _, _, _) := c in s.

Definition blank : conf := (A, [], false, []).

Lemma steps_add : forall a b c, steps (a + b) c = steps b (steps a c).
Proof. induction a as [| a IH]; intros b c; simpl; [reflexivity | apply IH]. Qed.

(* ---------- 2. Reaching ---------- *)

Definition reach (c c' : conf) : Prop := exists k, steps k c = c'.

Lemma reach_refl : forall c, reach c c.
Proof. intros c. exists 0. reflexivity. Qed.

Lemma reach_trans : forall c1 c2 c3, reach c1 c2 -> reach c2 c3 -> reach c1 c3.
Proof.
  intros c1 c2 c3 [p Hp] [q Hq]. exists (p + q). rewrite steps_add. congruence.
Qed.

Lemma reach_step : forall c c', reach (step c) c' -> reach c c'.
Proof. intros c c' [k Hk]. exists (S k). exact Hk. Qed.

Ltac one := apply reach_step; cbn [step act].
Ltac by_lemma L := eapply reach_trans; [ apply L | ].

(* ---------- 3. Blocks ---------- *)

Notation ones := (repeat true).
Notation zeros := (repeat false).

Lemma rep_snoc : forall (x : bool) k (l : list bool),
  repeat x k ++ x :: l = x :: repeat x k ++ l.
Proof. induction k; intros l; simpl; [reflexivity | rewrite IHk; reflexivity]. Qed.

(* ---------- 4. The coils ---------- *)

(* B walks left over ones (digit 3) and stops on the cell x. *)
Lemma coilB : forall k x l r,
  reach (B, ones k ++ x :: l, true, r) (B, l, x, ones (S k) ++ r).
Proof.
  induction k as [| k IH]; intros x l r.
  - one. apply reach_refl.
  - one. cbn [repeat app]. by_lemma IH.
    rewrite rep_snoc. apply reach_refl.
Qed.

(* D walks right over ones (digit 7), to the blank end. *)
Lemma coilD : forall k l,
  reach (D, l, true, ones k) (D, ones (S k) ++ l, false, []).
Proof.
  induction k as [| k IH]; intros l.
  - one. apply reach_refl.
  - one. cbn [repeat]. by_lemma IH.
    rewrite rep_snoc. apply reach_refl.
Qed.

(* D walks right over ones, to a 0 that is on the tape. *)
Lemma coilD0 : forall k l r,
  reach (D, l, true, ones k ++ false :: r) (D, ones (S k) ++ l, false, r).
Proof.
  induction k as [| k IH]; intros l r.
  - one. apply reach_refl.
  - one. cbn [repeat app]. by_lemma IH.
    rewrite rep_snoc. apply reach_refl.
Qed.

(* E walks right and erases the ones (digit 9), to the blank end. *)
Lemma coilE : forall k l,
  reach (E, l, true, ones k) (E, zeros (S k) ++ l, false, []).
Proof.
  induction k as [| k IH]; intros l.
  - one. apply reach_refl.
  - one. cbn [repeat]. by_lemma IH.
    rewrite rep_snoc. apply reach_refl.
Qed.

(* F walks right over ones (digit b), to the blank end. *)
Lemma coilF : forall k l,
  reach (F, l, true, ones k) (F, ones (S k) ++ l, false, []).
Proof.
  induction k as [| k IH]; intros l.
  - one. apply reach_refl.
  - one. cbn [repeat]. by_lemma IH.
    rewrite rep_snoc. apply reach_refl.
Qed.

(* ---------- 5. One build round:  2 4 7(k) 6 8 a 0 3(k+3) ---------- *)

Lemma round : forall k l,
  reach (B, false :: l, false, ones k) (B, l, false, ones (k + 4)).
Proof.
  intros k l. one. one. by_lemma coilD. one. one. one. one.
  change (true :: true :: ones (S k) ++ false :: l)
    with (ones (S (S (S k))) ++ false :: l).
  by_lemma coilB. rewrite app_nil_r.
  replace (S (S (S (S k)))) with (k + 4) by lia. apply reach_refl.
Qed.

Lemma rounds : forall n k l,
  reach (B, zeros n ++ l, false, ones k) (B, l, false, ones (k + 4 * n)).
Proof.
  induction n as [| n IH]; intros k l.
  - replace (k + 4 * 0) with k by lia. apply reach_refl.
  - cbn [repeat app]. by_lemma round. by_lemma IH.
    replace (k + 4 + 4 * n) with (k + 4 * S n) by lia. apply reach_refl.
Qed.

(* ---------- 6. The layer:  (L+2, n) -> (L, 4n+4),  with n = m+1 ---------- *)

Lemma layer : forall m l,
  reach (step (C, true :: true :: l, true, ones m))
        (C, l, true, ones (4 * m + 7)).
Proof.
  intros m l. cbn [step act]. one. by_lemma coilE. cbn [repeat app].
  one. one. one. one. one.
  rewrite rep_snoc.
  change (false :: zeros m ++ true :: l) with (zeros (S m) ++ true :: l).
  change [true; true] with (ones 2).
  by_lemma rounds. one.
  replace (4 * m + 7) with (S (2 + 4 * S m)) by lia. apply reach_refl.
Qed.

(* ---------- 7. The gate:  (0, n) -> (n, 4),  with n = m+2 ---------- *)

(* F walks over the block, A cuts its last cell off, G and B come back. *)
Lemma gate_walk : forall m l,
  reach (F, false :: l, true, ones (S m))
        (B, l, false, ones (S m) ++ [false; true]).
Proof.
  intros m l. by_lemma coilF. one. one. destruct m as [| m].
  - one. apply reach_refl.
  - one. cbn [repeat app]. by_lemma coilB.
    change (true :: ones m ++ [true; false; true])
      with (ones (S m) ++ true :: [false; true]).
    rewrite rep_snoc. apply reach_refl.
Qed.

(* The block becomes the counter, and a new block of 4 is started. *)
Lemma gate_load : forall m l,
  reach (D, false :: l, true, ones (S m) ++ [false; true])
        (C, ones (S (S m)) ++ false :: l, true, ones 3).
Proof.
  intros m l. by_lemma coilD0. one. one. one. one. one. one. one. one.
  apply reach_refl.
Qed.

Lemma gate : forall m z, exists y,
  reach (step (C, zeros z, true, ones (S m)))
        (C, ones (S (S m)) ++ zeros (S y), true, ones 3).
Proof.
  intros m z.
  assert (H1 : exists y1, reach (step (C, zeros z, true, ones (S m)))
                                (B, zeros y1, false, ones (S m) ++ [false; true])).
  { destruct z as [| z].
    - exists 0. cbn [step act repeat]. one. apply (gate_walk m []).
    - exists z. cbn [step act repeat]. one. apply (gate_walk m (zeros z)). }
  destruct H1 as [y1 H1].
  assert (H2 : exists y, reach (B, zeros y1, false, ones (S m) ++ [false; true])
                               (C, ones (S (S m)) ++ zeros (S y), true, ones 3)).
  { destruct y1 as [| y1].
    - exists 0. one. one. apply (gate_load m []).
    - exists y1. one. one. apply (gate_load m (zeros y1)). }
  destruct H2 as [y H2]. exists y. eapply reach_trans; eassumption.
Qed.

(* ---------- 8. The shape is kept for ever ---------- *)

(* (L, n) with L = 2a and n = 2b+2; z explicit zeros on the far left. *)
Definition Inv (c : conf) : Prop :=
  exists a b z, c = (C, ones (2 * a) ++ zeros z, true, ones (2 * b + 1)).

Lemma start : steps 2 blank = (C, [], true, [true]).
Proof. reflexivity. Qed.

Lemma Inv_start : Inv (steps 2 blank).
Proof. exists 0, 0, 0. reflexivity. Qed.

Lemma progress : forall c, Inv c -> exists c', reach (step c) c' /\ Inv c'.
Proof.
  intros c (a & b & z & ->). destruct a as [| a].
  - (* gate *)
    replace (2 * b + 1) with (S (2 * b)) by lia.
    destruct (gate (2 * b) z) as [y Hy].
    eexists. split; [ exact Hy | ].
    exists (S b), 1, (S y).
    replace (2 * S b) with (S (S (2 * b))) by lia. reflexivity.
  - (* layer *)
    replace (2 * S a) with (S (S (2 * a))) by lia. cbn [repeat app].
    eexists. split; [ apply layer | ].
    exists a, (4 * b + 5), z. f_equal. f_equal. lia.
Qed.

(* ---------- 9. Never halts ---------- *)

Lemma late : forall k c, Inv c -> exists m, k <= m /\ Inv (steps m c).
Proof.
  induction k as [| k IH]; intros c H.
  - exists 0. split; [lia | exact H].
  - destruct (progress c H) as (c' & [j Hj] & H').
    destruct (IH c' H') as (m & Hm & Hm').
    exists (S j + m). split; [lia | ].
    rewrite steps_add. cbn [steps]. rewrite Hj. exact Hm'.
Qed.

Lemma halted_stays : forall k c, state c = Hlt -> state (steps k c) = Hlt.
Proof.
  induction k as [| k IH]; intros c H; [exact H | ].
  cbn [steps]. apply IH.
  destruct c as [[[s l] h] r]. cbn [state] in H. subst s. reflexivity.
Qed.

Lemma Inv_not_halted : forall c, Inv c -> state c <> Hlt.
Proof. intros c (a & b & z & ->). discriminate. Qed.

Theorem never_halts : forall k, state (steps k blank) <> Hlt.
Proof.
  intros k Hk.
  destruct (late k (steps 2 blank) Inv_start) as (m & Hm & Hinv).
  apply (Inv_not_halted _ Hinv).
  rewrite <- steps_add.
  replace (2 + m) with (k + (2 + m - k)) by lia.
  rewrite steps_add. apply halted_stays. exact Hk.
Qed.

(* A check that the table above is the real machine: step 334 of the run. *)
Example run_334 : steps 334 blank = (C, ones 18 ++ [false], true, ones 19).
Proof. reflexivity. Qed.

Print Assumptions never_halts.
