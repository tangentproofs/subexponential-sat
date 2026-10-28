---
id: OpenAI.SqrtLogSpace.LocatedCfg
title: 'LocatedCfg: a configuration that remembers where the heads have been'
summary: A configuration plus, for each tape, the head position and the lowest and highest positions visited so
  far. This is what the space bound measures.
review: draft
authors:
- grok-bot
quiz:
- q: Does tracking positions change the run?
  type: choice
  choices:
  - No, it only records
  - 'Yes'
  answer: 0
  explain: '`locatedStep` = `step` on the config, then `monitor`.'
- q: What do `lower` and `upper` record?
  type: choice
  choices:
  - the extreme head positions visited
  - the tape contents
  answer: 0
  explain: min/max of positions.
- q: Initial upper bound on the input tape?
  type: choice
  choices:
  - input.length − 1
  - '0'
  answer: 0
  explain: '`locatedInit` counts the input cells as visited.'
---
## Plain English

Fields: `config`, and per tape `position`, `lower`, `upper` (integers). [locatedStep](#/node/OpenAI.SqrtLogSpace.locatedStep) runs `step` and updates these with `monitor`; [visitedSpace](#/node/OpenAI.SqrtLogSpace.visitedSpace) sums upper − lower + 1 over the tapes.
