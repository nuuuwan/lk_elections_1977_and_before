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

    DIR_PARSE_DATA = os.path.join('data', 'parsed_data')

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
            ElectionFPTP.DIR_PARSE_DATA,
            f'general-election-{self.date_str}.json',
        )

    @property
    def data_path_linux(self):
        return self.data_path.replace('\\', '/')

    def save(self):
        errors = self.validate_and_log()
        JSONFile(self.data_path).write(self.to_dict() | dict(errors=errors))
        log.info(f'Saved {self.data_path}')

    @staticmethod
    def from_dict(election_data):
        return ElectionFPTP(
            date_str=election_data['date_str'],
            results=[
                ResultFPTP.from_dict(result_data)
                for result_data in election_data['results']
            ],
        )

    @staticmethod
    def load_from_file(data_path):
        election_data = JSONFile(data_path).read()
        return ElectionFPTP.from_dict(election_data)

    @staticmethod
    def list_all():
        election_list = []
        for file_name in os.listdir(ElectionFPTP.DIR_PARSE_DATA):
            if file_name.endswith('.json'):
                election = ElectionFPTP.load_from_file(
                    os.path.join(ElectionFPTP.DIR_PARSE_DATA, file_name)
                )
                election_list.append(election)
        log.info(f'Loaded {len(election_list)} elections')
        return election_list
