from dataclasses import dataclass

@dataclass
class SingleResultFPTP:
    candidate: str
    party_symbol: str
    votes: int