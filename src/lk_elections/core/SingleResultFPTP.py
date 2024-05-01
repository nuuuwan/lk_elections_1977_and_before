from dataclasses import dataclass
from functools import cached_property

from lk_elections.core.Party import Party
from lk_elections.core.Validatable import Validatable


@dataclass
class SingleResultFPTP(Validatable):
    candidate: str
    party_symbol: str
    votes: int

    @cached_property
    def party_code(self):
        return Party.SYMBOL_TO_PARTY[self.party_symbol]
    
    @cached_property
    def party_emoji(self):
        return Party.PARTY_TO_EMOJI.get(self.party_code, '')
    
    @cached_property
    def party_emoji_and_code(self):
        return f"{self.party_emoji} {self.party_code}"

    def to_dict(self):
        return dict(
            candidate=self.candidate,
            party_code=self.party_code,
            party_symbol=self.party_symbol,
            votes=self.votes,
        )

    def validate(self, context=None):
        MIN_VOTES = 10
        errors = []
        if self.votes <= MIN_VOTES:
            errors.append(f"votes {self.votes} <= 0")

        if self.party_symbol not in Party.SYMBOL_TO_PARTY:
            errors.append(f"unknown party_symbol {self.party_symbol}")

        MIN_NAME_LEN = 5
        if len(self.candidate) < MIN_NAME_LEN:
            errors.append(f"candidate name too short: {self.candidate}")

        return errors

    @staticmethod
    def from_dict(single_result_data):
        return SingleResultFPTP(
            candidate=single_result_data['candidate'],
            party_symbol=single_result_data['party_symbol'],
            votes=single_result_data['votes'],
        )
