---
id: OpenAI.SqrtLog.Statement.runtimeBound
title: 'runtimeBound: C·(L+1)^d·2^{A·runtimeScale(n)}'
summary: A polynomial in the input length times 2 to a subexponential function of n.
review: draft
authors:
- grok-bot
quiz:
- q: What is L here?
  type: choice
  choices:
  - the input's bit length
  - the number of clauses
  answer: 0
  explain: '`inputBits`, given `formulaBitLength F`.'
- q: Is runtimeScale n = o(n)?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: (log log n)²/√log n → 0.
- q: Do C, A, d depend on k?
  type: choice
  choices:
  - Yes, they are chosen after k
  - 'No'
  answer: 0
  explain: '∃ C A … after `(k : ℕ)`.'
---
## Plain English

`runtimeBound C A d L n := C * (L + 1)^d * 2^(A * runtimeScale n)` with [runtimeScale](#/node/OpenAI.SqrtLog.Statement.runtimeScale) n = n·(log log(n+16))²/√(log(n+16)).
