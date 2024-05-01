from dataclasses import dataclass

from lk_elections.core.Validatable import Validatable


@dataclass
class SingleResultFPTP(Validatable):
    candidate: str
    party_symbol: str
    votes: int

    KNOWN_PARTY_SYMBOLS = [
        'Aeroplane',
        'Bell',
        'Bicycle',
        'Bird',
        'Book',
        'Bus',
        'Butterfly',
        'Cart Wheel',
        'Chair',
        'Clock',
        'Cockerel',
        'Cup',
        'Elephant',
        'Eye',
        'Flower',
        'Hand',
        'House',
        'Key',
        'Key',
        'Ladder',
        'Lamp',
        'Mortar',
        'Omnibus',
        'Orange',
        'Pair Of Scales',
        'Pair Of Spectacles',
        'Pineapple',
        'Pot',
        'Rabbit',
        'Radio',
        'Saw',
        'Sewing Machine',
        'Ship',
        'Spoon',
        'Star',
        'Sun',
        'Table',
        'Tree',
        'Tumbler',
        'Umbrella',
        'Wheel',
        'Window',
        'Uncontested',
    ]

    def to_dict(self):
        return dict(
            candidate=self.candidate,
            party_symbol=self.party_symbol,
            votes=self.votes,
        )

    def validate(self, context=None):
        MIN_VOTES = 10
        errors = []
        if self.votes <= MIN_VOTES:
            errors.append(f"votes {self.votes} <= 0")

        if self.party_symbol not in SingleResultFPTP.KNOWN_PARTY_SYMBOLS:
            # errors.append(f"unknown party_symbol {self.party_symbol}")
            print(self.party_symbol)

        MIN_NAME_LEN = 5
        if len(self.candidate) < MIN_NAME_LEN:
            errors.append(f"c: {self.candidate}")

        return errors
