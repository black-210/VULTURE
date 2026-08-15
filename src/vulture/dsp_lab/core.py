"""DSP Laboratory primitives: blocks and flow execution (placeholder).

Intended to be extended into a visual block editor and runtime.
"""
from typing import Callable, Any, Dict


class DSPBlock:
    def __init__(self, name: str, func: Callable[[Any], Any]):
        self.name = name
        self.func = func

    def run(self, input_data):
        return self.func(input_data)


class Flowgraph:
    def __init__(self):
        self.blocks = []

    def add_block(self, blk: DSPBlock):
        self.blocks.append(blk)

    def run(self, data):
        v = data
        for b in self.blocks:
            v = b.run(v)
        return v
