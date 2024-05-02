import camelot
from utils import Log

from lk_elections.core import ResultFPTP, SingleResultFPTP, Summary
from lk_elections.core.delimitation import Delimitation
from lk_elections.parsers.Parser import Parser
from utils_future import Int

log = Log('Parser1977')


class Parser1977(Parser):
    @property
    def result_rows_list(self):
        tables = camelot.read_pdf(
            self.pdf_path, pages='all', flavor='stream', edge_tol=1
        )
        result_rows_list = []
        current_result_rows = []
        for table in tables:
            table_aslist = table.df.values.tolist()
            for row in table_aslist:
                valid_cells = [cell for cell in row if cell != ""]

                first_token = valid_cells[0].split(' ')[0]
                if Int.isinstance(first_token):
                    result_rows_list.append(current_result_rows)
                    current_result_rows = []
                current_result_rows.append(valid_cells)
        result_rows_list.append(current_result_rows)
        result_rows_list = result_rows_list[1:]
        log.debug(f'Found {len(result_rows_list)} result rows')
        return result_rows_list

    @staticmethod
    def parse_result_first_row(first_row):
        # log.debug(f'parse_result_first_row: {first_row}')
        # Fix row_num-electorate_name merging issue
        if not Int.isinstance(first_row[0]):
            first_row_tokens = first_row[0].split(' ')
            first_row = [
                first_row_tokens[0],
                ' '.join(first_row_tokens[1:]),
            ] + first_row[1:]

        row_num, electorate_name = first_row[:2]
        row_num = Int.parse(row_num)

        polled, rejected, valid, electors = [
            Int.parse(x) for x in first_row[-4:]
        ]

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
        ]

    @staticmethod
    def parse_single_result(row):
        # log.debug(f'parse_single_result: {row}')
        if len(row) < 3:
            return None

        if len(row) == 3:
            tokens = row[0].split(' ')
            row = [' '.join(tokens[:-1]), tokens[-1]] + row[1:]

        candidate = row[0]
        party_symbol = Parser.clean(row[-3])

        if not Int.isinstance(row[-2]):
            return None
        votes = Int.parse(row[-2])

        return SingleResultFPTP(
            candidate,
            party_symbol,
            votes,
        )

    @staticmethod
    def parse_result(year, result_rows):
        # for i, row in enumerate(result_rows):
        #     log.debug(f'parse_result: {i}) {row}')

        [
            row_num,
            electorate_name,
            summary,
        ] = Parser1977.parse_result_first_row(result_rows[0])

        single_results = [
            single_result
            for single_result in [
                Parser1977.parse_single_result(row) for row in result_rows[1:]
            ]
            if single_result is not None
        ]

        pd_id_list = Delimitation.get_pd_id_list(year, electorate_name)

        result = ResultFPTP(
            row_num,
            electorate_name,
            pd_id_list,
            single_results,
            summary,
        )
        # log.debug(result)
        return result

    @property
    def results(self):
        return [
            Parser1977.parse_result(self.year, result_rows)
            for result_rows in self.result_rows_list
        ]
