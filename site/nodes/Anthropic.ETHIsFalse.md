---
id: Anthropic.ETHIsFalse
title: 'ETHIsFalse: the proposition ''ETH is false'''
summary: 'Just `¬ ETH`. Because s₃ can never be negative, this is the same as saying s₃ = 0: arbitrarily small exponents
  δ are achievable for 3-SAT.'
review: draft
authors:
- grok-bot
quiz:
- q: '`ETHIsFalse` is defined as…'
  type: choice
  choices:
  - '`s 3 = 0`'
  - '`¬ ETH`'
  - '`∀ δ > 0, InTime 3 δ`'
  - '`MainTheorem`'
  answer: 1
  explain: 'MainResults.lean line 122: `def ETHIsFalse : Prop := ¬ ETH`. The other forms are equivalent readings,
    not the definition.'
- q: Why does ¬(0 < s₃) give s₃ = 0?
  type: choice
  choices:
  - because s₃ is a natural number
  - because s₃ is an infimum of non-negative values, so s₃ ≥ 0
  - it does not; s₃ could be negative
  answer: 1
  explain: '`s` takes values in ℝ≥0∞, which has no negative numbers.'
- q: Does `ETHIsFalse` require one machine for all δ?
  type: choice
  choices:
  - 'Yes'
  - 'No'
  answer: 1
  explain: No. It only rules out a positive lower bound on the achievable δ's, and each δ may have its own machine.
---
## Plain English

`ETHIsFalse : Prop := ¬ ETH`, the negation of [ETH](#/node/Anthropic.ETH).

ETH says `0 < s 3`. Its negation says `s 3 ≤ 0`, and since [s](#/node/Anthropic.s) is an infimum of values in [0, ∞], that means s₃ = 0. Equivalently, for every δ > 0 there is some δ' < δ such that `InTime 3 δ'` holds, and since `InTime` gets weaker as δ grows, `InTime 3 δ` holds for every δ > 0.
