# Ovsienko–Tabachnikov's dual Somos integrality conjectures

## Result and sources

This revision-2 note extends Hone's divisibility proof (SIGMA 3 (2007),
022, Section 3, Proposition 1) to the conjectures immediately after
Corollary 5.2 in Ovsienko–Tabachnikov, arXiv:1705.01623v1, Section 5.4,
printed pages 10–11. The bibliography in `note.tex` gives the scientific
references and exact versions.

For positive integers `p,q`, integer weights `u,v`, and any fixed integer
initial shadows `c_0,c_1,c_2,c_3`, put `A_j=1+c_j ε`, `ε²=0`, for
`0≤j≤3`, and

```text
A_(n+4) A_n = (1+u ε)(A_(n+1) A_(n+3))^p + (1+v ε) A_(n+2)^q.
```

Writing `A_n=a_n+b_n ε`, all shadows `b_n` are integral exactly when
`(q−2)u=(2p−2)v`. If `κ=(2p−2)v−(q−2)u≠0` and
`m=min{n≥4 : a_n does not divide κ}`, the first noninteger shadow is
`b_(m+4)` with reduced denominator `a_m/gcd(a_m,κ)`. The note also covers
both singly weighted families, the admissible-weight lattice, affine
superposition, the `p=1,q=0,u=1,v=0` boundary case, and a finite sign
counterexample for the fourth classical homogeneous shadow.

## Files

- `note.tex`: the self-contained LaTeX source, including bibliography.
- `verify.py`: two exact-rational implementations and finite checks.
- `verification.json`: the expected checker output.
- `shadow-certificate.csv`: 26 exact real/shadow pairs for indices 0–25.
- `metadata.json`: revision, creators, license, problem ID, and evidence link.
- `SHA256SUMS`: SHA-256 hashes of the other files in the source archive.

The matching `note.pdf` accompanies the source archive separately. No external
figures, bibliography database, or additional TeX inputs are needed.

## Rebuild the PDF

Use Tectonic 0.17.0 from the directory containing `note.tex`:

```sh
tectonic --untrusted --outdir . note.tex
```

Alternatively, a standard TeX installation with the packages named in the
preamble can use:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is inline, so BibTeX is unnecessary. Repeated TeX passes
resolve the theorem, section, and bibliography references.

## Check the finite computations

Python 3.10 or later, using its standard library, is sufficient:

```sh
sha256sum -c SHA256SUMS
python3 verify.py --output verification.recomputed.json
cmp verification.json verification.recomputed.json
```

The output has `status: pass`. The principal grid contains 24,900 orbits,
249,000 coefficient comparisons, 174,300 coprime-window checks, and 44,820
local-divisibility and reduced-denominator checks, using
`p=1..3`, `q=1..4`, `u,v=−2..2`, 83 initial tuples, and indices 0–9.
Additional checks cover 83 `q=0` examples and every row of the sign certificate.
Arithmetic uses exact fractions, with no rounding.

## Proof coverage

The infinite simultaneous-weight classification and exact-denominator formula
have written proofs in `note.tex`; the finite computations supplement those
proofs. The pinned Lean source is:

https://github.com/the-omega-institute/trureturing/blob/256870690452e5629b1260ae620f2d647417e857/D5/S1/Recurrence/Invariants/SomosFirstDualIntegrality.lean

Its declaration
`D5.S1.Recurrence.Invariants.SomosFirstDualIntegrality.result`
covers the original first family `u=0,v=1`, positive `p,q`, arbitrary fixed
integer initial shadows, integrality exactly when `p=1`, existence,
uniqueness, positive real parts, and the rational/real dual correspondence.
The simultaneous-weight classification, second-family converse, exact failure
denominators, and `q=0` boundary assertion are the written results of this
note. The sign counterexample is certified by the finite recurrence identities
and `shadow-certificate.csv`. No conclusion about eventual signs or the two
forced-shadow positivity and growth conjectures is asserted.

## Creators and license

Haobo Ma — ChronoAI Pte Ltd, Singapore.

Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

Copyright 2026 Haobo Ma and Wenlin Zhang. Licensed under Creative Commons
Attribution 4.0 International (CC BY 4.0):
https://creativecommons.org/licenses/by/4.0/
