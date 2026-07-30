#!/usr/bin/env python3
"""ClipRelay prototype entry point.

Usage:
    python main.py --config config.json

Everything runs locally: it tails a text log file and polls the system
clipboard. Nothing is sent over the network, and nothing is typed into any
real terminal yet - this prototype only logs what it *would* send.
"""
from __future__ import annotations

import argparse

from cliprelay.config import load_config
from cliprelay.watcher import ClipRelayWatcher


def main() -> None:
    parser = argparse.ArgumentParser(description="ClipRelay prototype watcher")
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to a JSON config file (optional, defaults are used for any missing field)",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    watcher = ClipRelayWatcher(config)
    try:
        watcher.run_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
