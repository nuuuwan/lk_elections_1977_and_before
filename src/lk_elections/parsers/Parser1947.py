import os

import camelot
from utils import Log

from lk_elections.core import (ElectionFPTP, ResultFPTP, SingleResultFPTP,
                               Summary)

log = Log('Parser1947')


def parse_int(x):
    x = str(x)
    if x == '-':
        return 0
    if x == '':
        return 0
    x = x.replace(',', '')
    return int(x)


def is_int(x):
    try:
        parse_int(x)
        return True
    except BaseException:
        return False


class Parser1947:
    def __init__(self, id):
        self.id = id

    @property
    def pdf_path(self):
        return os.path.join(
            'original_pdfs',
            f'general-election-{self.id}.pdf',
        )

    @property
    def result_rows_list(self):
        tables = camelot.read_pdf(self.pdf_path, pages='all', flavor='stream')
        result_rows_list = []
        current_result_rows = []
        for table in tables:
            table_aslist = table.df.values.tolist()
            for row in table_aslist:
                valid_cells = [cell for cell in row if cell != ""]
                first_token = valid_cells[0].split(' ')[0]
                if is_int(first_token):
                    result_rows_list.append(current_result_rows)
                    current_result_rows = []
                current_result_rows.append(valid_cells)
        result_rows_list.append(current_result_rows)
        result_rows_list = result_rows_list[1:]
        log.debug(f'Found {len(result_rows_list)} result rows')
        return result_rows_list

    @staticmethod
    def parse_result_first_row(first_row):

        # Fix row_num-electorate_name merging issue 
        if not is_int(first_row[0]):        
            first_row_tokens = first_row[0].split(' ')
            first_row = [first_row_tokens[0], ' '.join(first_row_tokens[1:])] + first_row[1:]

        row_num, electorate_name = first_row[:2]
        rejected, polled, electors = [parse_int(x) for x in first_row[-3:]]
        first_single_result = Parser1947.parse_single_result(first_row[2:-3])

        summary = Summary(
            electors=electors,
            polled=polled,
            rejected=rejected,
            valid=polled - rejected,
        )

        return [
            row_num,
            electorate_name,
            summary,
            first_single_result,
        ]

    @staticmethod
    def parse_single_result(row):
        log.debug(f'parse_single_result: {row}')

        candidate = " ".join(row[:-2])
        party_symbol = row[-2]

        if not is_int(row[-1]):
            return None
        votes = parse_int(row[-1])

        return SingleResultFPTP(
            candidate,
            party_symbol,
            votes,
        )

    @staticmethod
    def parse_result(result_rows):
        for i, row in enumerate(result_rows):
            log.debug(f'parse_result: {i}) {row}')

        [
            row_num,
            electorate_name,
            summary,
            first_single_result,
        ] = Parser1947.parse_result_first_row(result_rows[0])

        single_results = [first_single_result] + [
            single_result
            for single_result in  [
            Parser1947.parse_single_result(row) for row in result_rows[1:]
            ] if single_result is not None
        ]

        result = ResultFPTP(
            row_num,
            electorate_name,
            single_results,
            summary,
        )
        log.debug(result)
        return result

    def parse(self):
        log.info(f'Parsing {self.id}...')
        results = [
            Parser1947.parse_result(result_rows)
            for result_rows in self.result_rows_list
        ]

        election = ElectionFPTP(
            date_str=self.id,
            results=results,
        )
        election.save()
