---
id: OpenAI.Encoding.formulaBitLength
title: formulaBitLength F = L
summary: 'The length of the canonical code: the L in the (L+1)^d factors.'
review: draft
authors:
- grok-bot
quiz:
- q: Is L the number of clauses?
  type: choice
  choices:
  - No, the bit length of the code
  - 'Yes'
  answer: 0
  explain: '`(encodeCNF F).length`.'
- q: Where does L appear in the headline?
  type: choice
  choices:
  - the polynomial factors in time and space
  - the exponent
  answer: 0
  explain: C·(L+1)^d·2^{…} and S·(L+1)^e.
- q: For a 3-CNF on n variables, L is…
  type: choice
  choices:
  - polynomial in n
  - exponential in n
  answer: 0
  explain: ≤ (2n+1)³ clauses with unary codes of size O(n).
---
## Plain English

`formulaBitLength F := (encodeCNF F).length`. See [encodeCNF](#/node/OpenAI.Encoding.encodeCNF).
