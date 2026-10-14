# Reproduction finding: frontier1094 complex moment

**Downgrade.** This is not a new claim and not a pull request.
`research/selected-suppliers-de-diagnostic` already certifies the complex-side
moment sign for the selected frontier1094 assembly. The integer-root run in
this directory is a second implementation of that sign, kept on the branch
for reference.

## Pins

| Pin | Value |
|---|---|
| Upstream `CrocSwap/integer-mult-bounds` `main` | `0b1cccf86e2f5132ed286a26ef0a681a495740ea` |
| `research/community-frontier1094-audit/ASSEMBLY.json` sha256 | `1122cb3a575f8c788345fc1bf4c108ac7c3250fb81a5988671f5eb04b3ab3045` |

The sha256 was computed from `upstream/main`'s copy of that file and matches
the worktree bytes.

## Method

Successive integer square roots (`math.isqrt`, 128 steps, 160-bit dyadic
roots), then the dyadic bits of the exponent. The sole input is
`ASSEMBLY.json`. The checker imports nothing from this repository and does
not copy `scripts/verify_frontier1094.py`,
`research/community-batch1099-audit/check_frontier1094.py`, or
`research/selected-suppliers-de-diagnostic/verify.py`. Acceptance comparisons
use integers and `fractions.Fraction` only.

The exponent is `a = κ/(1−κ)` with
`κ = 836330098538459/500000000000000000`, so
`a = 836330098538459/499163669901461541`.
The complex profile is the assembly histogram at width `m = 73`,
`W = 14336`, no surcharge. The bill is
`(1/W) Σ n_r (r/m)^(1−a) < 1`.

## Complex margin, and the two published values

This run's certified margin `1 − moment` at `a = κ/(1−κ)` is

`[0.000000000000000001936096349948151878, 0.000000000000000001936096349948151879]`.

The residual is negative, so the complex bill is strictly under 1.

`research/selected-suppliers-de-diagnostic/RESULT.json` prices a different
exponent, the recorded complex endpoint, and records:

```json
"endpoint": "67018507072324140917/40000000000000000000000",
"residual_decimal": ["-0.000000000000000000000001304215", "-0.000000000000000000000001304215"],
"next_grid_decimal": ["0.000000000000000000000001624723", "0.000000000000000000000001624723"],
"accept": true
```

`research/community-frontier1094-audit/INDEPENDENT1094.json` records the same
endpoint and:

```json
"complex_lower": "67018507072324140917/40000000000000000000000",
"moment_minus_one": [-1.3042153285555122e-24, 1.6247237581095317e-24]
```

The first `moment_minus_one` entry is the endpoint residual. The second is
the next-grid residual, which is positive.

**Sign agreement.** Both published checks and this run find the complex paid
bill strictly below 1 (`accept: true` there; negative residual here).

**Numeric disagreement, expected.** The published residuals are at
`a = 67018507072324140917/40000000000000000000000`. This run is at
`a = κ/(1−κ)`. The endpoint exceeds `κ/(1−κ)` by
`13198339462995539973097/19966546796058461640000000000000000000000`
(about `6.61022×10^−19`). This run does not reproduce
`−1.304215×10^−24`. A smaller exponent leaves a wider gap under 1, about
`1.936×10^−18` here. `make frontier1094-verify` was still running when this
note was written and was not used.

## Controls

`python3 -B research/frontier1094-assembly-moment/test_controls.py` printed
`PASS_MOMENT_CONTROLS fixture=0 assembly=0 perturbed-nr=1 larger-a=1 tampered-hash=1`.

| Command | Exit | Result |
|---|---:|---|
| `check_moment.py` | 0 | `PASS_FRONTIER1094_ASSEMBLY_MOMENT` |
| `check_moment.py --fixture` | 0 | `PASS_POSITIVE_FIXTURE` |
| `check_moment.py --control perturbed-nr` | 1 | `REJECTED perturbed-nr` |
| `check_moment.py --control larger-a` | 1 | `REJECTED larger-a` |
| `check_moment.py --control tampered-hash` | 1 | `HASH_REJECTED` |

## Not checked

- Bit rank counts. They are not pinned in `ASSEMBLY.json` and were not
  inferred from any other file.
- H1–H5.
- Hosting.
- The all-size transfer.

## Existing `independent-moment` packages

- `research/selected-suppliers-de-diagnostic` — exact complex moment sign at
  the recorded endpoint, plus the bit ledger. Inputs are `ASSEMBLY.json` and
  the bit `EXPECTED.json` histogram. No shared engine code. Arithmetic is
  rational square-root bisection for `ln`, then a Taylor `exp`. This is the
  package that already covers the complex-side sign check.
- `research/frontier1094-emitted-ledger-seed78` — rebuilds the complex
  histogram from the emitted hosted program and matches `complex_profile`.
  Input is the certificate plus that program. Code-disjoint standard library.
  No moment bill.
- `research/pr1293-log-enclosure-audit` — exact rational counterexample for
  the pinned `ln_exp_bisection` contract. Input is that logarithm routine,
  not `ASSEMBLY.json`. No selected complex moment.
- `research/bit589-projector-ledger` — reconstructs the PR555/PR589 bit
  histograms from source gates with rational projectors. Input is the bit
  words, not the complex assembly moment.
- `research/p112-asymmetric-unit-audit-seed43` — exact replay of the P112
  `d0=77` witness (pairing and F2 ranks). Input is that witness. No
  frontier1094 moment.
- `research/hpe-lean-semantic-binding` — not this card. Its task file only
  records that `independent-moment` was passed over because the endpoint
  engines, the PR1293 diagnostic, and the emitted-ledger package already
  cover the selected record.

## Credit

Frontier 1094 is Rohan Arun's PR1094 on Jeremy Kothe's T16 packing lineage
and Hao Yan's controller, with the retained PR589/PR555 bit supplier.
Batch 1099's owner audit is Josie Elliston's and its pricing pass is Sagar
Thakrar's, composed by Douglas Colkitt. The prior exact complex-side sign
check is Navinor's `research/selected-suppliers-de-diagnostic` (with help
from opencode). Those programs were not imported or copied.

## AI assistance

Contributor: Miley. Substantial assistance from Cursor Grok 4.7. The checker,
this note, and the local control run were drafted and executed by the
assistant. No independent human mathematical review is claimed.
