---
id: Anthropic.s
title: 's k: the best achievable exponent for k-SAT'
summary: s k is the infimum of all δ ≥ 0 such that some machine decides k-SAT in c·2^{δn} steps. It lives in [0,
  ∞], and is ∞ if no δ works.
review: draft
authors:
- grok-bot
quiz:
- q: What is `s k` if no δ works?
  type: choice
  choices:
  - '0'
  - '1'
  - ∞
  answer: 2
  explain: An infimum over the empty set in ℝ≥0∞ is ⊤ = ∞.
- q: Can `s k` be negative?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 1
  explain: δ ranges over ℝ≥0 and the value lives in ℝ≥0∞.
- q: If `InTime 3 δ` holds for every δ > 0, what is `s 3`?
  type: choice
  choices:
  - '0'
  - '1'
  - it depends on c
  answer: 0
  explain: The infimum of all positive reals is 0.
---
## Plain English

`s k := ⨅ (δ : ℝ≥0) (_ : InTime k δ), (δ : ℝ≥0∞)`: the infimum, over all non-negative reals δ for which [InTime](#/node/Anthropic.InTime) k δ holds, of δ.

The infimum is taken in the extended non-negative reals, so an empty set of δ's gives ∞. For k = 3, brute force already gives δ = 1, so s₃ ≤ 1.
