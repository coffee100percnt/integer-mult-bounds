# Local task card

Task ID / proposed scope key: `independent-moment` / `independent-moment`

Catalogue method fingerprint for the enclosure method: `c191650c0fa8d2fa514e`.
The donor named the scope key `independent-moment`. Priority revision 3.

Base commit; exact predecessor and dependency heads:
`0b1cccf86e2f5132ed286a26ef0a681a495740ea`
(upstream `CrocSwap/integer-mult-bounds` `main` at branch creation; the fork
`main` was the same SHA). Selected assembly
`research/community-frontier1094-audit/ASSEMBLY.json`, sha256
`1122cb3a575f8c788345fc1bf4c108ac7c3250fb81a5988671f5eb04b3ab3045`,
git blob `5fd676df060f3b450782fdf5ff5f6beb63a5eeb0`.
The same digest was checked against `upstream/main`.

Concrete object and question:
Selected frontier1094 κ = `836330098538459/500000000000000000`.
For each supplier, recompute the paid profile `(m, W, n_r)`, then decide the sign of

`(1/W) * Σ n_r (r/m)^(1-a) - 1`

at `a = κ/(1-κ)` by an integer-root enclosure.

Scope status: refined. The card's question and the enclosure method stay.
The domain is this one assembly. The complex histogram is in the file.
The bit histogram is not, so that moment is left open.

Existing restriction being changed (or exact claim being audited):
The selected assembly's moment claim at the frontier κ. No new κ.

Method; explicit parameter ranges/candidate alphabet:
Successive integer square roots (128 steps, 160 bits) and the dyadic bits of
`a`. Complex width `m = 73` is hardcoded as `COMPLEX_WIDTH` in
`check_moment.py`. It is not determined by `ASSEMBLY.json`. No selected-record
file encodes that width. The same value is stated in
`research/selected-suppliers-de-diagnostic/README.md` line 24
(`m = 73`, `W = 14,336`). One centre rank-64 unit per call.
`W` and `n_r` come from `ASSEMBLY.json`:
`W = (Σ r n_r - 64 N) / 72` with `N = provider_counts.gauge44`.
Bit `m`, `W` and the deficit are parsed from `bit_supplier`.

Nearest overlapping work and why this adds something:
`research/selected-suppliers-de-diagnostic` checks endpoint residuals and the
`a < D/E` screen, and it reads the bit `EXPECTED.json`.
`research/frontier1094-emitted-ledger-seed78` rebuilds the complex histogram
from the emitted program. This package does neither: it encloses the selected-κ
bill from the assembly histogram at the hardcoded width, with a fresh root chain.

Optimistic full cost budget; required observable improvement:
No supplier change and no κ gain. The observable is a certified negative
complex residual, plus the bit fields the assembly actually determines.

Success evidence; falsification test; time/compute cap:
`profiles.json`. Positive fixture: `4^(1/2)` contains 2, and the one-child
`a = 0` bill equals `1/2`. Failure controls: rank 48 incremented by 1,
`a + 1/10^15`, and one flipped assembly byte. Each must exit 1.

Predecessor authors; intended artifact and reproduction command:
Rohan Arun's PR1094, Jeremy Kothe's T16 packing lineage, Hao Yan's controller,
the PR589/PR555 bit supplier, and the batch1099 owner/price audits of Josie
Elliston and Sagar Thakrar. Artifact: `research/frontier1094-assembly-moment/`.
Command: `python3 -B research/frontier1094-assembly-moment/check_moment.py`.

Coordination limitation: Discussions #1163 and #1166 were read. The donor
forbade Discussion posts, review comments and pull requests, so no claim was
posted.
