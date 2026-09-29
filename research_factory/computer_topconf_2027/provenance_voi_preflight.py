"""Level-0 structural preflight for sequential provenance information acquisition.

This module uses only the frozen Tulu-3 source universe, frozen ambiguity classes,
and TAGCOS development class-resolution counts. It does not read held-out
provenance outcomes.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache

K = 5

# Frozen Tulu-3 ambiguous source universe. Class 2 = multi-record; class 3 = no direct record.
SOURCES = (
    ("CoCoNot", 10_983, 3),
    ("Tulu 3 Persona Algebra", 20_000, 3),
    ("FLAN v2", 89_982, 2),
    ("OpenAssistant Guanaco", 7_132, 2),
    ("Tulu 3 Persona MATH", 149_960, 3),
    ("Tulu 3 Persona GSM", 49_980, 3),
    ("NuminaMath-TIR", 64_312, 3),
    ("Tulu 3 WildGuardMix", 50_000, 3),
    ("Tulu 3 WildJailbreak", 50_000, 3),
    ("Tulu 3 Math Grade", 50_000, 3),
    ("Tulu 3 Persona Python", 34_999, 3),
    ("Tulu 3 Hardcoded", 240, 3),
    ("Aya", 100_000, 2),
    ("Tulu 3 Persona IF", 29_980, 3),
    ("TableGPT", 5_000, 3),
    ("SciRIFF", 10_000, 3),
    ("Evol CodeAlpaca", 107_276, 3),
)

# Frozen TAGCOS development outcomes:
# class 2 resolved 5/6 -> Beta(5,1); class 3 resolved 1/4 -> Beta(1,3).
INITIAL_POSTERIOR = (5, 1, 1, 3)

STATIC_K5_SET = frozenset(
    {
        "Aya",
        "FLAN v2",
        "Tulu 3 Persona MATH",
        "Evol CodeAlpaca",
        "NuminaMath-TIR",
    }
)


@lru_cache(maxsize=None)
def _optimal_value_and_action(
    remaining: tuple[int, ...],
    alpha2: int,
    beta2: int,
    alpha3: int,
    beta3: int,
    horizon: int,
) -> tuple[Fraction, int | None]:
    if horizon == 0 or not remaining:
        return Fraction(0), None

    best_value: Fraction | None = None
    best_action: int | None = None

    for index in remaining:
        _name, mass, ambiguity_class = SOURCES[index]
        if ambiguity_class == 2:
            alpha, beta = alpha2, beta2
        else:
            alpha, beta = alpha3, beta3

        p_resolve = Fraction(alpha, alpha + beta)
        next_remaining = tuple(i for i in remaining if i != index)

        if ambiguity_class == 2:
            success_future, _ = _optimal_value_and_action(
                next_remaining, alpha2 + 1, beta2, alpha3, beta3, horizon - 1
            )
            failure_future, _ = _optimal_value_and_action(
                next_remaining, alpha2, beta2 + 1, alpha3, beta3, horizon - 1
            )
        else:
            success_future, _ = _optimal_value_and_action(
                next_remaining, alpha2, beta2, alpha3 + 1, beta3, horizon - 1
            )
            failure_future, _ = _optimal_value_and_action(
                next_remaining, alpha2, beta2, alpha3, beta3 + 1, horizon - 1
            )

        value = (
            p_resolve * (mass + success_future)
            + (1.0 - p_resolve) * failure_future
        )

        if (
            best_value is None
            or value > best_value
            or (value == best_value and (best_action is None or index < best_action))
        ):
            best_value = value
            best_action = index

    assert best_value is not None
    return best_value, best_action


def initial_policy_action() -> str:
    remaining = tuple(range(len(SOURCES)))
    _value, action = _optimal_value_and_action(
        remaining, *INITIAL_POSTERIOR, K
    )
    assert action is not None
    return SOURCES[action][0]


def all_reachable_terminal_sets() -> set[frozenset[str]]:
    """Enumerate the K-audit sets reachable under every binary audit outcome path."""

    terminal_sets: set[frozenset[str]] = set()

    def visit(
        remaining: tuple[int, ...],
        alpha2: int,
        beta2: int,
        alpha3: int,
        beta3: int,
        horizon: int,
        selected: tuple[str, ...],
    ) -> None:
        if horizon == 0:
            terminal_sets.add(frozenset(selected))
            return

        _value, action = _optimal_value_and_action(
            remaining, alpha2, beta2, alpha3, beta3, horizon
        )
        assert action is not None

        name, _mass, ambiguity_class = SOURCES[action]
        next_remaining = tuple(i for i in remaining if i != action)
        next_selected = selected + (name,)

        if ambiguity_class == 2:
            visit(
                next_remaining,
                alpha2 + 1,
                beta2,
                alpha3,
                beta3,
                horizon - 1,
                next_selected,
            )
            visit(
                next_remaining,
                alpha2,
                beta2 + 1,
                alpha3,
                beta3,
                horizon - 1,
                next_selected,
            )
        else:
            visit(
                next_remaining,
                alpha2,
                beta2,
                alpha3 + 1,
                beta3,
                horizon - 1,
                next_selected,
            )
            visit(
                next_remaining,
                alpha2,
                beta2,
                alpha3,
                beta3 + 1,
                horizon - 1,
                next_selected,
            )

    visit(
        tuple(range(len(SOURCES))),
        *INITIAL_POSTERIOR,
        K,
        (),
    )
    return terminal_sets


def preflight_summary() -> dict[str, object]:
    terminal_sets = all_reachable_terminal_sets()
    return {
        "k": K,
        "initial_action": initial_policy_action(),
        "reachable_terminal_set_count": len(terminal_sets),
        "reachable_terminal_sets": [sorted(items) for items in sorted(terminal_sets, key=lambda s: sorted(s))],
        "static_k5_set": sorted(STATIC_K5_SET),
        "outcome_invariant_set_identity": terminal_sets == {STATIC_K5_SET},
    }


if __name__ == "__main__":
    import json

    print(json.dumps(preflight_summary(), indent=2, sort_keys=True))
