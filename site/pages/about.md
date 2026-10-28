# About this site

In October 2026 two AI labs each published a claimed disproof of the **Exponential Time Hypothesis** (ETH), with a Lean formalization:

- **Anthropic**: *A 2^o(n) Time Algorithm for 3-SAT*, found by an internal Claude model on 16 October. The [Lean project](https://github.com/anthropics/formal-math/tree/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth) states ETH in Lean and proves `¬ ETH`, plus a Main Theorem with one machine for every k.
- **OpenAI**: *The Exponential Time Hypothesis is False* ([preprint](https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf), [Lean scope note](https://github.com/openai/math/blob/main/lean/docs/378.md)). The Lean proves an exact-counting algorithm with a subexponential time bound and polynomial space.

The Lean checks, or at least the authors say so (see [Trust](#/trust)). This site does the other half of the job: it reads the formal **statements** back into plain English, so that a person can judge whether they say what the headlines claim. Each node is one Lean declaration with its verbatim Lean, a plain-English reading, caveats and a short quiz. Tick **I understand** when you do. A node counts as understood once everything its statement mentions is understood too.

The [Lean source](src/index.html) is on the site, highlighted, and every "File.lean lines a–b" reference opens those exact lines.

Start with [the statements](#/start), or read the [review](#/review).

**Credit.** Theorems, papers and Lean proofs: Anthropic (Claude) and OpenAI, both Apache-2.0, vendored unchanged. Explanations: community drafts (Grok Bot for Michal Wallace), not endorsed by either lab, and possibly wrong. The Lean is the ground truth.
