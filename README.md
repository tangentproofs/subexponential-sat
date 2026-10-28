# subexponential-sat, informalized

A plain-English reading of two Lean 4 proofs, published in October 2026, that k-SAT can be solved in subexponential time. If their statements mean what they say, the **Exponential Time Hypothesis (ETH) is false**.

| | Lean project | Paper | Headline in Lean |
|---|---|---|---|
| Anthropic (Claude) | [anthropics/formal-math `eth/`](https://github.com/anthropics/formal-math/tree/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth) @ 16a5ce4 | *A 2^o(n) Time Algorithm for 3-SAT* | `MainResults.ethIsFalse : ¬ ETH`, `MainResults.mainTheorem` |
| OpenAI | [openai/math `lean/`](https://github.com/openai/math/blob/main/lean/docs/378.md) @ 7ef5c0c | [*The Exponential Time Hypothesis is False*](https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf) | `SqrtLogSpace.exact_count_and_sat` |

Neither claim has been peer reviewed. See **[REVIEW.md](REVIEW.md)** for what each Lean statement says, what it assumes, and what has and hasn't been checked.

Site: https://tangentproofs.github.io/subexponential-sat/ (once Pages is enabled).

## Layout

- `vendor/` holds the upstream Lean, unchanged (Apache-2.0; see [NOTICE](NOTICE)).
- `site/` is the informalization site, built with the tangentproofs proof-site kit (reference: [star-height](https://github.com/tangentproofs/star-height)).
  - `site/nodes_src/*.py` holds the explainers as data. `python3 site/tools/write_nodes.py` writes `site/nodes/*.md`.
  - `site/tools/scan_decls.py` builds `data/decls.json` and `data/xref.json` from the source text, because no Lean build has been run yet (see the Trust page).
  - `site/pages/*.md` holds the Review, Trust and About pages.

```sh
cd site && npm ci && npm test && npm run serve   # http://localhost:8765/
```
