from dataclasses import dataclass

from lk_elections.core.Validatable import Validatable


@dataclass
class SingleResultFPTP(Validatable):
    candidate: str
    party_symbol: str
    votes: int

    KNOWN_PARTY_SYMBOLS = [
        'Aeroplane',
        'Bicycle',
        'Bird',
        'Bus',
        'Butterfly',
        'Cart Wheel',
        'Chair',
        'Clock',
        'Cup',
        'Elephant',
        'Eye',
        'Flower',
        'Hand',
        'House',
        'Key',
        'Lamp',
        'Omnibus',
        'Pair Of Scales',
        'Pair Of Spectacles',
        'Pineapple',
        'Spoon',
        'Star',
        'Tree',
        'Umbrella',
        'Wheel',



'Ladder',
'Ship',
'Table',
'Pot',
'Cockerel',
'Tumbler',
'Window',
'Sewing Machine',
'Bell',
'Orange',
'Book',
'Sun',

'Key',
'Mortar',
'Rabbit',
'Radio Set',
'Saw',

        
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

        return errors
