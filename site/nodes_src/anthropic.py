# Node explainers for the Anthropic project. Written as Python data so the YAML is always valid;
# tools/write_nodes.py turns each entry into site/nodes/<id>.md.
A = "Anthropic."
NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=A + id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("ethIsFalse", "ETH is false (Anthropic)",
 "**The surprise:** a famous hardness assumption, which hundreds of papers rely on, is stated in Lean from scratch and proved *false*, using only Lean's three standard axioms. For every δ > 0, some Turing machine decides 3-SAT on n variables within c·2^{δn} steps.",
 r"""
## Plain English

**Theorem (`MainResults.ethIsFalse`).** The Exponential Time Hypothesis, as defined in [ETH](#/node/Anthropic.ETH), is false.

Unfolded: let s₃ be the infimum of all δ ≥ 0 such that *some* deterministic multi-stack Turing machine decides 3-SAT on n variables within c·2^{δn} steps, for some constant c and every n (see [s](#/node/Anthropic.s) and [InTime](#/node/Anthropic.InTime)). ETH says s₃ > 0. The theorem says s₃ = 0: **for every δ > 0 there is such a machine**.

In the authors' words (Challenge.lean line 11): *"The hypothesis (Impagliazzo and Paturi) says s₃ > 0. The theorem says that this fails: s₃ = 0, that is, for every δ > 0 there is such a machine."*

Why this matters: ETH is the standard assumption behind most "this problem needs exponential time" results in fine-grained complexity. The paper reports a literature search that found more than 800 papers with at least one result proved only under ETH or a stronger hypothesis.

What the result is **not**: the paper itself stresses that the bound is "purely asymptotic". For 3-CNFs with m = 5n clauses, it beats the 2ⁿ of brute force only when n > 10^10000. It says nothing about solving formulas in practice, and it does not touch P vs NP.

### How the Lean proof is put together

The proof in `Solution.lean` is one line (Solution.lean line 40). It takes the [Main Theorem](#/node/Anthropic.mainTheorem) and applies two general arguments to it, each proved for *every* machine with the right bound. The outline below follows them.
""",
 [q("What does `ETHIsFalse` say about s₃, the infimum of the achievable exponents δ for 3-SAT?",
    ["s₃ > 0", "s₃ = 0", "s₃ = 1", "s₃ is infinite"], 1,
    "`ETHIsFalse := ¬ ETH` and `ETH := 0 < s 3`. As s₃ is an infimum of non-negative numbers, ¬(0 < s₃) means s₃ = 0."),
  q("Which model of computation does the Lean statement use?",
    ["a random-access machine", "Mathlib's finite multi-stack Turing machines (`FinTM2`)", "Boolean circuits", "a Lean function, with its evaluation steps counted"], 1,
    "`InTime` asks for a `TM2ComputableAux Bool Bool`, i.e. a `FinTM2` machine, with every stack alphabet finite."),
  q("Must one machine work for every δ > 0?",
    ["Yes, one machine for all δ", "No, the machine may depend on δ (and on k)"], 1,
    "`InTime k δ` starts with `∃ M`, after δ is fixed. The Main Theorem is stronger (one machine for everything), but `ETHIsFalse` only needs a machine for each δ."),
  q("Which axioms does the proof use, according to `scripts/PrintAxioms.lean` and the project's CI?",
    ["propext, Classical.choice, Quot.sound only", "those three plus `sorryAx`", "those three plus a custom axiom for the Turing-machine simulation", "`native_decide`"], 0,
    "The README says the axiom check prints exactly the three standard axioms, and the repository's CI (Comparator with the independent `nanoda` kernel) passed on commit 16a5ce4. This site has not rebuilt it itself; see the Trust page.")],
 caveats=[
  "The link from Mathlib's Turing machines to 'an algorithm in the usual sense' is an argument in the comment at the top of MainResults.lean (a RAM simulates the machine with bounded overhead, and re-encoding the formula takes polynomial time). It is standard, but it is not part of the Lean statements or proofs.",
  "Clauses are lists, and no clause may be written twice (`IsKCNF` uses `List.Nodup`), so a 3-CNF on n variables has at most (2n+1)³ clauses. That is why a time bound in n alone makes sense.",
  "ETH is stated for deterministic machines. The authors note (outside Lean) that refuting the deterministic form also refutes the randomized form.",
  "This site has not built the Lean. The claim that it checks rests on the authors' CI run (passed, 26 Oct 2026, 11:31 PM ET) and on our grep for `sorry`/`axiom` (none outside Challenge.lean)."],
 widgets=[{"type": "walkthrough", "title": "How Solution.lean proves it (Solution.lean, lines 36-40)", "config": {"steps": [
   {"text": "Start from the Main Theorem: one machine counts the satisfying assignments of every k-CNF within 2^{C·min{km/√log m, k²n·log log n/√log n}} steps", "lean": "CountedRoute.mainTheoremHolds", "link": "Anthropic.mainTheorem",
    "note": "This is where all the work is: about 150,000 lines under proof/. It needs the formula's variables to be named x₀ … x_{n−1} in order of use, and every variable to occur."},
   {"text": "Rename variables: a front end that renames the variables that occur gives the same bound for formulas with any names, plus a polynomial in the input length", "lean": "NamesInOrder.generalFormFollowsAsPropositions",
    "note": "proof/maintheorem/NamesInOrder/General.lean lines 61-69. It wraps the machine with a renaming front end and absorbs the overhead into the constant."},
   {"text": "Wrap the counter: a front end, a simulation and a last step give one machine that decides 3-SAT within c·2^{δn} steps for every δ > 0", "lean": "Wrap.countingBoundImpliesFailureOfETH",
    "note": "proof/machines/Wrap/Main.lean lines 113-117. 'Count > 0' answers satisfiability; the polynomial is absorbed because 2^{o(n)}·poly(n) is below c·2^{δn}."},
   {"text": "Pick the third of five conclusions: ¬ ETH", "lean": ".2.2.1",
    "note": "`Wrap.OneMachineEveryDeltaAndETHFails` bundles five statements. The third, `¬ Sat3.ETH_TM`, unfolds to `MainResults.ETHIsFalse`. Lean checks that by unfolding definitions."}]}}])

node("mainTheorem", "Main Theorem (Anthropic): one machine counts k-SAT solutions in time 2^o(n)",
 "**The surprise:** a *single* Turing machine, with *one* constant C that does not depend on k, counts the satisfying assignments of every k-CNF within 2^{C·min{km/√(log m), k²·n·log log n/√(log n)}} steps, which is 2^{o(n)} for each fixed k.",
 r"""
## Plain English

**Theorem (`MainResults.mainTheorem`).** There is one deterministic multi-stack Turing machine (all stack alphabets finite) and one constant C, both chosen *before* k and the formula, such that:

for every k ≥ 1, every n ≥ 4, and every formula φ on the variables x₀ … x_{n−1} in which

- every variable occurs ([AllOccur](#/node/Anthropic.AllOccur)),
- every clause has at most k literals and no clause is written twice ([IsKCNF](#/node/Anthropic.IsKCNF)),
- there are m ≥ 2 clauses,

the machine, started on the code of (k, φ) ([encInput](#/node/Anthropic.encInput)), halts with the number of satisfying assignments of φ ([numSat](#/node/Anthropic.numSat)), written in n + 1 bits, lowest bit first ([binary](#/node/Anthropic.binary)), within [timeMin](#/node/Anthropic.timeMin) C k m n = ⌊2^{C·min{km/√(log m), k²·n·log log n/√(log n)}}⌋ steps ([CountsWithin](#/node/Anthropic.CountsWithin)). Here log is log₂.

The paper's wording (Theorem 1): *"There is a deterministic algorithm that, given a k-CNF with m clauses in which n variables occur, computes the number of satisfying assignments of these n variables in time 2^{O(min{k²n log log n/√log n, km/√log m})}, where the O(·) hides an absolute constant."*

Two things are stronger than refuting ETH needs. First, the machine is **universal**: one machine for every k and every formula, not one per δ. Second, the bound has an explicit o(n) **rate**, and the time has **no extra polynomial factor**.

### The idea, in the authors' condensed form (README)

> Let 2^{e(K)·K²λ}·poly(λ) be the time to contract tensor networks on K_K with λ bits per edge and arbitrary node tensors. Then e(9K^16) ≤ 0.9·e(K) + O(1/K). Put the nodes on a grid: the two diagonals of each rectangle form a swap. Per bit, SWAP = I − 2·singlet; grouping by the number of singlets gives λ+1 operators with (row rank)·(column rank) ≤ 12^λ. …

In plain words: counting solutions is a *tensor network contraction* on a complete graph. The proof finds a way to lower the exponent of contracting such networks by a constant factor each time it zooms out, which compounds to a subexponential bound.
""",
 [q("Which comes first in the statement: the machine M, or the width k?",
    ["k, so each k gets its own machine", "M (and C), so one machine serves every k"], 1,
    "`∃ (M …) (C : ℕ), … ∀ (k n : ℕ) (φ : CNF n), …`. The existential is outside the universal."),
  q("Which formulas does the Main Theorem say nothing about?",
    ["formulas with a variable that does not occur, or with fewer than 2 clauses, or fewer than 4 variables", "formulas with an empty clause", "formulas with both x and ¬x in a clause", "3-CNFs"], 0,
    "The hypotheses are `1 ≤ k`, `IsKCNF k φ`, `2 ≤ φ.length`, `4 ≤ n`, `AllOccur φ`. An empty clause or a clause with x and ¬x is still allowed. The docstring says: 'Nothing is said about any other input word.'"),
  q("What is the output?",
    ["one bit: satisfiable or not", "the number of satisfying assignments, in n + 1 bits, lowest bit first", "a satisfying assignment", "the count modulo 2"], 1,
    "`CountsWithin` asks for output `binary n (numSat φ)`: the lowest n + 1 bits of the count, which is at most 2ⁿ, so nothing is lost."),
  q("Is k part of the input?",
    ["Yes: the input starts with 1ᵏ 0", "No: k is fixed in advance"], 0,
    "`encInput k φ = 1ᵏ 0 ++ encClauses k φ`. This is what lets one machine handle every k.")],
 caveats=[
  "The bound is stated for formulas in which every variable occurs, with variables x₀ … x_{n−1}. The step to formulas with arbitrary variable names (with a polynomial added) is proved in Lean on the way to `ethIsFalse`, but it is not this statement.",
  "log is `Real.logb 2`, of x itself (not x + 1). At m = 1 the term km/√(log m) would divide by zero, which is why m ≥ 2 is assumed; at n < 4, log log n < 1.",
  "The authors say a reader should compare MainResults.lean with the paper by hand, and the paper's Appendix E lists the differences. This site's review has not yet gone through Appendix E line by line.",
  "The README notes that a condensed prompt lets a model 'rederive the refutation of ETH'. That is a claim about AI models, not part of the mathematics, and this site has not tested it."],
 widgets=[{"type": "walkthrough", "title": "The proof route, as the paper is organised", "config": {"steps": [
   {"text": "§3–5: count solutions as the value of a tensor network on a complete graph, and bound the cost of computing that value (Lemma 1, Lemma 2, Proposition 3)",
    "note": "Lean: proof/networks (Groundwork, Paper, Eight, Value, Variance). The 'eight-square identity' supplies the low-rank pieces (Lemma 2)."},
   {"text": "§6: Theorem 2, for every δ > 0, 3-SAT in time O(2^{δn}). This already refutes ETH, with a simpler argument",
    "note": "Lean: proof/threesat. Not used by Solution.lean's route to the Main Theorem, but proved separately."},
   {"text": "Appendices A–B: the bound 2^{O(km/√log m)} in the number of clauses, via a recursion (Theorem A) on pieces with parameters (ρ, c)",
    "note": "Lean: proof/rates (PaddedDescent, ClauseBound, PiecesCounted, CountedRecursion …)."},
   {"text": "Appendix C: count-preserving sparsification",
    "note": "Lean: proof/sparsification. Reduces general formulas to ones where each variable occurs in few clauses."},
   {"text": "Appendix D: the bound 2^{O(k²n log log n/√log n)} in the number of variables",
    "note": "Lean: proof/variables (parity checks, the cut-off lemma, RecursionToBound …)."},
   {"text": "Take the smaller of the two bounds, on one machine, and convert operation counts to Turing-machine steps",
    "lean": "CountedRoute.mainTheoremHolds",
    "note": "proof/maintheorem/CountedRoute/Main.lean line 92, then Solution.lean line 44. Lean accepts the term by unfolding definitions to `MainResults.MainTheorem`."}]}}])

node("ETHIsFalse", "ETHIsFalse: the proposition 'ETH is false'",
 "Just `¬ ETH`. Because s₃ can never be negative, this is the same as saying s₃ = 0: arbitrarily small exponents δ are achievable for 3-SAT.",
 r"""
## Plain English

`ETHIsFalse : Prop := ¬ ETH`, the negation of [ETH](#/node/Anthropic.ETH).

ETH says `0 < s 3`. Its negation says `s 3 ≤ 0`, and since [s](#/node/Anthropic.s) is an infimum of values in [0, ∞], that means s₃ = 0. Equivalently, for every δ > 0 there is some δ' < δ such that `InTime 3 δ'` holds, and since `InTime` gets weaker as δ grows, `InTime 3 δ` holds for every δ > 0.
""",
 [q("`ETHIsFalse` is defined as…", ["`s 3 = 0`", "`¬ ETH`", "`∀ δ > 0, InTime 3 δ`", "`MainTheorem`"], 1, "MainResults.lean line 122: `def ETHIsFalse : Prop := ¬ ETH`. The other forms are equivalent readings, not the definition."),
  q("Why does ¬(0 < s₃) give s₃ = 0?", ["because s₃ is a natural number", "because s₃ is an infimum of non-negative values, so s₃ ≥ 0", "it does not; s₃ could be negative"], 1, "`s` takes values in ℝ≥0∞, which has no negative numbers."),
  q("Does `ETHIsFalse` require one machine for all δ?", ["Yes", "No"], 1, "No. It only rules out a positive lower bound on the achievable δ's, and each δ may have its own machine.")])

node("ETH", "ETH: the Exponential Time Hypothesis, as a Lean proposition",
 "ETH is stated as `0 < s 3`: some fixed exponent δ > 0 is unbeatable for 3-SAT. That is Impagliazzo and Paturi's form, restricted to deterministic Turing machines.",
 r"""
## Plain English

`ETH : Prop := 0 < s 3`, where [s](#/node/Anthropic.s) 3 is the infimum of the exponents δ for which 3-SAT on n variables can be decided in time O(2^{δn}).

The docstring cites Impagliazzo and Paturi, *On the complexity of k-SAT*, J. Comput. Syst. Sci. 62 (2001). The paper defines ETH as "s_k > 0 for all k ≥ 3" and notes that this is the same as s₃ > 0. The Lean uses the k = 3 form. Refuting it refutes the "all k" form too, because the k = 3 case fails.

**Why this form is the right one to refute.** It is stated about machines in Mathlib's model, which (by the head comment of MainResults.lean) are at least as slow as algorithms in the usual sense, up to polynomial factors. So s₃ in the usual sense is at most s₃ as defined here, and "s₃ = 0 here" gives "s₃ = 0 there".
""",
 [q("Which k does the Lean ETH use?", ["k = 2", "k = 3", "every k ≥ 3"], 1, "`ETH := 0 < s 3`."),
  q("If 3-SAT could be decided in time 1.0001ⁿ but not faster, would ETH (as defined) hold?", ["Yes", "No"], 0, "Then s₃ = log₂ 1.0001 > 0, so `0 < s 3`."),
  q("Does the Lean ETH speak about randomized algorithms?", ["Yes", "No, deterministic machines only"], 1, "`InTime` asks for a deterministic `FinTM2` machine. The authors remark, outside Lean, that refuting the deterministic form also refutes the randomized one.")],
 caveats=["The translation from 'machines in Mathlib's model' to 'algorithms in the usual sense' is an informal (standard) argument, given in the head comment of MainResults.lean."])

node("s", "s k: the best achievable exponent for k-SAT",
 "s k is the infimum of all δ ≥ 0 such that some machine decides k-SAT in c·2^{δn} steps. It lives in [0, ∞], and is ∞ if no δ works.",
 r"""
## Plain English

`s k := ⨅ (δ : ℝ≥0) (_ : InTime k δ), (δ : ℝ≥0∞)`: the infimum, over all non-negative reals δ for which [InTime](#/node/Anthropic.InTime) k δ holds, of δ.

The infimum is taken in the extended non-negative reals, so an empty set of δ's gives ∞. For k = 3, brute force already gives δ = 1, so s₃ ≤ 1.
""",
 [q("What is `s k` if no δ works?", ["0", "1", "∞"], 2, "An infimum over the empty set in ℝ≥0∞ is ⊤ = ∞."),
  q("Can `s k` be negative?", ["Yes", "No"], 1, "δ ranges over ℝ≥0 and the value lives in ℝ≥0∞."),
  q("If `InTime 3 δ` holds for every δ > 0, what is `s 3`?", ["0", "1", "it depends on c"], 0, "The infimum of all positive reals is 0.")])

node("InTime", "InTime k δ: some machine decides k-SAT in time O(2^{δn})",
 "One machine with finite alphabets and one constant c decide every k-CNF on n variables within ⌊c·2^{δn}⌋ steps, for **every** n. The machine and c may depend on k and δ.",
 r"""
## Plain English

`InTime k δ` holds when there are a machine `M` (a `TM2ComputableAux Bool Bool`, every stack alphabet finite) and a natural number `c` such that `M` [decides k-SAT](#/node/Anthropic.DecidesKSat) within ⌊c·2^{δn}⌋ steps on every formula with n variables.

There is no "for large enough n" and no extra polynomial factor: the bound c·2^{δn} must hold for every n. That is equivalent to the usual O(2^{δn}), since finitely many small cases are absorbed into c.
""",
 [q("Can the machine in `InTime k δ` depend on δ?", ["Yes", "No"], 0, "`InTime k δ := ∃ M c, …`, so M is chosen after k and δ."),
  q("Does the time bound depend on the number of clauses m?", ["Yes", "No, only on n"], 1, "The bound is `fun n => ⌊c * 2^(δ n)⌋₊`. That works because no clause may repeat, so m ≤ (2n+1)^k."),
  q("Why is `∀ i, Finite (M.tm.Γ i)` there?", ["Mathlib already requires it, so it is redundant", "Mathlib only requires the input alphabet to be finite; this makes every stack alphabet finite, as for a textbook machine", "it bounds the number of states"], 1, "The head comment of MainResults.lean explains: 'Of the stack alphabets, Mathlib requires only that of the input stack to be finite.'")])

node("DecidesKSat", "DecidesKSat: the machine answers k-SAT correctly and on time",
 "Started on the code of any k-CNF φ, the machine halts within t(n) steps with one output bit, which is 1 exactly when φ is satisfiable. k is fixed, not part of the input.",
 r"""
## Plain English

`DecidesKSat k M t`: for every n and every φ with [IsKCNF](#/node/Anthropic.IsKCNF) k φ, there is a bit b with (b = true ↔ φ is [satisfiable](#/node/Anthropic.Satisfiable)) such that `M`, started on [encClauses](#/node/Anthropic.encClauses) k φ (translated through the machine's input alphabet), outputs `[b]` within t(n) steps (`TM2OutputsInTime`).

`TM2OutputsInTime` is Mathlib's: started with the input on the input stack and every other stack empty, the machine halts after at most t steps with the output on its output stack, every other stack empty, and its internal state back at its initial value.
""",
 [q("Is k part of the input word for `DecidesKSat`?", ["Yes", "No"], 1, "The input is `encClauses k φ`: n in unary, then the clauses. k is fixed by the statement."),
  q("Which formulas must the machine handle?", ["only those with every variable occurring", "every φ with `IsKCNF k φ`, any number of clauses", "only 3-CNFs with at least 2 clauses"], 1, "`∀ (n : ℕ) (φ : CNF n), IsKCNF k φ → …`. No other condition."),
  q("What does the output look like?", ["a satisfying assignment", "one bit", "the number of solutions"], 1, "`some ([b].map M.outputAlphabet.invFun)`: one bit.")])

node("IsKCNF", "IsKCNF k φ: clauses of width at most k, none written twice",
 "A k-CNF here is a list of clauses, each of at most k literals, with **no clause repeated**. The no-repeat condition is what makes a time bound in n alone possible.",
 r"""
## Plain English

`IsKCNF k φ := (∀ C ∈ φ, C.length ≤ k) ∧ φ.Nodup`.

The docstring explains the choices. A clause is a list, so it may be empty (then it is false), may repeat a literal or hold both x and ¬x, and the same literals in another order make a different clause. So a k-CNF on n variables has at most (2n+1)^k clauses. And: *"Without this, no time bound in n alone could hold: before halting, a machine must pop nearly all of its input, a bounded number of symbols per step."*
""",
 [q("Is the formula `[[x₀, x₁], [x₁, x₀]]` allowed by `IsKCNF 2`?", ["Yes: the two clauses are different lists", "No: they are the same clause"], 0, "Lists in a different order are different, so `Nodup` holds."),
  q("Why forbid repeated clauses?", ["to make the problem easier", "otherwise the input could be arbitrarily long for fixed n, and no bound in n alone could hold", "Mathlib requires it"], 1, "The machine must read its input, so the input length must be bounded in n."),
  q("Is an empty clause allowed?", ["Yes", "No"], 0, "Its length is 0 ≤ k. An empty clause is false, so the formula is unsatisfiable.")])

node("CNF", "CNF n: a formula as a list of clauses",
 "A formula on variables x₀ … x_{n−1} is a list of clauses, and a clause is a list of literals. Order and repetition are allowed at this level; `IsKCNF` restricts them.",
 r"""
## Plain English

`CNF n := List (List (Lit n))`: an AND of clauses, each an OR of [literals](#/node/Anthropic.Lit).
""",
 [q("A clause is a…", ["Finset of literals", "List of literals", "function from variables to Bool"], 1, "`List (Lit n)`."),
  q("What is the empty formula `[]`?", ["always false", "always true", "not a CNF"], 1, "An AND of no clauses is true. Every assignment satisfies it."),
  q("Which condition stops clauses from repeating?", ["CNF itself", "IsKCNF (`List.Nodup`)"], 1, "CNF is just a list type; `IsKCNF` adds `φ.Nodup`.")])

node("Lit", "Lit n: a literal xᵢ or ¬xᵢ",
 "A literal is a pair (i, b): the variable xᵢ if b is true, its negation if b is false.",
 r"""
## Plain English

`Lit n := Fin n × Bool`. The pair (i, true) is xᵢ and (i, false) is ¬xᵢ, for 0 ≤ i < n.
""",
 [q("What is (2, false)?", ["x₂", "¬x₂", "x₃"], 1, "b = false means the negated variable."),
  q("How many literals are there on n variables?", ["n", "2n", "2ⁿ"], 1, "n choices of i times 2 choices of b."),
  q("Are the variables numbered from 0 or 1 in Lean?", ["0 (x₀ … x_{n−1})", "1 (x₁ … xₙ)"], 0, "`Fin n` = {0, …, n−1}. The paper numbers from 1.")])

node("Satisfiable", "Satisfiable φ",
 "Some assignment of true/false to the variables makes at least one literal of every clause true.",
 r"""
## Plain English

`Satisfiable φ := ∃ a : Fin n → Bool, ∀ C ∈ φ, ∃ l ∈ C, a l.1 = l.2`.

A literal (i, b) is true under `a` when `a i = b`.
""",
 [q("Is a formula with an empty clause satisfiable?", ["Yes", "No"], 1, "An empty clause has no literal to make true."),
  q("When is the literal (i, b) true under a?", ["when a i = true", "when a i = b", "when a i ≠ b"], 1, "`a l.1 = l.2`."),
  q("Is the empty formula satisfiable (for any n)?", ["Yes", "No"], 0, "There are no clauses, so `∀ C ∈ []` holds; any assignment works (for n = 0 there is exactly one).")])

node("encClauses", "encClauses: how a k-CNF is written on the input tape",
 "n in unary, then for each clause exactly k fixed-width slots of ⌊log₂(2n)⌋+1 bits. Its length is polynomial in n, which is what lets a 2^{o(n)} bound absorb the time to read the input.",
 r"""
## Plain English

`encClauses k φ` is the bit string: n ones, a zero, then for each clause, k positions of `Nat.log2 (2 * n) + 1` bits each, each holding the [slot](#/node/Anthropic.slot) number of that position (0 for empty, 2i+1 for ¬xᵢ, 2i+2 for xᵢ), lowest bit first. A clause with fewer than k literals is padded with empty positions.

Since clauses don't repeat and each has at most k literals, the length is at most n + 1 + (2n+1)^k · k · (log₂(2n)+1), which is polynomial in n for fixed k.
""",
 [q("How is n written?", ["in binary", "in unary: n ones then a zero"], 1, "`List.replicate n true ++ false :: …`."),
  q("How many bits does each clause take?", ["k · (⌊log₂(2n)⌋ + 1)", "its own length times log n", "exactly 3"], 0, "k positions of `Nat.log2 (2 * n) + 1` bits each."),
  q("Which slot number encodes x₃ (positive)?", ["7", "8", "6"], 1, "`2 * 3 + 1 + true.toNat = 8`. ¬x₃ is 7, and 0 means an empty position.")])

node("slot", "slot: the number written for one position of a clause",
 "0 for an empty position, 2i+1 for ¬xᵢ, 2i+2 for xᵢ. Every number is below 2n+1, so ⌊log₂(2n)⌋+1 bits suffice.",
 r"""
## Plain English

`slot none = 0` and `slot (some (i, b)) = 2i + 1 + (if b then 1 else 0)`.
""",
 [q("slot (some (0, false)) = ?", ["0", "1", "2"], 1, "2·0 + 1 + 0 = 1."),
  q("Why does 0 mean 'empty'?", ["so short clauses can be padded to k positions", "because x₀ is special"], 0, "`encClauses` writes k positions per clause; missing ones are `none`, i.e. 0."),
  q("Largest slot value for n variables?", ["2n", "2n − 1", "n"], 0, "x_{n−1} gives 2(n−1) + 2 = 2n.")])

node("AllOccur", "AllOccur φ: every variable occurs",
 "Each of x₀ … x_{n−1} appears in some clause, positively or negatively. Then n ≤ km, so a bound in m also bounds things in n.",
 r"""
## Plain English

`AllOccur φ := ∀ i : Fin n, ∃ C ∈ φ, ∃ l ∈ C, l.1 = i`.

The Main Theorem assumes it. The step to formulas with unused or arbitrarily named variables is handled in the proof of `ethIsFalse` by a renaming front end.
""",
 [q("Does `AllOccur` care whether xᵢ appears negated?", ["Yes, it must appear positively", "No, either sign counts"], 1, "It only checks `l.1 = i`."),
  q("With AllOccur and clauses of width ≤ k, how is n related to m?", ["n ≤ km", "n ≥ km", "no relation"], 0, "Each clause contains at most k variables, and every variable is in some clause."),
  q("Is AllOccur assumed by `ethIsFalse`?", ["Yes", "No, only by the Main Theorem"], 1, "`InTime`/`DecidesKSat` quantify over every k-CNF.")])

node("numSat", "numSat φ: the number of satisfying assignments",
 "Count, among all 2ⁿ assignments, those that make some literal of every clause true.",
 r"""
## Plain English

`numSat φ := (Finset.univ.filter fun a : Fin n → Bool => ∀ C ∈ φ, ∃ l ∈ C, a l.1 = l.2).card`.
""",
 [q("At most how large is numSat φ?", ["n", "2ⁿ", "m"], 1, "There are 2ⁿ assignments."),
  q("numSat φ > 0 iff…", ["φ is satisfiable", "φ has a clause", "every variable occurs"], 0, "Same condition as `Satisfiable`."),
  q("Over which variables are assignments counted?", ["only those that occur", "all of x₀ … x_{n−1}"], 1, "`a : Fin n → Bool`, all n variables.")])

node("binary", "binary n c: the lowest n+1 bits of c",
 "The count is output as exactly n + 1 bits, lowest first. Since the count is at most 2ⁿ, nothing is lost.",
 r"""
## Plain English

`binary n c := (List.range (n + 1)).map c.testBit`: bit 0, bit 1, …, bit n of c.
""",
 [q("binary 2 5 = ?", ["[true, false, true]", "[true, false, true, false]", "[false, true, true]"], 0, "5 = 101₂; bits 0, 1, 2 are 1, 0, 1."),
  q("Why n + 1 bits rather than n?", ["the count can be 2ⁿ itself, which needs n + 1 bits", "for a parity bit"], 0, "2ⁿ = 1 followed by n zeros."),
  q("Lowest or highest bit first?", ["lowest", "highest"], 0, "`List.range` starts at bit 0.")])

node("encInput", "encInput: the Main Theorem's input, with k in it",
 "1ᵏ 0 followed by encClauses k φ. Putting k in the input is what lets one machine handle every width.",
 r"""
## Plain English

`encInput k φ := List.replicate k true ++ false :: encClauses k φ`. See [encClauses](#/node/Anthropic.encClauses).
""",
 [q("How is k written?", ["unary", "binary"], 0, "k ones, then a zero."),
  q("Why is k part of the input here but not in DecidesKSat?", ["the Main Theorem has one machine for all k", "for no reason"], 0, "In `InTime`, k is fixed before the machine is chosen."),
  q("What follows 1ᵏ 0?", ["the formula's code, starting with 1ⁿ 0", "the count"], 0, "`encClauses k φ` starts with n in unary.")])

node("CountsWithin", "CountsWithin: the machine outputs the count within t steps",
 "Started on encInput k φ, the machine halts after at most t steps with binary n (numSat φ) on its output stack.",
 r"""
## Plain English

`CountsWithin M k φ t := Nonempty (TM2OutputsInTime M.tm (encInput k φ …) (some (binary n (numSat φ) …)) t)`.

See [encInput](#/node/Anthropic.encInput), [binary](#/node/Anthropic.binary), [numSat](#/node/Anthropic.numSat). `TM2OutputsInTime` is Mathlib's notion: halt within t steps with that output and every other stack empty.
""",
 [q("Why `Nonempty (…)`?", ["`TM2OutputsInTime` is a structure (data), so `Nonempty` turns it into a proposition", "to allow non-halting runs"], 0, "Mathlib's `TM2OutputsInTime` is a `Type`, holding the run as evidence."),
  q("Must the machine halt?", ["Yes, within t steps", "No"], 0, "`TM2OutputsInTime … t` includes halting within t steps."),
  q("What must the other stacks hold at the end?", ["anything", "nothing (empty)"], 1, "Mathlib's `haltList` puts the output on the output stack and leaves the others empty.")])

node("timeMin", "timeMin: the Main Theorem's time bound",
 "⌊2^{C·min{km/√(log m), k²·n·log log n/√(log n)}}⌋: the better of a bound in the number of clauses and one in the number of variables, with nothing added.",
 r"""
## Plain English

`timeMin C k m n := ⌊2 ^ (C * min (expM k m) (expN k n))⌋₊`, with [expM](#/node/Anthropic.expM) k m = km/√(log m) and [expN](#/node/Anthropic.expN) k n = k²·n·log log n/√(log n), log = [lg](#/node/Anthropic.lg) = log₂.

For fixed k, expN k n / n = k²·log log n/√(log n) → 0, so the bound is 2^{o(n)}.
""",
 [q("Is the bound 2^{o(n)} for fixed k?", ["Yes", "No"], 0, "log log n/√log n → 0."),
  q("Is there a polynomial factor in front?", ["Yes", "No, nothing is added"], 1, "Only the floor of the power of 2. The Challenge docstring stresses: 'nothing is added to it'."),
  q("Which bound wins when m = 5n?", ["the m-bound, km/√log m = O(n/√log n)", "the n-bound"], 0, "For sparse formulas km/√(log m) avoids the log log n factor.")])

node("expM", "expM k m = km/√(log m)", "The exponent in the number of clauses.",
 r"""
## Plain English

`expM k m := k * m / √(lg m)`, with [lg](#/node/Anthropic.lg) = log₂.
""",
 [q("Which log?", ["natural", "base 2"], 1, "`lg = Real.logb 2`."),
  q("What happens at m = 1?", ["√(log 1) = 0, so Lean's x/0 = 0 would make the bound 1 step; the Main Theorem assumes m ≥ 2", "nothing special"], 0, "See the MainTheorem docstring."),
  q("Does expM grow slower than m for fixed k?", ["Yes, by a factor √(log m)", "No"], 0, "km/√log m = o(m).")])

node("expN", "expN k n = k²·n·log log n/√(log n)", "The exponent in the number of variables: o(n) for fixed k.",
 r"""
## Plain English

`expN k n := k^2 * n * lg (lg n) / √(lg n)`, with [lg](#/node/Anthropic.lg) = log₂.
""",
 [q("Is expN k n = o(n) for fixed k?", ["Yes", "No"], 0, "log log n / √log n → 0."),
  q("How does it depend on k?", ["k", "k²", "2^k"], 1, "`(k : ℝ) ^ 2`."),
  q("Why n ≥ 4 in the Main Theorem?", ["so log log n ≥ 1", "so n is even"], 0, "log₂ log₂ 4 = 1. At n = 2, log log n = 0 and the bound would be one step.")])

node("lg", "lg: logarithm to base 2", "The paper's log: Real.logb 2 x, not rounded.",
 r"""
## Plain English

`lg x := Real.logb 2 x`, the real base-2 logarithm, not rounded, and of x itself.
""",
 [q("lg 8 = ?", ["3", "2.08", "8"], 0, "2³ = 8, so log₂ 8 = 3."),
  q("Is lg rounded?", ["Yes", "No"], 1, "It is the real logarithm."),
  q("What is `Real.logb 2 0` in Lean?", ["undefined, so Lean rejects it", "0, by Mathlib's convention (log 0 = 0)"], 1, "Mathlib's `Real.log 0 = 0`. The Main Theorem's hypotheses avoid such inputs.")])

node("MainTheorem", "MainTheorem: the proposition stated by the Main Theorem",
 "The definition whose proof is `mainTheorem`: ∃ one machine M and one constant C, ∀ k ≥ 1, n ≥ 4 and k-CNFs φ with m ≥ 2 clauses where every variable occurs, M counts φ's solutions within timeMin C k m n.",
 r"""
## Plain English

See [mainTheorem](#/node/Anthropic.mainTheorem) for the reading. This node is the `def … : Prop` in MainResults.lean that the theorem in Solution.lean proves.
""",
 [q("What kind of declaration is `MainTheorem`?", ["a theorem", "a definition of a proposition"], 1, "`def MainTheorem : Prop := …`; the proof is `MainResults.mainTheorem`."),
  q("Which quantifier comes first?", ["∃ M C", "∀ k"], 0, "One machine and one constant for everything."),
  q("Does C depend on k?", ["Yes", "No"], 1, "C is chosen before k.")])
