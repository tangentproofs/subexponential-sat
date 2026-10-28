---
id: OpenAI.SAT.satisfyingAssignments
title: SAT.satisfyingAssignments F
summary: All assignments under which every clause has a true literal.
review: draft
authors:
- grok-bot
quiz:
- q: Which assignments are kept?
  type: choice
  choices:
  - those with F.eval a = true
  - all
  answer: 0
  explain: '`Finset.univ.filter` keeps exactly those.'
- q: What does Clause.eval check?
  type: choice
  choices:
  - some literal is true
  - all literals are true
  answer: 0
  explain: '`decide (∃ l ∈ C, l.eval a = true)`.'
- q: Why is `[Fintype V]` needed?
  type: choice
  choices:
  - to form `Finset.univ` of all assignments
  - for decidable equality
  answer: 0
  explain: Assignments V → Bool form a finite type only if V is finite.
---
## Plain English

`Finset.univ.filter fun a => F.eval a = true`, where `CNF.eval` checks every clause and `Clause.eval` checks for some true literal.
