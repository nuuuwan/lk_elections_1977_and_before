from dataclasses import dataclass


from lk_elections.core.SingleResultFPTP import SingleResultFPTP
from lk_elections.core.Summary import Summary
from lk_elections.core.Validatable import Validatable
from lk_elections.core.delimitation import Delimitation


@dataclass
class ResultFPTP(Validatable):
    row_num: int
    electorate_name: str
    pd_id_list: list[str]
    single_results: list[SingleResultFPTP]
    summary: Summary

    @property 
    def pds_short(self):
        short_pd_id_list = []
        for pd_id in self.pd_id_list:
            short_pd_id = pd_id[-1:] if short_pd_id_list else pd_id[-3:]
            short_pd_id_list.append(short_pd_id)
        return ','.join(short_pd_id_list)
    
    def to_dict(self, election):
        return dict(
            row_num=self.row_num,
            electorate_name=self.electorate_name,
            pd_id_list=self.pd_id_list,
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

        if self.pd_id_list == []:
            errors.append(f"PD not found for {self.electorate_name}")
            print(f"'{self.electorate_name}': '{self.electorate_name}',")

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
            pd_id_list=result_data['pd_id_list'],
            single_results=[
                SingleResultFPTP.from_dict(single_result_data)
                for single_result_data in result_data['single_results']
            ],
            summary=Summary.from_dict(result_data['summary']),
        )
