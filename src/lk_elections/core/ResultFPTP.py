from dataclasses import dataclass
from gig import Ent, EntType
from lk_elections.core.SingleResultFPTP import SingleResultFPTP
from lk_elections.core.Summary import Summary
from lk_elections.core.Validatable import Validatable


@dataclass
class ResultFPTP(Validatable):
    row_num: int
    electorate_name: str
    single_results: list[SingleResultFPTP]
    summary: Summary

    @property 
    def pd_id(self):
        search_key = self.electorate_name.replace('-', ' ').title()
        pd_list = Ent.list_from_name_fuzzy(search_key, EntType.PD, None, 1, 90 )
        if not pd_list:
            return '-'
        return pd_list[0].id
    
    @property
    def pd_id_short(self):
        return self.pd_id.split('-')[1]
    
    def to_dict(self):
        return dict(
            row_num=self.row_num,
            electorate_name=self.electorate_name,
            pd_id=self.pd_id,
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

        if self.pd_id == '-':
            errors.append(f"PD not found for {self.electorate_name}")

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
