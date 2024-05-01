from dataclasses import dataclass

from lk_elections.core.SingleResultFPTP import SingleResultFPTP
from lk_elections.core.Summary import Summary
from lk_elections.core.Validatable import Validatable


@dataclass
class ResultFPTP(Validatable):
    row_num: int
    electorate_name: str
    single_results: list[SingleResultFPTP]
    summary: Summary

    def to_dict(self):
        return dict(
            row_num=self.row_num,
            electorate_name=self.electorate_name,
            single_results=[
                single_result.to_dict()
                for single_result in self.single_results
            ],
            summary=self.summary.to_dict(),
        )

    def validate(self, context=None):
        context = context or {}
        errors = []

        exp_row_num = context.get('exp_row_num', None)
        if self.row_num != exp_row_num:
            errors.append(f"row_num {exp_row_num} missing")

        for single_result in self.single_results:
            errors += single_result.validate()
        errors += self.summary.validate()

        exp_valid = sum(
            single_result.votes for single_result in self.single_results
        )
        if self.summary.valid != exp_valid:
            errors.append(
                '[summary.valid != results-valid] '
                + f"{self.summary.valid} != {exp_valid}"
            )

        return errors

    @staticmethod
    def from_dict(result_data):
        return ResultFPTP(
            row_num=result_data['row_num'],
            electorate_name=result_data['electorate_name'],
            single_results=[
                SingleResultFPTP.from_dict(single_result_data)
                for single_result_data in result_data['single_results']
            ],
            summary=Summary.from_dict(result_data['summary']),
        )
