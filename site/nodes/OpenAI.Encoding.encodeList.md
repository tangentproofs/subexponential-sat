---
id: OpenAI.Encoding.encodeList
title: 'encodeList: self-delimiting lists'
summary: Each element is prefixed by a 1 and framed; the list ends with a 0.
review: draft
authors:
- grok-bot
quiz:
- q: encodeList of the empty list?
  type: choice
  choices:
  - '[]'
  - '[false]'
  - '[true]'
  answer: 1
  explain: '`| [] => [false]`.'
- q: What marks 'another element follows'?
  type: choice
  choices:
  - a leading true
  - a leading false
  answer: 0
  explain: '`true :: …`.'
- q: Why frame each element?
  type: choice
  choices:
  - so element boundaries can be found
  - to add parity
  answer: 0
  explain: '`frame` makes each element''s code self-delimiting.'
---
## Plain English

`encodeList enc [] = [false]`, `encodeList enc (a :: as) = true :: (frame (enc a) ++ encodeList enc as)`.
