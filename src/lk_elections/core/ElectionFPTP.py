import os
from dataclasses import dataclass

from utils import JSONFile, Log

from lk_elections.core.ResultFPTP import ResultFPTP
from lk_elections.core.Validatable import Validatable

log = Log('ElectionFPTP')


@dataclass
class ElectionFPTP(Validatable):
    date_str: str
    results: list[ResultFPTP]

    def year(self):
        return int(self.date_str.split('-')[0])

    def to_dict(self):
        return dict(
            date_str=self.date_str,
            results=[result.to_dict() for result in self.results],
        )

    def validate(self, context=None):
        context = context or {}
        errors = []
        exp_row_num = 1
        for result in self.results:
            errors += result.validate(context | dict(exp_row_num=exp_row_num))
            exp_row_num = result.row_num + 1
        return errors

    @property
    def data_path(self):
        return os.path.join(
            'parsed_data',
            f'general-election-{self.date_str}.json',
        )

    def save(self):
        errors = self.validate_and_log()
        JSONFile(self.data_path).write(self.to_dict() | dict(errors=errors))
        log.info(f'Saved {self.data_path}')
