#!/usr/bin/env python3
"""Check local dependencies for the single-stock multi-agent analysis skill."""

from __future__ import annotations

import importlib.util
import platform
import sys


REQUIRED = ["akshare", "pandas", "numpy", "matplotlib"]

RUNTIME_CAPABILITIES = [
    (
        "Current web/source access",
        "Required for fresh prices, filings, announcements, and news.",
    ),
    (
        "Dedicated finance/quote tool",
        "Recommended for quote verification when exposed by the host.",
    ),
    (
        "Multi-agent/subagent tools",
        "Required for true parallel agent tracks; otherwise use labeled sequential memos.",
    ),
    (
        "Browser or Chrome plugin",
        "Optional for authenticated or visual page workflows.",
    ),
    (
        "Automation/reminder tool",
        "Optional for recurring monitors and follow-up checks.",
    ),
    (
        "Skill installer",
        "Optional for installing this skill or companion output skills from GitHub.",
    ),
]


def main() -> int:
    print(f"python: {sys.executable}")
    print(f"version: {platform.python_version()}")

    missing: list[str] = []
    for module_name in REQUIRED:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            print(f"{module_name}: MISSING")
            missing.append(module_name)
            continue

        module = __import__(module_name)
        version = getattr(module, "__version__", "unknown")
        print(f"{module_name}: OK ({version})")

    if missing:
        print("\nInstall missing packages with:")
        print(f"{sys.executable} -m pip install {' '.join(missing)}")
        return 1

    print("\nCodex runtime capabilities to verify in the current turn:")
    for name, purpose in RUNTIME_CAPABILITIES:
        print(f"- {name}: {purpose}")
    print("Note: this Python checker cannot inspect Codex plugin/tool exposure.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
