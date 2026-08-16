import json
import os

from radon.complexity import cc_visit


CONFIG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config"
)

SEVERITY_MAP_PATH = os.path.join(CONFIG_DIR, "radon_severity_map.json")
RANK_THRESHOLDS_PATH = os.path.join(CONFIG_DIR, "complexity_rank_thresholds.json")

_severity_map = None
_rank_thresholds = None


def _load_severity_map():

    global _severity_map

    if _severity_map is None:

        with open(SEVERITY_MAP_PATH, "r", encoding="utf-8") as f:
            _severity_map = json.load(f)

    return _severity_map


def _load_rank_thresholds():

    global _rank_thresholds

    if _rank_thresholds is None:

        with open(RANK_THRESHOLDS_PATH, "r", encoding="utf-8") as f:
            _rank_thresholds = json.load(f)

    return _rank_thresholds


def _rank_for_complexity(complexity: int) -> str:
    """
    Computes the A-F complexity rank directly from the numeric
    complexity, using config/complexity_rank_thresholds.json,
    instead of trusting Radon's own `block.letter` attribute -
    which has been observed to return inconsistent values in some
    Radon versions/environments (e.g. reporting 'F' for a
    complexity of 1, which contradicts Radon's own documented
    thresholds). This keeps the mapping deterministic and
    editable, independent of that library quirk.
    """

    for band in _load_rank_thresholds():

        if complexity <= band["max_complexity"]:
            return band["rank"]

    return "F"


class RadonRunner:
    """
    Executes Radon to calculate Cyclomatic Complexity.
    No complexity rules are implemented manually.
    """

    def __init__(self):
        pass

    def run(self, code):

        findings = []

        try:

            results = cc_visit(code)

            for block in results:

                rank = _rank_for_complexity(block.complexity)

                severity = _load_severity_map().get(
                    rank,
                    "LOW"
                )

                findings.append(
                    {
                        "agent": "Code Analysis Agent",
                        "tool": "Radon",
                        "name": block.name,
                        "type": block.__class__.__name__,
                        "complexity": block.complexity,
                        "rank": rank,
                        "severity": severity,
                        "line": block.lineno,
                        "end_line": block.endline,
                    }
                )

        except Exception as e:

            findings.append(
                {
                    "agent": "Code Analysis Agent",
                    "tool": "Radon",
                    "error": str(e)
                }
            )

        return findings