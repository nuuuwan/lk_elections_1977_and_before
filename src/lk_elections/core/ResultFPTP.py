from dataclasses import dataclass

from lk_elections.core.SingleResultFPTP import SingleResultFPTP
from lk_elections.core.Summary import Summary


@dataclass
class ResultFPTP:
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
