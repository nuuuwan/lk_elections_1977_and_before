from dataclasses import dataclass

from lk_elections.core.Validatable import Validatable


@dataclass
class Summary(Validatable):
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

    def validate(self, context=None):
        context = context or {}
        errors = []
        if self.electors < self.polled:
            errors.append(
                '[electors < polled] ' + f"{self.electors} < {self.polled}"
            )

        if self.valid + self.rejected != self.polled:
            errors.append(
                '[valid + rejected != polled] '
                + f"{self.valid} + {self.rejected} != {self.polled}"
            )

        return errors

    @staticmethod
    def from_dict(summary_data):
        return Summary(
            electors=summary_data['electors'],
            polled=summary_data['polled'],
            rejected=summary_data['rejected'],
            valid=summary_data['valid'],
        )
