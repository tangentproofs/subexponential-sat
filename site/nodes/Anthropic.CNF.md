---
id: Anthropic.CNF
title: 'CNF n: a formula as a list of clauses'
summary: A formula on variables x₀ … x_{n−1} is a list of clauses, and a clause is a list of literals. Order and
  repetition are allowed at this level; `IsKCNF` restricts them.
review: draft
authors:
- grok-bot
quiz:
- q: A clause is a…
  type: choice
  choices:
  - Finset of literals
  - List of literals
  - function from variables to Bool
  answer: 1
  explain: '`List (Lit n)`.'
- q: What is the empty formula `[]`?
  type: choice
  choices:
  - always false
  - always true
  - not a CNF
  answer: 1
  explain: An AND of no clauses is true. Every assignment satisfies it.
- q: Which condition stops clauses from repeating?
  type: choice
  choices:
  - CNF itself
  - IsKCNF (`List.Nodup`)
  answer: 1
  explain: CNF is just a list type; `IsKCNF` adds `φ.Nodup`.
---
## Plain English

`CNF n := List (List (Lit n))`: an AND of clauses, each an OR of [literals](#/node/Anthropic.Lit).
