"""Cybersecurity research helpers: log parsing and basic analytics."""
from typing import List


def parse_lines(lines: List[str]):
    return [l.strip() for l in lines if l.strip()]
