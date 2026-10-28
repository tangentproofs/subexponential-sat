---
id: Anthropic.MainTheorem
title: 'MainTheorem: the proposition stated by the Main Theorem'
summary: 'The definition whose proof is `mainTheorem`: ∃ one machine M and one constant C, ∀ k ≥ 1, n ≥ 4 and k-CNFs
  φ with m ≥ 2 clauses where every variable occurs, M counts φ''s solutions within timeMin C k m n.'
review: draft
authors:
- grok-bot
quiz:
- q: What kind of declaration is `MainTheorem`?
  type: choice
  choices:
  - a theorem
  - a definition of a proposition
  answer: 1
  explain: '`def MainTheorem : Prop := …`; the proof is `MainResults.mainTheorem`.'
- q: Which quantifier comes first?
  type: choice
  choices:
  - ∃ M C
  - ∀ k
  answer: 0
  explain: One machine and one constant for everything.
- q: Does C depend on k?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 1
  explain: C is chosen before k.
---
## Plain English

See [mainTheorem](#/node/Anthropic.mainTheorem) for the reading. This node is the `def … : Prop` in MainResults.lean that the theorem in Solution.lean proves.
