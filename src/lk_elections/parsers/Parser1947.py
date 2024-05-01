import os

import camelot
from utils import Log

from lk_elections.core import ElectionFPTP, ResultFPTP

log = Log('Parser1947')


def parse_int(x):
    x = str(x)
    if x == '-':
        return 0
    if x == '':
        return 0
    x = x.replace(',', '')
    return int(x)


def isnumeric(x):
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
                if (
                    row[0].startswith("No")
                    or row[1].startswith("No")
                    or row[0].startswith("of ")
                    or row[3].startswith("Polled")
                ):
                    continue
                if row[0] != "" or (
                    row[0] == ""
                    and row[1] != ""
                    and isnumeric(row[1].split(" ")[0])
                ):
                    result_rows_list.append(current_result_rows)
                    current_result_rows = []
                current_result_rows.append(row)
        result_rows_list.append(current_result_rows)
        result_rows_list = result_rows_list[1:]
        log.debug(f'Found {len(result_rows_list)} result rows')
        return result_rows_list

    @staticmethod
    def parse_result_first_row(first_row):
        row_num, electorate_name = first_row[:2]

        if row_num == "":
            tokens = electorate_name.split(" ")
            row_num = tokens[0]
            electorate_name = " ".join(tokens[1:])
        elif not isnumeric(row_num):
            tokens = row_num.split(" ")
            row_num = tokens[0]
            electorate_name = " ".join(tokens[1:])

        if len(first_row) == 8:
            rejected, polled, electors = [
                parse_int(x) for x in first_row[5:8]
            ]
        else:
            rejected, polled, electors = [
                parse_int(x) for x in first_row[4:7]
            ]

        return [
            row_num,
            electorate_name,
            electors,
            rejected,
            polled,
        ]

    @staticmethod
    def parse_result(result_rows):
        for row in result_rows:
            print(row)

        [
            row_num,
            electorate_name,
            electors,
            rejected,
            polled,
        ] = Parser1947.parse_result_first_row(result_rows[0])

        party_to_candidate = {}
        party_to_votes = {}
        for row in result_rows:
            if row[2] == "":
                continue
            if len(result_rows[0]) == 8:
                candidate, party, votes = row[2:5]
            else:
                candidate, party, votes = row[1:4]

            party_to_candidate[party] = candidate

            if votes == "":
                continue

            party_to_votes[party] = parse_int(votes)

        valid = sum(party_to_votes.values())

        result = ResultFPTP(
            row_num,
            electorate_name,
            party_to_candidate,
            party_to_votes,
            electors,
            valid,
            rejected,
            polled,
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
