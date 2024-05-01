import os
from dataclasses import dataclass

from utils import JSONFile, Log

from lk_elections.core.ResultFPTP import ResultFPTP

log = Log('ElectionFPTP')


@dataclass
class ElectionFPTP:
    date_str: str
    results: list[ResultFPTP]


    def to_dict(self):
        return dict(
            date_str=self.date_str,
            results=[result.to_dict() for result in self.results],
        )

    @property
    def data_path(self):
        return os.path.join(
            'parsed_data',
            f'general-election-{self.date_str}.json',
        )

    def save(self):
        JSONFile(self.data_path).write(self.to_dict())
        log.info(f'Saved {self.data_path}')
