from functools import cached_property

from utils import File, Log

from lk_elections.core import ElectionFPTP

log = Log('ReadMe')


class ReadMe:
    @cached_property
    def elections(self):
        return ElectionFPTP.list_all()

    @staticmethod
    def get_lines_for_election_result(election):
        lines =[f'### {election.date_str}', '']
        table_lines = [
            '| # | Electorate | Party | Candidate | Votes |',
            '|---:|:---|:---|:---|---:|',
        ]
        for result in election.results:
            winning_single_result = result.single_results[0]
            table_lines.append(
                f'| {result.row_num} | {result.electorate_name} | {winning_single_result.party_symbol} | {winning_single_result.candidate} | {winning_single_result.votes} |'
            )
        table_lines.append('')
        return lines + table_lines

    @property
    def lines_elections_results(self):
        lines = ['## Elections Results', '']
        for election in self.elections:
            lines += ReadMe.get_lines_for_election_result(election)
        return lines

    @property
    def lines_election_summary_table(self):
        lines = ['## Elections', '']

        table_lines = [
            '| Election | n(Results) | Data |',
            '|:----|---:|:---|',
        ]
        for election in self.elections:
            table_lines.append(
                f'| {election.date_str} | {len(election.results)} | [{election.data_path_linux}]({election.data_path_linux}) |'
            )
        table_lines.append('')
        return lines + table_lines 

    @property
    def lines(self):
        return [
            '# Sri Lankan Elections (1977 and before)',
            '',
        ] + self.lines_election_summary_table + self.lines_elections_results

    @property
    def readme_path(self):
        return 'README.md'

    def write(self):
        File(self.readme_path).write_lines(self.lines)
        log.info(f'Wrote {self.readme_path}')
