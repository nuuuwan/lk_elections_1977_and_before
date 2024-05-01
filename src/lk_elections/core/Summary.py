from dataclasses import dataclass

@dataclass
class Summary:
    electors: int
    polled: int
    rejected: int
    valid: int
    