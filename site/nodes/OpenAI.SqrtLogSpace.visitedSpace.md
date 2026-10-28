---
id: OpenAI.SqrtLogSpace.visitedSpace
title: 'visitedSpace: tape cells visited so far'
summary: The sum over all tapes of (highest − lowest + 1) visited positions.
review: draft
authors:
- grok-bot
quiz:
- q: Does it count cells per tape?
  type: choice
  choices:
  - Yes, summed over tapes
  - only the input tape
  answer: 0
  explain: '`∑ i` runs over all tapes.'
- q: Can it shrink during a run?
  type: choice
  choices:
  - 'No: lower only decreases and upper only increases'
  - 'Yes'
  answer: 0
  explain: monitor uses min and max.
- q: What bound does the headline give?
  type: choice
  choices:
  - S·(L+1)^e at every prefix
  - 2^{o(n)}
  answer: 0
  explain: Polynomial space.
---
## Plain English

`visitedSpace c := ∑ i, (c.upper i − c.lower i + 1).toNat`.
