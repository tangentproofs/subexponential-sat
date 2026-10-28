---
id: OpenAI.SqrtLogSpace.countWord
title: 'countWord: the count in binary'
summary: Binary digits of the count, lowest first; [false] for 0.
review: draft
authors:
- grok-bot
quiz:
- q: countWord 0 = ?
  type: choice
  choices:
  - '[]'
  - '[false]'
  answer: 1
  explain: Special case.
- q: countWord 6 = ?
  type: choice
  choices:
  - '[false, true, true]'
  - '[true, true, false]'
  answer: 0
  explain: 6 = 110₂, lowest bit first.
- q: Why state `toNat (countWord …) = count`?
  type: choice
  choices:
  - so a reader can see the tape spells the count
  - for speed
  answer: 0
  explain: It ties the tape contents to the number.
---
## Plain English

`countWord a := if a = 0 then [false] else a.bits`. The headline also proves `toNat (countWord (count F)) = count F` ([toNat](#/node/OpenAI.BinaryArithmetic.toNat)) and that its length is ≤ n + 1.
