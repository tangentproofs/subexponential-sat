#!/usr/bin/env python3
"""Build site/data/decls.json and site/data/xref.json from the vendored Lean source, WITHOUT a Lean build.

The reference sites (star-height and others) extract declarations from a compiled build
(ExtractDecls.lean) and identifier references from Lean's .ilean files. This site has not been
built yet (no Lean build is allowed on the shared box), so this script does the same job by
reading the source text:

  * declarations: top-level `def/theorem/lemma/abbrev/structure/inductive/instance` lines in the
    files listed in FILES, with their namespace, line range and verbatim header text;
  * mentions (meaningDeps) / proof uses (proofDeps): identifier tokens of the statement (and of a
    definition's body) / of a theorem's proof, resolved against the declarations found here;
  * Mathlib links: tokens that are in the hand-checked list MATHLIB below.

Every declaration is marked `"extracted": false` so the site and its Trust page say so. When the
projects are built on a capable machine, replace this with ExtractDecls.lean + build_xref.py.
"""
import hashlib, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "site/data")

# (repo-relative file, id prefix, namespace prefix stripped from ids)
PROJECTS = {
    "anthropic": {"prefix": "Anthropic.", "ns": "MainResults.", "files": [
        "vendor/anthropic-eth/MainResults.lean",
        "vendor/anthropic-eth/Solution.lean",
    ]},
    "openai": {"prefix": "OpenAI.", "ns": "OAI.Algorithms.SubexponentialSAT.", "files": [
        "vendor/openai-sat/ComparatorChallenges/SubexponentialSAT.lean",
        "vendor/openai-sat/OAI/Algorithms/SubexponentialSAT/SqrtLogSpace/Final.lean",
        "vendor/openai-sat/OAI/Algorithms/SubexponentialSAT/SubexpOrderedRawMainTheorem.lean",
    ]},
}
# The comparator statement file restates the theorem with `sorry`; the real proof is in Final.lean.
SKIP = {("vendor/openai-sat/ComparatorChallenges/SubexponentialSAT.lean", "OAI.Algorithms.SubexponentialSAT.SqrtLogSpace.exact_count_and_sat")}

# Mathlib / core names used in the headline statements (checked by hand against Mathlib's docs).
MATHLIB = """Turing.FinTM2 Turing.TM2ComputableAux Turing.TM2OutputsInTime Turing.Tape Turing.Tape.mk₁
Turing.Tape.move Turing.Tape.write Turing.Tape.head Turing.TM0.Stmt Turing.Dir Real.logb Real.log Real.sqrt
Finset Finset.univ Finset.filter Finset.card Finset.image Finset.sort Fintype Finite List List.Nodup
List.replicate List.flatMap List.range List.map List.foldr List.length Nat.log2 Nat.testBit Nat.bits
Function.update Fin Bool Nat Int Option Sum Sum.inl Sum.elim Int.ofNat Int.toNat Bool.toNat
Nat.floor DecidableEq NNReal ENNReal Nonempty iInf decide""".split()
ALIASES = {}
for n in MATHLIB:
    ALIASES.setdefault(n, n)
    if n.startswith("Turing."): ALIASES.setdefault(n[len("Turing."):], n)
ALIASES.update({"ℝ≥0": "NNReal", "ℝ≥0∞": "ENNReal", "⌊": None})

DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|partial|unsafe)\s+)*(def|theorem|lemma|abbrev|structure|inductive|class|instance)\s+([^\s:({\[]+)")
TOK = re.compile(r"[A-Za-z_\u00c0-\u024f\u0370-\u03ff\u1d00-\u1dbf\u2080-\u209f][\w.'\u00c0-\u024f\u0370-\u03ff\u1d00-\u1dbf\u2080-\u209f!?₀-₉]*")
OPEN, CLOSE = "([{⟨⦃", ")]}⟩⦄"


def cut(text, kind):
    """Header up to the top-level ':=' (or ' where' / first top-level '|' for defs). Whole text for types."""
    if kind in ("structure", "inductive", "class"): return text.rstrip(), ""
    depth = 0
    i = 0
    while i < len(text):
        c = text[i]
        if c in OPEN: depth += 1
        elif c in CLOSE: depth = max(0, depth - 1)
        elif depth == 0 and text.startswith(":=", i):
            return text[:i].rstrip(), text[i:]
        elif depth == 0 and kind != "theorem" and text[i] == "\n" and re.match(r"\n\s*\|", text[i:]):
            return text[:i].rstrip(), text[i:]
        i += 1
    return text.rstrip(), ""


def scan(file):
    lines = open(os.path.join(ROOT, file), encoding="utf-8").read().split("\n")
    ns, out = [], []
    in_comment = 0
    starts = []
    for k, ln in enumerate(lines):
        s = ln.strip()
        in_comment += ln.count("/-") - ln.count("-/")
        if in_comment > 0 and not s.startswith("/-"): continue
        if m := re.match(r"^namespace\s+(\S+)", ln): ns.append(m.group(1)); starts.append(("ns", k)); continue
        if m := re.match(r"^end\s+(\S+)\s*$", ln):
            if ns and ns[-1] == m.group(1): ns.pop()
            starts.append(("end", k)); continue
        if re.match(r"^(section|end|open|variable|universe|#print|/-|--)", ln): starts.append(("other", k)); continue
        if m := DECL.match(ln):
            name = m.group(2)
            full = ".".join(ns + [name]) if not name.startswith("_root_.") else name[7:]
            # `theorem MainResults.ethIsFalse` at top level: already fully qualified
            starts.append(("decl", k, m.group(1), full))
    for j, st in enumerate(starts):
        if st[0] != "decl": continue
        k, kind, full = st[1], st[2], st[3]
        end = (starts[j + 1][1] if j + 1 < len(starts) else len(lines)) - 1
        while end > k and not lines[end].strip(): end -= 1
        # a doc comment directly above belongs to the declaration
        doc = None
        if k > 0 and lines[k - 1].rstrip().endswith("-/"):
            a = k - 1
            while a > 0 and "/--" not in lines[a]: a -= 1
            doc = "\n".join(lines[a:k]).strip()
            doc = re.sub(r"^/--\s*|\s*-/$", "", doc)
        text = "\n".join(lines[k:end + 1])
        out.append({"name": full, "kind": "theorem" if kind == "lemma" else kind, "file": file,
                    "line": k + 1, "endLine": end + 1, "text": text, "doc": doc,
                    "ns": full.rsplit(".", 1)[0] if "." in full else ""})
    return out


def main():
    decls, names_by_proj = [], {}
    for pk, P in PROJECTS.items():
        for f in P["files"]:
            for d in scan(f):
                if (f, d["name"]) in SKIP: continue
                if not d["name"].startswith(P["ns"]): continue
                d["project"] = pk
                d["id"] = P["prefix"] + d["name"][len(P["ns"]):]
                decls.append(d)
    by_full = {d["name"]: d for d in decls}

    def resolve(tok, d):
        # exact full name, then current namespace and its parents, then any decl whose name ends with .tok
        if tok in by_full and by_full[tok]["project"] == d["project"]: return by_full[tok]
        ns = d["ns"].split(".") if d["ns"] else []
        for i in range(len(ns), 0, -1):
            c = ".".join(ns[:i] + [tok])
            if c in by_full: return by_full[c]
        cands = [e for e in decls if e["project"] == d["project"] and e["name"].endswith("." + tok)]
        return cands[0] if len(cands) == 1 else None

    for d in decls:
        stmt, proof = cut(d["text"], d["kind"])
        d["statement"] = stmt
        meaning_text = stmt if d["kind"] == "theorem" else d["text"]
        def deps(text):
            out = []
            clean = re.sub(r"--[^\n]*|/-[\s\S]*?-/", "", text)
            for m in TOK.finditer(clean):
                if m.start() and clean[m.start() - 1] == ".": continue  # x.toNat: a field/method, not a name
                t = m.group(0)
                for cand in (t, t.rstrip(".")):
                    e = resolve(cand, d)
                    if e and e is not d and e["id"] not in out: out.append(e["id"]); break
            return out
        d["meaningDeps"] = deps(meaning_text)
        d["proofDeps"] = [x for x in deps(proof) if x not in d["meaningDeps"]] if d["kind"] == "theorem" else []
        ml = []
        for t in TOK.findall(meaning_text):
            n = ALIASES.get(t) or ALIASES.get(t.split(".")[-1] if t.startswith("Turing.") else "")
            if n and n not in ml: ml.append(n)
        d["mathlib"] = ml
    ids = {d["id"]: d for d in decls}
    for d in decls: d["usedBy"] = sorted(e["id"] for e in decls if d["id"] in e["meaningDeps"] + e["proofDeps"])
    # depth: shortest distance from any headline along mentions and proof uses
    heads = ["Anthropic.ethIsFalse", "Anthropic.mainTheorem", "OpenAI.SqrtLogSpace.exact_count_and_sat"]
    dist = {h: 0 for h in heads if h in ids}
    frontier = list(dist)
    while frontier:
        nxt = []
        for i in frontier:
            for j in ids[i]["meaningDeps"] + ids[i]["proofDeps"]:
                if j not in dist: dist[j] = dist[i] + 1; nxt.append(j)
        frontier = nxt
    out = []
    for d in sorted(decls, key=lambda d: d["id"]):
        out.append({"id": d["id"], "name": d["name"], "kind": d["kind"], "file": d["file"],
                    "module": d["file"].rsplit("/", 1)[-1][:-5], "line": d["line"], "endLine": d["endLine"],
                    "statement": d["statement"], "variables": [], "truncated": False,
                    "mathlib": d["mathlib"], "meaningDeps": d["meaningDeps"], "proofDeps": d["proofDeps"],
                    "usedBy": d["usedBy"], "depth": dist.get(d["id"]), "project": d["project"],
                    "extracted": False})
    json.dump(out, open(os.path.join(OUT, "decls.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    # Heuristic xref (same format as build_xref.py) for every vendored .lean file.
    names, mods, ni, mi = [], [], {}, {}
    def nix(n):
        if n not in ni: ni[n] = len(names); names.append(n)
        return ni[n]
    def mix(m):
        if m not in mi: mi[m] = len(mods); mods.append(m)
        return mi[m]
    files = {}
    for dp, dns, fs in sorted(os.walk(os.path.join(ROOT, "vendor"))):
        dns.sort()
        for f in sorted(fs):
            if not f.endswith(".lean"): continue
            rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/")
            raw = open(os.path.join(ROOT, rel), "rb").read()
            text = raw.decode("utf-8")
            here = [d for d in decls if d["file"] == rel]
            refs = []
            for l0, ln in enumerate(text.split("\n")):
                code = ln.split("--", 1)[0]
                for m in TOK.finditer(code):
                    if m.start() and code[m.start() - 1] == ".": continue
                    t = m.group(0).rstrip(".")
                    c0 = len(ln[:m.start()].encode("utf-16-le")) // 2
                    c1 = c0 + len(t.encode("utf-16-le")) // 2
                    target, mod = None, None
                    proj = "anthropic" if rel.startswith("vendor/anthropic") else "openai"
                    ctx = here[0] if here else {"project": proj, "ns": PROJECTS[proj]["ns"].rstrip(".")}
                    # only resolve project names inside files that define project decls (avoid false hits)
                    e = resolve(t, ctx) if here or rel.endswith(("Challenge.lean", "Main.lean")) else None
                    if e and not (e["file"] == rel and e["line"] == l0 + 1):
                        target, mod = e["name"], "project"
                    elif t in ALIASES and ALIASES[t]:
                        target, mod = ALIASES[t], "Mathlib"
                    if target: refs.append([l0, c0, c1, nix(target), mix(mod)])
            files[rel] = {"sha256": hashlib.sha256(raw).hexdigest(),
                          "decls": [[nix(d["name"]), d["line"] - 1, d["endLine"] - 1] for d in here],
                          "refs": refs}
    json.dump({"version": 1, "heuristic": True, "names": names, "mods": mods, "files": files},
              open(os.path.join(OUT, "xref.json"), "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
    print(f"decls: {len(out)} ({sum(1 for d in out if d['depth'] is not None)} reachable); xref: {len(files)} files, {sum(len(v['refs']) for v in files.values())} refs")


if __name__ == "__main__":
    main()
