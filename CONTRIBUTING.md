# Contributing explainers

**The Lean is the ground truth.** An explainer is right only if it matches the statement exactly as written in `vendor/`: its hypotheses, the order of its quantifiers, and what is `∃` and what is `∀`. Don't import claims from the papers that the Lean doesn't make. If you aren't sure, say so under `caveats`.

The node format, progress rules and quiz rules are the same as on the other tangentproofs sites (see [star-height's CONTRIBUTING.md](https://github.com/tangentproofs/star-height/blob/main/CONTRIBUTING.md)). There are three differences:

- **ids** carry a project prefix: `Anthropic.<name without MainResults.>` or `OpenAI.<name without OAI.Algorithms.SubexponentialSAT.>`. Look them up in `site/data/decls.json`.
- **Edit `site/nodes_src/anthropic.py` or `site/nodes_src/openai.py`**, not `site/nodes/*.md`. Then run `python3 site/tools/write_nodes.py` to regenerate the Markdown, which keeps the YAML valid. CI checks that the two agree.
- **Lead with the surprise.** A node's `summary` should start with its most surprising takeaway.

Run `cd site && npm ci && npm test` before opening a PR. Keep `review: draft` unless a person has checked the node against the Lean.
