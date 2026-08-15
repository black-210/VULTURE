import argparse


def parse_args():
    parser = argparse.ArgumentParser(prog="vulture", description="VULTURE CLI")
    parser.add_argument("--config", "-c", help="Path to config file", default=None)
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    return parser.parse_args()
