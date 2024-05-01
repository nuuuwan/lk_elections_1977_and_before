from dataclasses import dataclass


@dataclass
class SingleResultFPTP:
    candidate: str
    party_symbol: str
    votes: int

    def to_dict(self):
        return dict(
            candidate=self.candidate,
            party_symbol=self.party_symbol,
            votes=self.votes,
        )