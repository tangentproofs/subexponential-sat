O = "OpenAI."
NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=O + id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("SqrtLogSpace.exact_count_and_sat", "Exact counting and SAT in subexponential time and polynomial space (OpenAI)",
 "**The surprise:** for each width k ≥ 2, one multi-tape Turing machine counts the solutions of any k-CNF in time (L+1)^d·2^{A·n(log log n)²/√(log n)}, and it uses only polynomially many tape cells while doing so.",
 r"""
## Plain English

**Theorem (`SqrtLogSpace.exact_count_and_sat`).** Fix k ≥ 2. There are a [PrimitiveMachine](#/node/OpenAI.Computation.PrimitiveMachine), two of its tapes (a count tape and an answer tape), and constants C, A, S > 0 and d, e > 0 such that, for every n and every formula F on n variables whose clauses have at most k literals ([WidthAtMost](#/node/OpenAI.SAT.WidthAtMost)):

1. the machine, started on the [canonical code](#/node/OpenAI.Encoding.encodeCNF) of F, runs for some number of steps `time` and halts ([Trace](#/node/OpenAI.Computation.Trace));
2. at the end the count tape holds the number of satisfying assignments ([count](#/node/OpenAI.SAT.count)) in binary ([countWord](#/node/OpenAI.SqrtLogSpace.countWord)), the answer tape holds one bit "count > 0", and the machine's halting state is that same bit;
3. `time` ≤ [runtimeBound](#/node/OpenAI.SqrtLog.Statement.runtimeBound) = C·(L+1)^d·2^{A·n·(log log(n+16))²/√(log(n+16))}, where L is the [bit length](#/node/OpenAI.Encoding.formulaBitLength) of the input;
4. at **every** moment of the run, the number of tape cells visited so far ([visitedSpace](#/node/OpenAI.SqrtLogSpace.visitedSpace)) is at most S·(L+1)^e.

The docstring: *"One fixed primitive machine exactly counts every bounded-width formula, decides satisfiability, meets the square-root-logarithmic time bound, and uses only polynomially many visited tape cells at every execution prefix."*

### Does this refute ETH?

The Lean does **not** state ETH. The step is short, but it is outside Lean. For a 3-CNF on n variables, clauses are *sets* of at most 3 literals, so there are at most (2n+1)³ of them. Numbers in the code are written in unary, so L is polynomial in n. Then (L+1)^d = 2^{O(log n)}, and the whole bound is 2^{O(n(log log n)²/√log n)} = 2^{o(n)}. A multi-tape Turing machine is a standard model, so 3-SAT is in time 2^{o(n)}, and ETH fails.

### What the paper claims beyond this

The manuscript's Theorem 1.1 gives the sharper (n+m)^{O_k(1)}·2^{O_k(n log log n/√log n)}. The scope note (lean/docs/378.md) says the Lean proves the weaker (log log n)² exponent. The sharper bound is **not** formalized here.
""",
 [q("Does one machine serve every k?", ["Yes", "No: the machine is chosen after k"], 1, "`theorem exact_count_and_sat (k : ℕ) (hk : 2 ≤ k) : ∃ (machine …)`. Anthropic's Main Theorem is uniform in k; this one is not, and refuting ETH doesn't need it to be."),
  q("Which exponent is formalized?", ["n·log log n/√log n", "n·(log log n)²/√log n", "n/√log n"], 1, "`runtimeScale n = n·(log log(n+16))²/√(log(n+16))`. The paper's sharper bound is not formalized (see lean/docs/378.md)."),
  q("Does the Lean statement mention ETH?", ["Yes", "No, it states an algorithm and its bounds; 'so ETH fails' is an informal step"], 1, "There is no ETH definition in the comparator file. Anthropic's project states ETH in Lean; OpenAI's does not."),
  q("What does the space clause bound?", ["only the final configuration", "every configuration reached within `time` steps"], 1, "`∀ prefixSteps intermediate, prefixSteps ≤ time → Trace … prefixSteps … intermediate → visitedSpace intermediate ≤ S·(L+1)^e`."),
  q("Which formulas are allowed as input?", ["any F : SAT.CNF (Fin n) with clauses of size ≤ k", "only formulas with every variable occurring", "only n ≥ 20"], 0, "No other hypothesis. (The variant `exact_count_eth` assumes n ≥ 20 and bounds time by (n+m+1)^d instead of (L+1)^d.)")],
 caveats=[
  "The step 'this bound is 2^{o(n)} for 3-CNFs, so ETH fails' is informal. It needs L to be polynomial in n, which holds because clauses are Finsets (no repeats) and the code is unary. It is an easy argument but it is not checked by Lean.",
  "The machine model is OpenAI's own `PrimitiveMachine` (defined in the comparator file, built on Mathlib's `Turing.Tape`), not one of Mathlib's machine types. It is a restricted multi-tape Turing machine: each step reads or acts on one tape. A reader must check this definition. It looks standard, and the machine found uses 1220 tapes.",
  "Inputs are the canonical code only: clauses and literals sorted. The machine is not claimed to handle other encodings of the same formula.",
  "The comparator configuration `ComparatorChallenges/SubexponentialSAT.json` allows only the three standard axioms, but we found no public CI run on commit 7ef5c0c, and this site has not built the proof (≈710,000 lines). The proof tree has no `sorry`, `axiom` or `native_decide` (grep). See the Trust page.",
  "The constants depend on k, so the bound is 2^{O_k(…)}."],
 widgets=[{"type": "walkthrough", "title": "How Final.lean proves it (Final.lean, lines 10-102)", "config": {"steps": [
   {"text": "Compile: the machine is GuardedCompiler.primitive of a structured bit program (80 registers, 1220 stacks)", "lean": "Native.countingProgram cutoff k (NativeLeafProgram.command k)",
    "note": "The algorithm is written in a small structured language (BitProgram) and compiled to a PrimitiveMachine, with stack 256 holding the count and stack 1216 the answer.", "link": "OpenAI.SqrtLogSpace.compiled_exact_count_and_sat"},
   {"text": "Large inputs (n > cutoff): run the subexponential algorithm and use its time and space bounds", "lean": "NativeLargeEntry.run k hk",
    "note": "This is where the mathematics is: shared linear summaries, low-degree replacement forms and counting common zeros of sparse polynomial systems (paper §3–6). Thousands of files under OAI/Algorithms/SubexponentialSAT, not vendored here."},
   {"text": "Small inputs (n ≤ cutoff): a fallback that still meets the bounds", "lean": "Native.entry_small_primitive (Native.outerCommand k (NativeLeafProgram.command k)) F hn",
    "note": "Below the cutoff the bounds are met with padded constants (C + 28700, S + 5022741, …)."},
   {"text": "Merge both cases into one time bound and one space bound", "lean": "NativeOuterBudgets.runtime_with_fallback C A d hC (by linarith)"},
   {"text": "Repackage: pick the machine and its two tapes (256 and 1216)", "lean": "refine ⟨GuardedCompiler.primitive program, (256 : Fin 1220), (1216 : Fin 1220),",
    "note": "Final.lean lines 100-102. This turns the compiled form into exactly the comparator statement."}]}}])

node("SqrtLogSpace.compiled_exact_count_and_sat", "The compiled form of the main theorem",
 "The same statement as the headline, with the machine given as a compiled bit program with 1220 stacks, the count on stack 256 and the answer on stack 1216.",
 r"""
## Plain English

This is the version proved first in SqrtLogSpace/Final.lean lines 10-69. The headline [exact_count_and_sat](#/node/OpenAI.SqrtLogSpace.exact_count_and_sat) is obtained from it by naming the machine `GuardedCompiler.primitive program` and its two tapes.
""",
 [q("How many stacks does the compiled program use?", ["2", "80", "1220"], 2, "`BitProgram.Program 80 1220 labels`: 80 registers, 1220 stacks."),
  q("Where is the count written?", ["stack 256", "stack 1216", "stack 0"], 0, "`final.config.tapes (256 : Fin 1220) = Tape.mk₁ (countWord …)`."),
  q("Is this a weaker statement than the headline?", ["No, the headline is a repackaging of it", "Yes"], 0, "`exact_count_and_sat` is proved by `refine` from this theorem.")])

node("SAT.CNF", "SAT.CNF: a formula as a finite set of clauses",
 "A formula is a **Finset** of clauses and a clause a **Finset** of literals, so nothing can repeat and order does not matter. That keeps the input size polynomial in n.",
 r"""
## Plain English

`CNF V := Finset (Clause V)` and [Clause](#/node/OpenAI.SAT.Clause) V := Finset ([Literal](#/node/OpenAI.SAT.Literal) V). The headline uses V = Fin n.
""",
 [q("Can a clause appear twice in a `SAT.CNF`?", ["Yes", "No"], 1, "It is a Finset."),
  q("Compared to Anthropic's CNF (lists), which is more restrictive?", ["OpenAI's (sets)", "Anthropic's (lists)"], 0, "Anthropic allows repeated literals and different orders; only repeated clauses are forbidden."),
  q("At most how many clauses can a width-3 CNF on n variables have?", ["(2n+1)³ (roughly)", "unbounded", "3n"], 0, "Each clause is a set of at most 3 of the 2n literals.")])

node("SAT.Clause", "SAT.Clause: a finite set of literals", "An OR of finitely many literals, with no repeats.",
 r"""
## Plain English

`Clause V := Finset (Literal V)`.
""",
 [q("Is the empty clause allowed?", ["Yes", "No"], 0, "The empty Finset is a clause; it is false."),
  q("Can a clause contain both x and ¬x?", ["Yes", "No"], 0, "They are different literals."),
  q("Is the order of literals meaningful?", ["Yes", "No"], 1, "Finsets are unordered.")])

node("SAT.Literal", "SAT.Literal: a variable with a sign", "A record with a variable and a Boolean `positive`.",
 r"""
## Plain English

`structure Literal V where variable : V; positive : Bool`. It evaluates to true under `a` when `a variable == positive`.
""",
 [q("What does `positive = false` mean?", ["the negated variable", "the variable itself"], 0, "`Literal.eval a l := a l.variable == l.positive`."),
  q("Does Literal derive DecidableEq?", ["Yes", "No"], 0, "`deriving DecidableEq`, needed to form Finsets of literals."),
  q("How many literals over Fin n?", ["n", "2n"], 1, "n variables × 2 signs.")])

node("SAT.Assignment", "SAT.Assignment", "A function from variables to Bool.",
 r"""
## Plain English

`Assignment V := V → Bool`.
""",
 [q("How many assignments for V = Fin n?", ["n", "2ⁿ", "n²"], 1, "Functions Fin n → Bool."),
  q("Is an assignment partial?", ["No, it gives every variable a value", "Yes"], 0, "It is a total function."),
  q("Is it an `abbrev`?", ["Yes", "No"], 0, "`abbrev Assignment (V : Type u) := V → Bool`.")])

node("SAT.WidthAtMost", "SAT.WidthAtMost k F", "Every clause has at most k literals.",
 r"""
## Plain English

`WidthAtMost k F := ∀ C ∈ F, C.card ≤ k`.
""",
 [q("Does width ≤ 3 allow a clause with 2 literals?", ["Yes", "No"], 0, "The condition is C.card ≤ k, not = k."),
  q("Is it about clauses or variables?", ["clauses", "variables"], 0, "`C.card` is the number of literals in a clause."),
  q("Which k does the headline require?", ["k ≥ 2", "k ≥ 3", "k = 3"], 0, "`(hk : 2 ≤ k)`.")])

node("SAT.count", "SAT.count F: the number of satisfying assignments", "The size of the set of assignments that make every clause true.",
 r"""
## Plain English

`count F := (satisfyingAssignments F).card`, where [satisfyingAssignments](#/node/OpenAI.SAT.satisfyingAssignments) F = all assignments a with `F.eval a = true`.
""",
 [q("count F > 0 iff…", ["F is satisfiable", "F is non-empty"], 0, "Some assignment makes every clause true."),
  q("count of the empty formula on n variables?", ["0", "1", "2ⁿ"], 2, "Every assignment satisfies an empty AND."),
  q("Upper bound?", ["2ⁿ", "n"], 0, "There are 2ⁿ assignments.")])

node("SAT.satisfyingAssignments", "SAT.satisfyingAssignments F", "All assignments under which every clause has a true literal.",
 r"""
## Plain English

`Finset.univ.filter fun a => F.eval a = true`, where `CNF.eval` checks every clause and `Clause.eval` checks for some true literal.
""",
 [q("Which assignments are kept?", ["those with F.eval a = true", "all"], 0, "`Finset.univ.filter` keeps exactly those."),
  q("What does Clause.eval check?", ["some literal is true", "all literals are true"], 0, "`decide (∃ l ∈ C, l.eval a = true)`."),
  q("Why is `[Fintype V]` needed?", ["to form `Finset.univ` of all assignments", "for decidable equality"], 0, "Assignments V → Bool form a finite type only if V is finite.")])

node("Encoding.encodeCNF", "Encoding.encodeCNF: the canonical input word",
 "n in unary, then the formula as a sorted list of sorted clauses of literal codes, all numbers in **unary**. Unary makes the input longer but still polynomial in n for fixed k.",
 r"""
## Plain English

`encodeCNF F := encodeNat n ++ encodeCNFBody F`. [encodeNat](#/node/OpenAI.Encoding.encodeNat) writes n as n ones and a zero. [encodeCNFBody](#/node/OpenAI.Encoding.encodeCNFBody) writes the sorted list of clauses ([cnfNumbers](#/node/OpenAI.Encoding.cnfNumbers)), each a sorted list of [literal codes](#/node/OpenAI.Encoding.literalCode) 2v + (1 if positive), using [encodeList](#/node/OpenAI.Encoding.encodeList) and [frame](#/node/OpenAI.Encoding.frame) for self-delimiting lists.
""",
 [q("How are numbers written?", ["binary", "unary"], 1, "`encodeNat n = replicate n true ++ [false]`."),
  q("Why sort clauses and literals?", ["so each Finset formula has exactly one code", "for speed"], 0, "Finsets have no order; sorting makes the code canonical."),
  q("Is L polynomial in n for fixed k?", ["Yes", "No"], 0, "At most (2n+1)^k clauses, each with ≤ k codes of size O(n), plus framing overhead.")])

node("Encoding.encodeNat", "encodeNat: unary numbers", "n ones followed by a zero.",
 r"""
## Plain English

`encodeNat n := List.replicate n true ++ [false]`.
""",
 [q("encodeNat 2 = ?", ["[true, true, false]", "[true, false]", "[false, true, false]"], 0, "Two ones then a zero."),
  q("Length of encodeNat n?", ["n", "n + 1", "log n"], 1, "n ones plus the terminating zero."),
  q("Is this binary?", ["No, unary", "Yes"], 0, "It is unary: the value is the number of ones.")])

node("Encoding.encodeCNFBody", "encodeCNFBody: the clauses part of the code", "The sorted list of sorted literal-code lists, as nested self-delimiting lists.",
 r"""
## Plain English

`encodeCNFBody F := encodeList (encodeList encodeNat) (cnfNumbers F)`.
""",
 [q("How many list levels?", ["one", "two: clauses, then literals"], 1, "`encodeList (encodeList encodeNat)`."),
  q("What is encoded at the innermost level?", ["literal codes, in unary", "variable names"], 0, "`encodeNat` of each literal code."),
  q("Which order are clauses in?", ["sorted", "insertion order"], 0, "`cnfNumbers` sorts.")])

node("Encoding.encodeList", "encodeList: self-delimiting lists", "Each element is prefixed by a 1 and framed; the list ends with a 0.",
 r"""
## Plain English

`encodeList enc [] = [false]`, `encodeList enc (a :: as) = true :: (frame (enc a) ++ encodeList enc as)`.
""",
 [q("encodeList of the empty list?", ["[]", "[false]", "[true]"], 1, "`| [] => [false]`."),
  q("What marks 'another element follows'?", ["a leading true", "a leading false"], 0, "`true :: …`."),
  q("Why frame each element?", ["so element boundaries can be found", "to add parity"], 0, "`frame` makes each element's code self-delimiting.")])

node("Encoding.frame", "frame: making a bit string self-delimiting", "Each bit b becomes (true, b), and a final false ends the frame. The length doubles plus one.",
 r"""
## Plain English

`frame bits := bits.foldr (fun b rest => true :: b :: rest) [false]`.
""",
 [q("frame [true] = ?", ["[true, true, false]", "[true, false]", "[false, true, true]"], 0, "true :: true :: [false]."),
  q("Length of frame of k bits?", ["k", "2k + 1", "k + 1"], 1, "Two per bit plus the final false."),
  q("How does a reader know the frame ended?", ["it reads false where a 'bit follows' marker would be", "a length prefix"], 0, "Each bit is preceded by true; false ends it.")])

node("Encoding.cnfNumbers", "cnfNumbers: the formula as sorted lists of numbers", "Each clause becomes a sorted list of literal codes; the clauses are then sorted.",
 r"""
## Plain English

`cnfNumbers F := (F.image clauseNumbers).sort (· ≤ ·)` using [clauseNumbers](#/node/OpenAI.Encoding.clauseNumbers).
""",
 [q("Order used for lists of numbers?", ["lexicographic (≤ on lists)", "by length"], 0, "`sort (· ≤ ·)` on `List ℕ` is lexicographic."),
  q("Can two clauses give the same list?", ["No, literal codes determine the literals", "Yes"], 0, "literalCode is injective."),
  q("Is it canonical?", ["Yes", "No"], 0, "Sorted output.")])

node("Encoding.clauseNumbers", "clauseNumbers: a clause as a sorted list", "The literal codes of the clause, sorted.",
 r"""
## Plain English

`clauseNumbers C := (C.image literalCode).sort (· ≤ ·)`, see [literalCode](#/node/OpenAI.Encoding.literalCode).
""",
 [q("Are duplicates possible?", ["No", "Yes"], 0, "A Finset image of an injective map."),
  q("Sorted how?", ["ascending", "descending"], 0, "`(· ≤ ·)`."),
  q("What is in the list?", ["literal codes", "variables"], 0, "2v + sign.")])

node("Encoding.literalCode", "literalCode: 2v + (1 if positive)", "x_v ↦ 2v+1, ¬x_v ↦ 2v.",
 r"""
## Plain English

`literalCode l := 2 * l.variable.val + if l.positive then 1 else 0`.
""",
 [q("Code of ¬x₀?", ["0", "1", "2"], 0, "2·0 + 0 = 0 (positive = false adds nothing)."),
  q("Code of x₃?", ["6", "7", "8"], 1, "2·3 + 1 = 7 (positive adds 1)."),
  q("Is literalCode injective?", ["Yes", "No"], 0, "v = code / 2, sign = code mod 2.")])

node("Encoding.formulaBitLength", "formulaBitLength F = L", "The length of the canonical code: the L in the (L+1)^d factors.",
 r"""
## Plain English

`formulaBitLength F := (encodeCNF F).length`. See [encodeCNF](#/node/OpenAI.Encoding.encodeCNF).
""",
 [q("Is L the number of clauses?", ["No, the bit length of the code", "Yes"], 0, "`(encodeCNF F).length`."),
  q("Where does L appear in the headline?", ["the polynomial factors in time and space", "the exponent"], 0, "C·(L+1)^d·2^{…} and S·(L+1)^e."),
  q("For a 3-CNF on n variables, L is…", ["polynomial in n", "exponential in n"], 0, "≤ (2n+1)³ clauses with unary codes of size O(n).")])

node("Computation.PrimitiveMachine", "PrimitiveMachine: OpenAI's Turing machine model",
 "A finite set of states, a fixed number of tapes over {0, 1, blank}, and in each state the machine looks at **one** tape and either halts with an answer, or moves that tape's head, or writes a symbol on it.",
 r"""
## Plain English

A `PrimitiveMachine` has `tapeCount` tapes and `stateCount` states, a designated input tape and start state, and for each state `q`:

- `scan q`: which tape it reads;
- `transition q s`, given the symbol s under that tape's head (`Option Bool`, `none` = blank): either `.inl answer` (halt with a Boolean answer), or `.inr (q', action)` (go to q' and do one `Turing.TM0.Stmt`: move left or right, or write a symbol).

[step](#/node/OpenAI.Computation.PrimitiveMachine.step) does one transition; [init](#/node/OpenAI.Computation.PrimitiveMachine.init) puts the input on the input tape. Everything else is Mathlib's `Turing.Tape`.

This is a standard (if spartan) multi-tape Turing machine: one tape touched per step, so it is no more powerful than a textbook machine.
""",
 [q("How many tapes does one step act on?", ["one", "all of them"], 0, "`scan q` picks one tape; only it is moved or written."),
  q("What is the tape alphabet?", ["`Option Bool`: 0, 1 or blank", "arbitrary"], 0, "`Turing.Tape (Option Bool)`."),
  q("How does a run halt?", ["`transition` returns `.inl answer`", "by running out of tape"], 0, "Then the state becomes `.inl answer` and `step` returns `none` afterwards.")],
 caveats=["The model is defined in the comparator file, not taken from Mathlib, so its fairness must be checked by reading these few lines. We read them and found nothing unusual, but a second reader should check too."])

node("Computation.PrimitiveMachine.step", "PrimitiveMachine.step: one step", "Read the scanned tape's head symbol; halt with an answer, or move/write on that tape and change state.",
 r"""
## Plain English

From a halted configuration, `step` returns `none`. Otherwise it applies `transition` to the current state and the symbol under the scanned tape's head, and updates only that tape (`Function.update`).
""",
 [q("What does step return on a halted configuration?", ["none", "the same configuration"], 0, "`| .inl _ => none`."),
  q("Does halting cost a step?", ["Yes: the step that returns `.inl answer`", "No"], 0, "That transition is itself a step to the halted configuration."),
  q("How many tapes change per step?", ["at most one", "all"], 0, "`Function.update c.tapes tapeIndex nextTape`.")])

node("Computation.Trace", "Trace step t a b: b is reached from a in exactly t steps", "An inductive relation: t successful steps of `step` lead from a to b.",
 r"""
## Plain English

`Trace step 0 a a`, and if `step a = some b` and `Trace step n b c` then `Trace step (n+1) a c`.
""",
 [q("Can a Trace pass through a halted configuration?", ["only at its end, since step returns none there", "yes"], 0, "Each step must be `some`."),
  q("Is t exact or an upper bound?", ["exact", "upper bound"], 0, "Exactly t steps."),
  q("In the headline, is the final configuration halted?", ["Yes, its state is `Sum.inl …`", "Not necessarily"], 0, "`final.config.state = Sum.inl (decide (0 < count F))`.")])

node("SqrtLogSpace.LocatedCfg", "LocatedCfg: a configuration that remembers where the heads have been",
 "A configuration plus, for each tape, the head position and the lowest and highest positions visited so far. This is what the space bound measures.",
 r"""
## Plain English

Fields: `config`, and per tape `position`, `lower`, `upper` (integers). [locatedStep](#/node/OpenAI.SqrtLogSpace.locatedStep) runs `step` and updates these with `monitor`; [visitedSpace](#/node/OpenAI.SqrtLogSpace.visitedSpace) sums upper − lower + 1 over the tapes.
""",
 [q("Does tracking positions change the run?", ["No, it only records", "Yes"], 0, "`locatedStep` = `step` on the config, then `monitor`."),
  q("What do `lower` and `upper` record?", ["the extreme head positions visited", "the tape contents"], 0, "min/max of positions."),
  q("Initial upper bound on the input tape?", ["input.length − 1", "0"], 0, "`locatedInit` counts the input cells as visited.")])

node("SqrtLogSpace.locatedInit", "locatedInit: start with the input counted as visited", "Initial configuration; the whole input counts as visited cells.",
 r"""
## Plain English

`config := machine.init input`, positions 0, and `upper` on the input tape = input length − 1.
""",
 [q("Are the input's cells counted in the space?", ["Yes", "No"], 0, "`upper` is set to the input length − 1."),
  q("Where do heads start?", ["position 0", "at the end of the input"], 0, "`position _ := 0`."),
  q("Why does that matter?", ["space is then at least the input length, which the poly(L) bound allows", "it doesn't"], 0, "The bound S·(L+1)^e covers it.")])

node("SqrtLogSpace.locatedStep", "locatedStep", "One machine step, also updating the visited range.",
 r"""
## Plain English

`locatedStep machine c := (machine.step c.config).map c.monitor`.
""",
 [q("When does locatedStep return none?", ["exactly when step does", "never"], 0, "It is `Option.map` of step."),
  q("What does monitor update?", ["position, lower, upper of the scanned tape", "all tapes"], 0, "Only tape `scan q`."),
  q("Does it change the config itself?", ["It replaces it by step's result", "No"], 0, "`{ config … }`.")])

node("SqrtLogSpace.visitedSpace", "visitedSpace: tape cells visited so far", "The sum over all tapes of (highest − lowest + 1) visited positions.",
 r"""
## Plain English

`visitedSpace c := ∑ i, (c.upper i − c.lower i + 1).toNat`.
""",
 [q("Does it count cells per tape?", ["Yes, summed over tapes", "only the input tape"], 0, "`∑ i` runs over all tapes."),
  q("Can it shrink during a run?", ["No: lower only decreases and upper only increases", "Yes"], 0, "monitor uses min and max."),
  q("What bound does the headline give?", ["S·(L+1)^e at every prefix", "2^{o(n)}"], 0, "Polynomial space.")])

node("SqrtLogSpace.countWord", "countWord: the count in binary", "Binary digits of the count, lowest first; [false] for 0.",
 r"""
## Plain English

`countWord a := if a = 0 then [false] else a.bits`. The headline also proves `toNat (countWord (count F)) = count F` ([toNat](#/node/OpenAI.BinaryArithmetic.toNat)) and that its length is ≤ n + 1.
""",
 [q("countWord 0 = ?", ["[]", "[false]"], 1, "Special case."),
  q("countWord 6 = ?", ["[false, true, true]", "[true, true, false]"], 0, "6 = 110₂, lowest bit first."),
  q("Why state `toNat (countWord …) = count`?", ["so a reader can see the tape spells the count", "for speed"], 0, "It ties the tape contents to the number.")])

node("BinaryArithmetic.toNat", "BinaryArithmetic.toNat: read a bit list as a number", "Lowest bit first: toNat (b :: bs) = b + 2·toNat bs.",
 r"""
## Plain English

`toNat [] = 0`, `toNat (b :: bs) = bitVal b + 2 * toNat bs`.
""",
 [q("toNat [true, false, true] = ?", ["5", "3", "6"], 0, "1 + 2·(0 + 2·1) = 5."),
  q("Lowest or highest bit first?", ["lowest", "highest"], 0, "The head is the units bit."),
  q("toNat [] = ?", ["0", "1"], 0, "Base case.")])

node("BinaryArithmetic.bitVal", "bitVal", "true ↦ 1, false ↦ 0.",
 r"""
## Plain English

`bitVal b := if b then 1 else 0`.
""",
 [q("bitVal true?", ["1", "0"], 0, "`if true then 1 else 0` = 1."), q("bitVal false?", ["1", "0"], 1, "`if false then 1 else 0` = 0."), q("Type of the result?", ["ℕ", "Bool"], 0, "`def bitVal (b : Bool) : ℕ`.")])

node("SqrtLog.Statement.runtimeBound", "runtimeBound: C·(L+1)^d·2^{A·runtimeScale(n)}", "A polynomial in the input length times 2 to a subexponential function of n.",
 r"""
## Plain English

`runtimeBound C A d L n := C * (L + 1)^d * 2^(A * runtimeScale n)` with [runtimeScale](#/node/OpenAI.SqrtLog.Statement.runtimeScale) n = n·(log log(n+16))²/√(log(n+16)).
""",
 [q("What is L here?", ["the input's bit length", "the number of clauses"], 0, "`inputBits`, given `formulaBitLength F`."),
  q("Is runtimeScale n = o(n)?", ["Yes", "No"], 0, "(log log n)²/√log n → 0."),
  q("Do C, A, d depend on k?", ["Yes, they are chosen after k", "No"], 0, "∃ C A … after `(k : ℕ)`.")])

node("SqrtLog.Statement.runtimeScale", "runtimeScale n = n·(log log(n+16))²/√(log(n+16))", "The o(n) exponent. Natural logs, shifted by 16 so that small n behave.",
 r"""
## Plain English

`runtimeScale n := n * (log (log (n + 16)))^2 / √(log (n + 16))` with `Real.log` (natural log).
""",
 [q("Which log?", ["natural", "base 2"], 0, "`Real.log`."),
  q("Why n + 16?", ["so log log is positive for every n ≥ 0", "arbitrary"], 0, "log 16 ≈ 2.77 and log log 16 ≈ 1.02 > 0."),
  q("Is this the paper's sharpest exponent?", ["No, the paper claims n log log n/√log n; this is the (log log n)² version", "Yes"], 0, "See lean/docs/378.md.")])
