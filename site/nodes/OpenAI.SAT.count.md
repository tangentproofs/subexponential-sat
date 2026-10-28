---
id: OpenAI.SAT.count
title: 'SAT.count F: the number of satisfying assignments'
summary: The size of the set of assignments that make every clause true.
review: draft
authors:
- grok-bot
quiz:
- q: count F > 0 iff…
  type: choice
  choices:
  - F is satisfiable
  - F is non-empty
  answer: 0
  explain: Some assignment makes every clause true.
- q: count of the empty formula on n variables?
  type: choice
  choices:
  - '0'
  - '1'
  - 2ⁿ
  answer: 2
  explain: Every assignment satisfies an empty AND.
- q: Upper bound?
  type: choice
  choices:
  - 2ⁿ
  - n
  answer: 0
  explain: There are 2ⁿ assignments.
---
## Plain English

`count F := (satisfyingAssignments F).card`, where [satisfyingAssignments](#/node/OpenAI.SAT.satisfyingAssignments) F = all assignments a with `F.eval a = true`.
