# Review: do the two Lean statements say what the papers claim?

*Reviewed 27 October 2026 by Grok Bot, for Michal Wallace, by reading the source at the pinned commits. Neither project was built for this review. A second, independent model audit is still to do.*

**The short answer:** both statements look faithful, and we found no hidden hypotheses, no `sorry` in either proof and no extra axioms. Anthropic's project states ETH itself in Lean and proves it false. OpenAI's project proves a time bound for one algorithm and leaves the final, easy step ("so ETH fails") to the reader. Neither result has been peer reviewed. Impagliazzo, Paturi and Williams are leading a community check.

| | Anthropic (Claude) | OpenAI |
|---|---|---|
| Repo, commit | [anthropics/formal-math `eth/`](https://github.com/anthropics/formal-math/tree/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth) @ 16a5ce4 (26 Oct 2026) | [openai/math `lean/`](https://github.com/openai/math/blob/main/lean/docs/378.md) @ 7ef5c0c (26 Oct 2026) |
| Paper | *A 2^o(n) Time Algorithm for 3-SAT*, by Claude (in the repo as `paper.pdf`) | *The Exponential Time Hypothesis is False*, by OpenAI (preprint, 25 Oct 2026) |
| Lean / Mathlib | v4.33.1 / v4.33.1 | v4.34.1 (one large library for all their papers) |
| License | Apache-2.0 (+ NOTICE) | Apache-2.0 |
| Size | 1,047 files, ≈152,000 lines | 3,977 files, ≈710,000 lines (in `OAI/Algorithms/SubexponentialSAT/`) |
| Headline in Lean | `MainResults.ethIsFalse` (¬ETH) and `MainResults.mainTheorem` | `OAI.Algorithms.SubexponentialSAT.SqrtLogSpace.exact_count_and_sat` |
| Time bound proved | 2^{C·min{km/√log m, k²n log log n/√log n}}, with one machine for all k | C·(L+1)^d·2^{A·n(log log n)²/√log n}, with one machine per k, plus polynomial space |
| Machine model | Mathlib's `Turing.FinTM2` (multi-stack) | Their own `PrimitiveMachine` (multi-tape, on Mathlib's `Turing.Tape`) |
| `sorry` / `axiom` / `native_decide` in the proof | none (grep) | none (grep) |
| Independent check | GitHub CI "verify (eth)" **passed** at 11:31 PM ET, 26 Oct, using Comparator with the independent `nanoda` kernel | Comparator config present (`SubexponentialSAT.json`, 3 standard axioms, nanoda off). **No public CI run found** |

## Anthropic: `ethIsFalse` and the Main Theorem

**Faithfulness.** MainResults.lean defines everything from scratch on top of Mathlib: literals, CNFs, satisfiability, the input encoding, "decides k-SAT within t(n) steps", s_k as an infimum and `ETH := 0 < s 3`. That is the textbook Impagliazzo–Paturi definition, restricted to deterministic machines. `ETHIsFalse := ¬ ETH`. The theorem has no hypotheses.

**Things to know (not red flags):**

- *Mathlib Turing machines versus "algorithms".* The comment at the top of MainResults.lean argues that a RAM simulates a `FinTM2` with bounded overhead, and that re-encoding a formula is polynomial, so s₃ here is at least s₃ in the usual sense. That is standard, but it is prose, not Lean.
- *No repeated clauses.* `IsKCNF` requires `φ.Nodup`. Without it, inputs could be arbitrarily long for fixed n, and no bound in n alone could hold. This is the usual convention.
- *Main Theorem side conditions.* It needs k ≥ 1, n ≥ 4, m ≥ 2, and every variable to occur. These are stated openly, and the docstring explains each one. The route to `ethIsFalse` removes the "every variable occurs" condition by a renaming front end, proved in Lean.
- *Stronger than needed.* One machine and one constant C handle **all** k, and the time has no polynomial factor in front.
- The authors list where the Lean differs from the printed statements (paper, Appendix E, and proof/PaperIndex.lean). **We have not checked Appendix E line by line yet.**

**Red flags:** none found.

## OpenAI: `exact_count_and_sat`

**Faithfulness.** The comparator file ComparatorChallenges/SubexponentialSAT.lean (lines 1-218) defines CNFs as Finsets of Finsets of literals, a canonical unary bit encoding, a small multi-tape Turing machine model, and a "located" run that tracks visited cells. The theorem says that for each k ≥ 2 one machine counts the solutions of every width-k formula exactly. It halts with the count and a SAT bit, within C·(L+1)^d·2^{A·n(log log(n+16))²/√log(n+16)} steps, and uses at most S·(L+1)^e visited cells at every point of the run. That matches the scope note (lean/docs/378.md).

**Things to know:**

- *ETH is not stated in Lean.* The step from the bound to "ETH is false" is informal: for 3-CNFs, L is polynomial in n (Finset clauses, unary numbers), so the bound is 2^{o(n)}. It is easy and we believe it, but a skeptic should note it.
- *Their own machine model.* `PrimitiveMachine` is defined in the comparator file, not taken from Mathlib. We read it (about 40 lines). Each step reads one tape and either halts, moves that tape's head or writes one symbol. That is no stronger than a textbook multi-tape machine. The machine found uses 1220 tapes, which is a fixed constant and so is fine.
- *Weaker than the paper.* The paper's headline exponent is n·log log n/√log n. The Lean proves n·(log log n)²/√log n. OpenAI's scope note says so. Both are 2^{o(n)}.
- *Canonical input.* Clauses and literals must be sorted. That is reasonable, because a Finset formula has one such code.
- *Not uniform in k.* The machine is chosen after k. Refuting ETH only needs k = 3.
- *Two `private opaque` wrappers* (NativeCode.lean and SparseDFSProgram.lean) hide a list of port numbers from unfolding. Each has a real value and a proved equation, and adds no axiom. This is harmless, but we noted it.

**Red flags:** none found in the statement. The one gap is evidence rather than content: we found no public build or CI result for this commit, and the proof is very large (≈710k lines). **A build plus `#print axioms` (or Comparator) is needed before anyone treats it as checked.** Final.lean ends with `#print axioms` lines, so a build would show the answer.

## What would make this review stronger

1. Build OpenAI's `OAI.Algorithms.SubexponentialSAT.Main` and run its Comparator challenge. It is huge, so it needs a large machine.
2. Re-run Anthropic's Comparator check ourselves. It takes about 8 minutes on 24 vCPUs, with a peak of about 7 GB.
3. Get an independent model audit of both statement files, and go through Anthropic's Appendix E line by line.
4. Replace this site's text-scanned declaration list with one extracted from a real build (`ExtractDecls.lean`).
