"""Back-compat shim. Prefer silex.wedge."""

from silex.wedge import KITTING_STEPS as STEPS
from silex.wedge import build_kitting_cell


def build_demo_world():
    graph, ledger, runtime, issuer, _actor = build_kitting_cell()
    return graph, ledger, runtime, issuer
