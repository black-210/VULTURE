from dataclasses import dataclass


@dataclass
class Result:
    success: bool
    message: str = ""
