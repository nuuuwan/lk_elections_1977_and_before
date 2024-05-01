from dataclasses import dataclass
from lk_elections.core.SingleResultFPTP import SingleResultFPTP
from lk_elections.core.Summary import Summary

@dataclass
class ResultFPTP:
    row_num: int
    electorate_name: str
    single_results: list[SingleResultFPTP]
    summary: Summary
