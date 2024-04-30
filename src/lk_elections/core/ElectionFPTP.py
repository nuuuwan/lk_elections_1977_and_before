import os
from dataclasses import dataclass
from lk_elections.core.ResultFPTP import ResultFPTP
from utils import JSONFile, Log

log = Log('ElectionFPTP')

@dataclass
class ElectionFPTP:
    date_str: str
    results: list[ResultFPTP]

    @property 
    def data(self):
        return {
            'date_str': self.date_str,
            'results': [result.__dict__ for result in self.results],
        }

    @property 
    def data_path(self):
        return os.path.join(
            'parsed_data',
            f'general-election-{self.date_str}.json',
        )

    def save(self):
        JSONFile(self.data_path).write(self.data)
        log.info(f'Saved {self.data_path}')
