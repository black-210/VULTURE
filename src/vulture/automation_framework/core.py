"""Automation framework: workflow engine placeholder."""
from typing import Callable, List


class WorkflowEngine:
    def __init__(self):
        self.tasks: List[Callable] = []

    def add_task(self, fn: Callable):
        self.tasks.append(fn)

    def run(self):
        results = []
        for t in self.tasks:
            results.append(t())
        return results
