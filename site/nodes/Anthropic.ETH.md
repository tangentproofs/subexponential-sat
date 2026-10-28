---
id: Anthropic.ETH
title: 'ETH: the Exponential Time Hypothesis, as a Lean proposition'
summary: 'ETH is stated as `0 < s 3`: some fixed exponent δ > 0 is unbeatable for 3-SAT. That is Impagliazzo and
  Paturi''s form, restricted to deterministic Turing machines.'
review: draft
authors:
- grok-bot
caveats:
- The translation from 'machines in Mathlib's model' to 'algorithms in the usual sense' is an informal (standard)
  argument, given in the head comment of MainResults.lean.
quiz:
- q: Which k does the Lean ETH use?
  type: choice
  choices:
  - k = 2
  - k = 3
  - every k ≥ 3
  answer: 1
  explain: '`ETH := 0 < s 3`.'
- q: If 3-SAT could be decided in time 1.0001ⁿ but not faster, would ETH (as defined) hold?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: Then s₃ = log₂ 1.0001 > 0, so `0 < s 3`.
- q: Does the Lean ETH speak about randomized algorithms?
  type: choice
  choices:
  - 'Yes'
  - No, deterministic machines only
  answer: 1
  explain: '`InTime` asks for a deterministic `FinTM2` machine. The authors remark, outside Lean, that refuting
    the deterministic form also refutes the randomized one.'
---
## Plain English

`ETH : Prop := 0 < s 3`, where [s](#/node/Anthropic.s) 3 is the infimum of the exponents δ for which 3-SAT on n variables can be decided in time O(2^{δn}).

The docstring cites Impagliazzo and Paturi, *On the complexity of k-SAT*, J. Comput. Syst. Sci. 62 (2001). The paper defines ETH as "s_k > 0 for all k ≥ 3" and notes that this is the same as s₃ > 0. The Lean uses the k = 3 form. Refuting it refutes the "all k" form too, because the k = 3 case fails.

**Why this form is the right one to refute.** It is stated about machines in Mathlib's model, which (by the head comment of MainResults.lean) are at least as slow as algorithms in the usual sense, up to polynomial factors. So s₃ in the usual sense is at most s₃ as defined here, and "s₃ = 0 here" gives "s₃ = 0 there".
