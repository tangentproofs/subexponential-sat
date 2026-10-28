---
id: Anthropic.AllOccur
title: 'AllOccur φ: every variable occurs'
summary: Each of x₀ … x_{n−1} appears in some clause, positively or negatively. Then n ≤ km, so a bound in m also
  bounds things in n.
review: draft
authors:
- grok-bot
quiz:
- q: Does `AllOccur` care whether xᵢ appears negated?
  type: choice
  choices:
  - Yes, it must appear positively
  - No, either sign counts
  answer: 1
  explain: It only checks `l.1 = i`.
- q: With AllOccur and clauses of width ≤ k, how is n related to m?
  type: choice
  choices:
  - n ≤ km
  - n ≥ km
  - no relation
  answer: 0
  explain: Each clause contains at most k variables, and every variable is in some clause.
- q: Is AllOccur assumed by `ethIsFalse`?
  type: choice
  choices:
  - 'Yes'
  - No, only by the Main Theorem
  answer: 1
  explain: '`InTime`/`DecidesKSat` quantify over every k-CNF.'
---
## Plain English

`AllOccur φ := ∀ i : Fin n, ∃ C ∈ φ, ∃ l ∈ C, l.1 = i`.

The Main Theorem assumes it. The step to formulas with unused or arbitrarily named variables is handled in the proof of `ethIsFalse` by a renaming front end.
