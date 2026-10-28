---
id: OpenAI.Encoding.frame
title: 'frame: making a bit string self-delimiting'
summary: Each bit b becomes (true, b), and a final false ends the frame. The length doubles plus one.
review: draft
authors:
- grok-bot
quiz:
- q: frame [true] = ?
  type: choice
  choices:
  - '[true, true, false]'
  - '[true, false]'
  - '[false, true, true]'
  answer: 0
  explain: 'true :: true :: [false].'
- q: Length of frame of k bits?
  type: choice
  choices:
  - k
  - 2k + 1
  - k + 1
  answer: 1
  explain: Two per bit plus the final false.
- q: How does a reader know the frame ended?
  type: choice
  choices:
  - it reads false where a 'bit follows' marker would be
  - a length prefix
  answer: 0
  explain: Each bit is preceded by true; false ends it.
---
## Plain English

`frame bits := bits.foldr (fun b rest => true :: b :: rest) [false]`.
