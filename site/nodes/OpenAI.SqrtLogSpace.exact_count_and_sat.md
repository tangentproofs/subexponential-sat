---
id: OpenAI.SqrtLogSpace.exact_count_and_sat
title: Exact counting and SAT in subexponential time and polynomial space (OpenAI)
summary: '**The surprise:** for each width k ≥ 2, one multi-tape Turing machine counts the solutions of any k-CNF
  in time (L+1)^d·2^{A·n(log log n)²/√(log n)}, and it uses only polynomially many tape cells while doing so.'
review: draft
authors:
- grok-bot
caveats:
- The step 'this bound is 2^{o(n)} for 3-CNFs, so ETH fails' is informal. It needs L to be polynomial in n, which
  holds because clauses are Finsets (no repeats) and the code is unary. It is an easy argument but it is not checked
  by Lean.
- 'The machine model is OpenAI''s own `PrimitiveMachine` (defined in the comparator file, built on Mathlib''s `Turing.Tape`),
  not one of Mathlib''s machine types. It is a restricted multi-tape Turing machine: each step reads or acts on
  one tape. A reader must check this definition. It looks standard, and the machine found uses 1220 tapes.'
- 'Inputs are the canonical code only: clauses and literals sorted. The machine is not claimed to handle other encodings
  of the same formula.'
- The comparator configuration `ComparatorChallenges/SubexponentialSAT.json` allows only the three standard axioms,
  but we found no public CI run on commit 7ef5c0c, and this site has not built the proof (≈710,000 lines). The proof
  tree has no `sorry`, `axiom` or `native_decide` (grep). See the Trust page.
- The constants depend on k, so the bound is 2^{O_k(…)}.
widgets:
- type: walkthrough
  title: How Final.lean proves it (Final.lean, lines 10-102)
  config:
    steps:
    - text: 'Compile: the machine is GuardedCompiler.primitive of a structured bit program (80 registers, 1220 stacks)'
      lean: Native.countingProgram cutoff k (NativeLeafProgram.command k)
      note: The algorithm is written in a small structured language (BitProgram) and compiled to a PrimitiveMachine,
        with stack 256 holding the count and stack 1216 the answer.
      link: OpenAI.SqrtLogSpace.compiled_exact_count_and_sat
    - text: 'Large inputs (n > cutoff): run the subexponential algorithm and use its time and space bounds'
      lean: NativeLargeEntry.run k hk
      note: 'This is where the mathematics is: shared linear summaries, low-degree replacement forms and counting
        common zeros of sparse polynomial systems (paper §3–6). Thousands of files under OAI/Algorithms/SubexponentialSAT,
        not vendored here.'
    - text: 'Small inputs (n ≤ cutoff): a fallback that still meets the bounds'
      lean: Native.entry_small_primitive (Native.outerCommand k (NativeLeafProgram.command k)) F hn
      note: Below the cutoff the bounds are met with padded constants (C + 28700, S + 5022741, …).
    - text: Merge both cases into one time bound and one space bound
      lean: NativeOuterBudgets.runtime_with_fallback C A d hC (by linarith)
    - text: 'Repackage: pick the machine and its two tapes (256 and 1216)'
      lean: 'refine ⟨GuardedCompiler.primitive program, (256 : Fin 1220), (1216 : Fin 1220),'
      note: Final.lean lines 100-102. This turns the compiled form into exactly the comparator statement.
quiz:
- q: Does one machine serve every k?
  type: choice
  choices:
  - 'Yes'
  - 'No: the machine is chosen after k'
  answer: 1
  explain: '`theorem exact_count_and_sat (k : ℕ) (hk : 2 ≤ k) : ∃ (machine …)`. Anthropic''s Main Theorem is uniform
    in k; this one is not, and refuting ETH doesn''t need it to be.'
- q: Which exponent is formalized?
  type: choice
  choices:
  - n·log log n/√log n
  - n·(log log n)²/√log n
  - n/√log n
  answer: 1
  explain: '`runtimeScale n = n·(log log(n+16))²/√(log(n+16))`. The paper''s sharper bound is not formalized (see
    lean/docs/378.md).'
- q: Does the Lean statement mention ETH?
  type: choice
  choices:
  - 'Yes'
  - No, it states an algorithm and its bounds; 'so ETH fails' is an informal step
  answer: 1
  explain: There is no ETH definition in the comparator file. Anthropic's project states ETH in Lean; OpenAI's does
    not.
- q: What does the space clause bound?
  type: choice
  choices:
  - only the final configuration
  - every configuration reached within `time` steps
  answer: 1
  explain: '`∀ prefixSteps intermediate, prefixSteps ≤ time → Trace … prefixSteps … intermediate → visitedSpace
    intermediate ≤ S·(L+1)^e`.'
- q: Which formulas are allowed as input?
  type: choice
  choices:
  - 'any F : SAT.CNF (Fin n) with clauses of size ≤ k'
  - only formulas with every variable occurring
  - only n ≥ 20
  answer: 0
  explain: No other hypothesis. (The variant `exact_count_eth` assumes n ≥ 20 and bounds time by (n+m+1)^d instead
    of (L+1)^d.)
---
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
