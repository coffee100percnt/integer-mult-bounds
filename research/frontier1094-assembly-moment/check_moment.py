#!/usr/bin/env python3
"""Integer-root check of the selected frontier1094 moment.

Complex width m = 73 is the hardcoded COMPLEX_WIDTH. It is not determined by
ASSEMBLY.json. No selected-record file encodes that width. The same value is
stated in research/selected-suppliers-de-diagnostic/README.md line 24
(m = 73, W = 14,336). W and n_r come from
research/community-frontier1094-audit/ASSEMBLY.json.
The checker imports nothing from this repository. Acceptance comparisons use
integers and fractions only.

The paid bill checked here is

    (1/W) * sum_r n_r * (r/m)^(1-a) < 1,

with a = kappa/(1-kappa) and kappa the selected assembly rational.
"""

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
ASSEMBLY = ROOT / "research/community-frontier1094-audit/ASSEMBLY.json"
OUT = Path(__file__).resolve().parent / "profiles.json"
PIN = "1122cb3a575f8c788345fc1bf4c108ac7c3250fb81a5988671f5eb04b3ab3045"
KAPPA = Fraction(836330098538459, 500000000000000000)
# Selected complex chart width. The histogram and call count do not determine
# it: three positive-deficit widths satisfy the same coverage identity.
COMPLEX_WIDTH = 73
COMPLEX_CENTRE = 64
STEPS = 128
ROOT_BITS = 160
LARGER_A = Fraction(1, 10**15)
FORMULA = re.compile(r"T\(2Kv-L\*cst\), L=(\d+) T=(\d+) K=(\d+) M=(\d+)\Z")


def fail(message, code=1):
    print(message)
    raise SystemExit(code)


def fraction_text(value):
    return f"{value.numerator}/{value.denominator}"


def decimal_bound(value, places, rounding):
    """Directed decimal of a rational. rounding is 'floor' or 'ceil'."""
    if places < 0:
        fail("decimal places", 2)
    sign = "-" if value < 0 else ""
    magnitude = -value if value < 0 else value
    scale = 10**places
    numerator = magnitude.numerator * scale
    denominator = magnitude.denominator
    if rounding == "floor":
        digits = numerator // denominator
    elif rounding == "ceil":
        digits = (numerator + denominator - 1) // denominator
    else:
        fail("unknown rounding", 2)
    # Floor/ceil of a negative value swaps the directed side.
    if value < 0 and rounding == "floor":
        digits = (numerator + denominator - 1) // denominator
        sign = "-"
    elif value < 0 and rounding == "ceil":
        digits = numerator // denominator
        sign = "-" if digits else ""
    whole = digits // scale
    frac = digits % scale
    return f"{sign}{whole}.{frac:0{places}d}"


def sqrt_floor(value, bits):
    if value <= 0:
        fail("square root of a non-positive value", 2)
    scale = 1 << bits
    squared = scale * scale
    root = math.isqrt((value.numerator * squared) // value.denominator)
    bound = Fraction(root, scale)
    if bound * bound > value:
        fail("integer square-root floor escaped its argument", 2)
    return bound


def sqrt_ceil(value, bits):
    if value <= 0:
        fail("square root of a non-positive value", 2)
    scale = 1 << bits
    squared = scale * scale
    root = math.isqrt((value.numerator * squared) // value.denominator)
    for _ in range(8):
        if Fraction(root, scale) ** 2 >= value:
            return Fraction(root, scale)
        root += 1
    fail("integer square-root ceil did not catch the argument", 2)


def pow_bounds(base, exponent):
    """Dyadic integer-root bounds for base^exponent, base > 1, 0 <= exponent < 1."""
    if base <= 1 or exponent < 0 or exponent >= 1:
        fail("power domain", 2)
    lower = upper = base
    chain_lower = []
    chain_upper = []
    for _ in range(STEPS):
        lower = sqrt_floor(lower, ROOT_BITS)
        upper = sqrt_ceil(upper, ROOT_BITS)
        if not (0 < lower <= upper):
            fail("root chain order", 2)
        chain_lower.append(lower)
        chain_upper.append(upper)
    scale = 1 << STEPS
    numerator = (exponent.numerator * scale) // exponent.denominator
    if numerator + 1 >= scale:
        fail("exponent does not fit the dyadic window", 2)

    def product(chain, power):
        acc = Fraction(1)
        bit = 0
        while power:
            if power & 1:
                acc *= chain[STEPS - 1 - bit]
            power >>= 1
            bit += 1
        return acc

    below = product(chain_lower, numerator)
    above = product(chain_upper, numerator + 1)
    if not (below <= above):
        fail("power bounds crossed", 2)
    return below, above


def moment_bounds(histogram, width, roles, exponent):
    if width <= 1 or roles <= 0:
        fail("profile dimensions", 2)
    lower = Fraction(0)
    upper = Fraction(0)
    for rank, count in histogram.items():
        if type(rank) is not int or type(count) is not int:
            fail("histogram entry type", 2)
        if not (0 < rank < width and count > 0):
            fail("histogram support", 2)
        power_lower, power_upper = pow_bounds(Fraction(width, rank), exponent)
        weight = Fraction(count * rank, width * roles)
        lower += weight * power_lower
        upper += weight * power_upper
    if not (lower <= upper):
        fail("moment bounds crossed", 2)
    return lower, upper


def load_assembly(raw):
    digest = hashlib.sha256(raw).hexdigest()
    if digest != PIN:
        fail(f"HASH_REJECTED {digest}")
    try:
        assembly = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"assembly json: {exc}", 2)
    if Fraction(assembly["kappa"]) != KAPPA:
        fail("assembly kappa differs from the selected rational", 2)
    return assembly


def positive_integers(mapping):
    if type(mapping) is not dict or not mapping:
        fail("histogram object", 2)
    parsed = {}
    for key, count in mapping.items():
        if type(key) is not str or not key.isdecimal() or type(count) is not int:
            fail("histogram encoding", 2)
        rank = int(key)
        if str(rank) != key:
            fail("histogram key", 2)
        parsed[rank] = count
    return parsed


def complex_profile(assembly):
    if assembly["surcharge_model"]["complex"] is not False:
        fail("complex surcharge is present; the unsurcharged bill is not the paid bill", 2)
    if assembly["binding"] != "complex":
        fail("assembly binding side", 2)
    counts = assembly["provider_counts"]
    if list(counts) != ["gauge44"] or type(counts["gauge44"]) is not int or counts["gauge44"] <= 0:
        fail("provider counts", 2)
    calls = counts["gauge44"]
    histogram = positive_integers(assembly["complex_profile"])
    rank_mass = sum(rank * count for rank, count in histogram.items())
    numerator = rank_mass - COMPLEX_CENTRE * calls
    if numerator <= 0 or numerator % (COMPLEX_WIDTH - 1) != 0:
        fail("complex coverage identity does not produce an integer role count", 2)
    roles = numerator // (COMPLEX_WIDTH - 1)
    deficit = COMPLEX_WIDTH * roles - rank_mass
    if deficit != roles - COMPLEX_CENTRE * calls or deficit <= 0:
        fail("complex deficit identity", 2)
    if max(histogram) >= COMPLEX_WIDTH:
        fail("complex child rank", 2)
    return {
        "supplier": "complex",
        "m": COMPLEX_WIDTH,
        "W": roles,
        "n_r": histogram,
        "calls": calls,
        "centre_rank_per_call": COMPLEX_CENTRE,
        "rank_mass": rank_mass,
        "deficit": deficit,
        "surcharge": False,
    }


def bit_profile(assembly):
    if assembly["surcharge_model"]["bit"] is not True:
        fail("bit surcharge flag", 2)
    supplier = assembly["bit_supplier"]
    match = FORMULA.fullmatch(supplier["deficit_formula"])
    if match is None:
        fail("bit deficit formula", 2)
    stages, replicas, ports, width = (int(piece) for piece in match.groups())
    word = supplier["word"]
    live_ports = word["v"]
    decoder = word["decoder_constant"]
    copy_ranks = word["copy_ranks"]
    if type(live_ports) is not int or type(decoder) is not int or type(copy_ranks) is not list:
        fail("bit word encoding", 2)
    if len(copy_ranks) != stages or any(type(rank) is not int or not 0 < rank <= 8 for rank in copy_ranks):
        fail("bit copy ranks", 2)
    if sum(copy_ranks) != decoder:
        fail("decoder constant is not the copy-rank sum", 2)
    if type(supplier["derived_deficit"]) is not int:
        fail("derived deficit encoding", 2)
    roles = 2 * ports * live_ports * replicas
    deficit = replicas * (2 * ports * live_ports - stages * decoder)
    if deficit != supplier["derived_deficit"] or roles <= 0 or deficit <= 0 or width <= 1:
        fail("bit profile identity", 2)
    rank_mass = width * roles - deficit
    if rank_mass <= 0:
        fail("bit rank mass", 2)
    return {
        "supplier": "bit",
        "m": width,
        "W": roles,
        "n_r": None,
        "calls": None,
        "rank_mass": rank_mass,
        "deficit": deficit,
        "surcharge": True,
        "parameters": {
            "L": stages,
            "T": replicas,
            "K": ports,
            "v": live_ports,
            "decoder_constant": decoder,
        },
        "moment_status": "not_certified",
        "reason": (
            "ASSEMBLY.json records the bit width, role count and deficit formula, "
            "but it does not record n_r. The moment sum is not determined by "
            "(m, W, deficit) alone, and the retained bad-residue surcharge needs "
            "the same histogram."
        ),
    }


def moment_of(profile, exponent):
    return moment_bounds(profile["n_r"], profile["m"], profile["W"], exponent)


def certificate_from(lower, upper):
    if not upper < 1:
        fail(f"MOMENT_REJECTED upper={fraction_text(upper)}")
    margin_lower = 1 - upper
    margin_upper = 1 - lower
    return {
        "moment_minus_one": [fraction_text(lower - 1), fraction_text(upper - 1)],
        "margin": [fraction_text(margin_lower), fraction_text(margin_upper)],
        "margin_decimal": [
            decimal_bound(margin_lower, 36, "floor"),
            decimal_bound(margin_upper, 36, "ceil"),
        ],
        "sign": "negative",
        "accepted": True,
    }


def positive_fixture():
    lower, upper = pow_bounds(Fraction(4), Fraction(1, 2))
    if not (lower <= 2 <= upper):
        fail("fixture missed the exact square root of 4", 2)
    zero_lower, zero_upper = moment_bounds({1: 1}, 2, 1, Fraction(0))
    if zero_lower != Fraction(1, 2) or not zero_upper < 1:
        fail("fixture missed the exact zero-exponent bill 1/2", 2)
    half_lower, half_upper = moment_bounds({1: 1}, 2, 1, Fraction(1, 2))
    if not (0 < half_lower <= half_upper < 1):
        fail("fixture rejected a one-child half-exponent bill", 2)


def selected_exponent():
    return KAPPA / (1 - KAPPA)


def prepared(raw, mutate=None):
    assembly = load_assembly(raw)
    profile = complex_profile(assembly)
    if mutate is not None:
        mutate(profile)
    return assembly, profile


def emit(assembly_profile, certificate, bit):
    payload = {
        "assembly_sha256": PIN,
        "kappa": fraction_text(KAPPA),
        "a": fraction_text(selected_exponent()),
        "relation": "a = kappa/(1-kappa)",
        "bill": "(1/W)*sum n_r*(r/m)^(1-a) < 1",
        "enclosure": {
            "method": "successive integer square roots, then the dyadic bits of a",
            "root_steps": STEPS,
            "root_bits": ROOT_BITS,
        },
        "suppliers": {
            "complex": {
                "m": assembly_profile["m"],
                "W": assembly_profile["W"],
                "n_r": {str(rank): count for rank, count in sorted(assembly_profile["n_r"].items())},
                "calls": assembly_profile["calls"],
                "centre_rank_per_call": assembly_profile["centre_rank_per_call"],
                "rank_mass": assembly_profile["rank_mass"],
                "deficit": assembly_profile["deficit"],
                "surcharge": False,
                "moment_minus_one": certificate["moment_minus_one"],
                "margin": certificate["margin"],
                "margin_decimal_floor_ceil": certificate["margin_decimal"],
                "sign": certificate["sign"],
                "accepted": True,
            },
            "bit": {
                "m": bit["m"],
                "W": bit["W"],
                "n_r": None,
                "rank_mass": bit["rank_mass"],
                "deficit": bit["deficit"],
                "surcharge": True,
                "parameters": bit["parameters"],
                "moment_minus_one": None,
                "margin": None,
                "sign": None,
                "accepted": False,
                "moment_status": bit["moment_status"],
                "reason": bit["reason"],
            },
        },
        "minimum_certified_margin": certificate["margin"][0],
        "minimum_certified_margin_decimal_floor": certificate["margin_decimal"][0],
        "minimum_supplier": "complex",
    }
    text = json.dumps(payload, indent=2) + "\n"
    OUT.write_text(text, encoding="utf-8")
    print("PASS_FRONTIER1094_ASSEMBLY_MOMENT")
    print(f"complex_margin {certificate['margin_decimal'][0]} {certificate['margin_decimal'][1]}")
    print(f"minimum_certified_margin {certificate['margin_decimal'][0]} supplier=complex")
    print("bit_moment not_certified n_r_absent")


def main(argv):
    positive_fixture()
    mode = argv[1] if len(argv) > 1 else "--assembly"
    if mode == "--fixture":
        print("PASS_POSITIVE_FIXTURE")
        return 0
    raw = ASSEMBLY.read_bytes()
    exponent = selected_exponent()
    if mode == "--assembly":
        _assembly, profile = prepared(raw)
        certificate = certificate_from(*moment_of(profile, exponent))
        emit(profile, certificate, bit_profile(_assembly))
        return 0
    if mode != "--control" or len(argv) != 3:
        fail("usage: check_moment.py [--fixture | --control perturbed-nr|larger-a|tampered-hash]", 2)
    control = argv[2]
    if control == "tampered-hash":
        tampered = bytearray(raw)
        tampered[-1] ^= 1
        digest = hashlib.sha256(tampered).hexdigest()
        if digest == PIN:
            fail("tamper collided with the pin", 2)
        fail(f"HASH_REJECTED {digest}")
    if control == "perturbed-nr":
        def mutate(profile):
            profile["n_r"][48] = profile["n_r"][48] + 1
        _assembly, profile = prepared(raw, mutate)
        lower, _upper = moment_of(profile, exponent)
        if not lower > 1:
            fail("perturbed histogram was not proved above 1", 2)
        print("REJECTED perturbed-nr")
        return 1
    if control == "larger-a":
        _assembly, profile = prepared(raw)
        lower, _upper = moment_of(profile, exponent + LARGER_A)
        if not lower > 1:
            fail("larger exponent was not proved above 1", 2)
        print("REJECTED larger-a")
        return 1
    fail("unknown control", 2)


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv))
    except SystemExit:
        raise
    except Exception as exc:
        fail(f"unexpected {type(exc).__name__}: {exc}", 2)
