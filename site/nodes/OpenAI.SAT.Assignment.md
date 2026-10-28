---
id: OpenAI.SAT.Assignment
title: SAT.Assignment
summary: A function from variables to Bool.
review: draft
authors:
- grok-bot
quiz:
- q: How many assignments for V = Fin n?
  type: choice
  choices:
  - n
  - 2ⁿ
  - n²
  answer: 1
  explain: Functions Fin n → Bool.
- q: Is an assignment partial?
  type: choice
  choices:
  - No, it gives every variable a value
  - 'Yes'
  answer: 0
  explain: It is a total function.
- q: Is it an `abbrev`?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: '`abbrev Assignment (V : Type u) := V → Bool`.'
---
## Plain English

`Assignment V := V → Bool`.
