# frontier1094 assembly moment

**Independent verification of one selected bill. No new κ.** The selected
record is unchanged.

Contributor: Miley. Substantial assistance from Cursor cloud agent (AI). Apache-2.0.
Task card: [TASK-CARD.md](TASK-CARD.md). Metadata: [TASK.json](TASK.json).

## Scope and evidence

The complex width `m = 73` is hardcoded as `COMPLEX_WIDTH` in
[`check_moment.py`](check_moment.py). It is not determined by `ASSEMBLY.json`.
No selected-record file encodes that width. The same value is stated in
[`research/selected-suppliers-de-diagnostic/README.md`](../selected-suppliers-de-diagnostic/README.md)
line 24 (`m = 73`, `W = 14,336`). All other complex profile data (`W`, `n_r`) comes from
[`research/community-frontier1094-audit/ASSEMBLY.json`](../community-frontier1094-audit/ASSEMBLY.json).

| Pin | Value |
|---|---|
| Upstream `main` base | `0b1cccf86e2f5132ed286a26ef0a681a495740ea` |
| sha256 | `1122cb3a575f8c788345fc1bf4c108ac7c3250fb81a5988671f5eb04b3ab3045` |
| git blob | `5fd676df060f3b450782fdf5ff5f6beb63a5eeb0` |

The same sha256 was computed from the working file and from
`upstream/main:research/community-frontier1094-audit/ASSEMBLY.json`.

Selected κ = `836330098538459/500000000000000000`.
The exponent is the exact rational

`a = κ/(1-κ) = 836330098538459/499163669901461541`.

The bill is `(1/W) Σ n_r (r/m)^(1-a) < 1`. Acceptance comparisons use
integers and `fractions.Fraction` only. `math.isqrt` is the integer square
root. The checker imports nothing from this repository, and it does not import
or copy `scripts/verify_frontier1094.py` or
`research/community-batch1099-audit/check_frontier1094.py`.

### How the enclosure works

For each child rank `r`, write `(r/m)^(1-a) = (r/m) (m/r)^a`.
Take 128 successive integer square roots of `m/r`, each kept as a dyadic
rational with denominator `2^160`. The binary digits of `a` multiply a subset
of those roots. The product of the floor roots is a lower bound on
`(m/r)^(N/2^128)`, and the product of the ceil roots at the next dyadic is an
upper bound. Both comparisons are exact integer comparisons.

### Recomputed profiles

Complex width `m = 73` is the hardcoded `COMPLEX_WIDTH`. The histogram and the
call count do not determine it: three positive-deficit widths satisfy
`Σ r n_r - 64 N` divisible by `m - 1`. Given `m = 73` and one centre unit of
rank 64 on each of the `N = 144` gauge44 calls,

`W = (Σ r n_r - 64·144) / 72 = 14336`,

and the deficit identity `73 W - Σ r n_r = W - 64·144 = 5120` holds.
There is no complex surcharge (`surcharge_model.complex` is false), so this
sum is the paid bill.

| Rank | Count |
|---:|---:|
| 1 | 349604 |
| 2 | 60192 |
| 3 | 62585 |
| 4 | 20448 |
| 5 | 11808 |
| 7 | 7 |
| 8 | 1152 |
| 48 | 4866 |

Bit parameters are read from `bit_supplier`: `M = 64`, `L = 9`, `T = 32`,
`K = 4`, `v = 111`, decoder constant 63 equal to the nine copy ranks.
Then `W = 2·K·v·T = 28416` and
`deficit = T(2Kv - L·cst) = 10272`, matching `derived_deficit`.
Rank mass `64·28416 - 10272 = 1808352`. The assembly does not contain `n_r`,
and the moment is not a function of `(m, W, deficit)` alone. The bit
bad-residue surcharge is recorded as present and is not evaluated.

### Certified complex margin

The complex residual `moment - 1` is a strictly negative interval. Its
endpoints are the exact fractions in [profiles.json](profiles.json). At 36
decimal places the margin `1 - moment` lies in

**[0.000000000000000001936096349948151878, 0.000000000000000001936096349948151879]**.

That lower endpoint is the minimum certified margin. The only certified
supplier is complex. The bit margin is not certified.

| Supplier | `m` | `W` | `n_r` | Margin |
|---|---:|---:|---|---|
| complex | 73 | 14336 | assembly histogram | **[1.936096349948151878 × 10⁻¹⁸, 1.936096349948151879 × 10⁻¹⁸]** |
| bit | 64 | 28416 | absent | not certified |

## Reproduce

From the repository root:

```sh
python3 -B research/frontier1094-assembly-moment/check_moment.py
python3 -B research/frontier1094-assembly-moment/check_moment.py --fixture
python3 -B research/frontier1094-assembly-moment/check_moment.py --control perturbed-nr
python3 -B research/frontier1094-assembly-moment/check_moment.py --control larger-a
python3 -B research/frontier1094-assembly-moment/check_moment.py --control tampered-hash
python3 scripts/research_package.py --package research/frontier1094-assembly-moment --check-only
```

Expected outcomes:

| Command | Exit | Expected text |
|---|---:|---|
| `check_moment.py` | 0 | `PASS_FRONTIER1094_ASSEMBLY_MOMENT` |
| `--fixture` | 0 | `PASS_POSITIVE_FIXTURE` |
| `--control perturbed-nr` | 1 | `REJECTED perturbed-nr` |
| `--control larger-a` | 1 | `REJECTED larger-a` |
| `--control tampered-hash` | 1 | `HASH_REJECTED` |

`test_controls.py` runs those five commands and requires those exit codes.
The positive fixture checks that the enclosure of `4^(1/2)` contains 2 and
that one rank-1 child of width 2 at `a = 0` has moment exactly `1/2`.
`perturbed-nr` adds one rank-48 child. `larger-a` uses `a + 1/10^15`.
`tampered-hash` flips the last assembly byte before the pin comparison.
Each rejection is proved: the perturbed and larger-`a` bills have a lower
bound strictly above 1, and the flipped byte's sha256 differs from the pin.

## Obligations not checked

- **H1–H5.** The bit scalar-interface hypotheses (gate directions, frames,
  ordering and cleanup) are not replayed.
- **Hosting.** Whole-call hosting, owner placement and idle realization are
  not replayed.
- **The all-size transfer.** The uniform all-size compiler and the analytic
  passage from this finite bill to a multiplication exponent are not proved.
- The bit histogram moment and its bad-residue surcharge.
- Reconstruction of either supplier from its circuit.
- Bootstrap cutoffs, the 47 outer inequalities, and the conservative
  complex-surcharge endpoints stored in the assembly.
- Any claim that this finite bill is a complete multiplication theorem.
- Cross-check against `make frontier1094-verify` was not run, because an
  independent replay on full history fails in the ancestor step of the
  baseline799 chain (the original run was also still going after 34 min).

## Open next questions

1. **What exact margin does the selected κ give the PR589 bit supplier once
   its paid histogram is available?** The assembly prices both suppliers, and
   the bit bill keeps a bad-residue surcharge. This package recomputes bit
   `m`, `W` and the deficit, but `n_r` is not in `ASSEMBLY.json`, so the bit
   moment is still unchecked. First step: pin the nine-stage histogram named
   by `bit_supplier.git_blob_sha1` and run this same integer-root bill,
   including the surcharge term. Blocked by the histogram living outside
   `ASSEMBLY.json`. Adding it changes the input domain fixed here.

2. **Can the complex residual be replaced by an exact rational value at this
   same `a`?** The sign and a `10^-36` decimal gap are already certified. An
   exact value would remove the dyadic window from the reported margin.
   First step: enclose the rank-48 term a second way at a higher root-bit
   count and compare the intervals. Blocked by `(m/r)^a` not being rational
   for this `a`; only a tighter enclosure is expected.

## Credit

Frontier 1094 is Rohan Arun's PR1094 on Jeremy Kothe's T16 packing lineage
and Hao Yan's controller, with the retained PR589/PR555 bit supplier.
Batch 1099's independent owner audit is Josie Elliston's and its pricing
pass is Sagar Thakrar's, composed in
`research/community-batch1099-audit/check_frontier1094.py` by Douglas Colkitt.
Those programs were not imported or copied. The integer-root checker in this
directory is new.

## AI assistance

Substantial assistance from Cursor cloud agent (AI). The checker, enclosure, package
text and local runs were drafted and executed by the assistant. No independent
human mathematical review is claimed.
