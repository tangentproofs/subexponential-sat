---
id: OpenAI.SqrtLogSpace.locatedInit
title: 'locatedInit: start with the input counted as visited'
summary: Initial configuration; the whole input counts as visited cells.
review: draft
authors:
- grok-bot
quiz:
- q: Are the input's cells counted in the space?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 0
  explain: '`upper` is set to the input length − 1.'
- q: Where do heads start?
  type: choice
  choices:
  - position 0
  - at the end of the input
  answer: 0
  explain: '`position _ := 0`.'
- q: Why does that matter?
  type: choice
  choices:
  - space is then at least the input length, which the poly(L) bound allows
  - it doesn't
  answer: 0
  explain: The bound S·(L+1)^e covers it.
---
## Plain English

`config := machine.init input`, positions 0, and `upper` on the input tape = input length − 1.
