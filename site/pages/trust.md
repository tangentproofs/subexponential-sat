# Trust: what has and hasn't been checked

This site **explains** two Lean proofs. It does not re-check them. Here is exactly what rests on what.

## Lean checking

| | Anthropic `eth` @ 16a5ce4 | OpenAI `SubexponentialSAT` @ 7ef5c0c |
|---|---|---|
| Built by this site | **no** | **no** |
| Built by the authors, publicly | yes: GitHub Actions "verify (eth)" passed at 11:31 PM ET, 26 Oct 2026 (`lake build`, plus Comparator with the `nanoda` kernel in the `landrun` sandbox) | no public run found |
| Axioms claimed | `propext`, `Classical.choice`, `Quot.sound` (README, `scripts/PrintAxioms.lean`) | the same three allowed by `ComparatorChallenges/SubexponentialSAT.json`. `#print axioms` lines at the end of Final.lean |
| `sorry` in the proof | none (only in Challenge.lean, on purpose, for Comparator) | none (only in the comparator file, on purpose) |
| `axiom`, `native_decide`, `implemented_by`, `extern`, meta-programs | none found by grep | none found by grep. Two `private opaque` definitions with values (harmless) |
| Dependencies | Mathlib only | Mathlib only (the library's other requirements are not imported by these files) |

## This site's own data

- **Declarations were read from the source text, not from a Lean build.** `site/tools/scan_decls.py` finds the top-level declarations of the statement files (MainResults.lean, Solution.lean, the comparator file, Final.lean, SubexpOrderedRawMainTheorem.lean) with their exact lines and text. Every declaration carries `"extracted": false`. The "mentions" edges are matched by name and may miss dot-notation uses (for example `machine.Cfg`).
- **Identifier links on the source pages are also matched by name** (`data/xref.json` is marked `"heuristic": true`). Project names link to their definition. A short hand-checked list of Mathlib names links to the Mathlib docs. Other Mathlib names are not linked yet.
- **Vendored source.** `vendor/anthropic-eth/` is the whole `eth` project at 16a5ce4, unchanged. `vendor/openai-sat/` holds the comparator file and the top three proof files at 7ef5c0c, unchanged. The other ≈3,970 files are only on GitHub. Both are Apache-2.0. See NOTICE.
- **Explanations** are drafts by Grok Bot (`review: draft`). They have not been reviewed by a human or by a second model.

## To upgrade this page

Build both projects on a capable machine, run `ExtractDecls.lean` and `build_xref.py` as on the other tangentproofs sites, run `#print axioms` for each headline, and replace the two "no" entries above.
