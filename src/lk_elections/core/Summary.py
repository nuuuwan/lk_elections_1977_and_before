from dataclasses import dataclass


@dataclass
class Summary:
    electors: int
    polled: int
    rejected: int
    valid: int

    def to_dict(self):
        return dict(
            electors=self.electors,
            polled=self.polled,
            rejected=self.rejected,
            valid=self.valid,
        )
