---
id: Anthropic.timeMin
title: 'timeMin: the Main Theorem''s time bound'
summary: '⌊2^{C·min{km/√(log m), k²·n·log log n/√(log n)}}⌋: the better of a bound in the number of clauses and
  one in the number of variables, with nothing added.'
review: draft
authors:
- grok-bot
quiz:
- q: Is the bound 2^{o(n)} for fixed k?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: log log n/√log n → 0.
- q: Is there a polynomial factor in front?
  type: choice
  choices:
  - 'Yes'
  - No, nothing is added
  answer: 1
  explain: 'Only the floor of the power of 2. The Challenge docstring stresses: ''nothing is added to it''.'
- q: Which bound wins when m = 5n?
  type: choice
  choices:
  - the m-bound, km/√log m = O(n/√log n)
  - the n-bound
  answer: 0
  explain: For sparse formulas km/√(log m) avoids the log log n factor.
---
## Plain English

`timeMin C k m n := ⌊2 ^ (C * min (expM k m) (expN k n))⌋₊`, with [expM](#/node/Anthropic.expM) k m = km/√(log m) and [expN](#/node/Anthropic.expN) k n = k²·n·log log n/√(log n), log = [lg](#/node/Anthropic.lg) = log₂.

For fixed k, expN k n / n = k²·log log n/√(log n) → 0, so the bound is 2^{o(n)}.
