from dataclasses import dataclass


@dataclass
class ResultFPTP:
    row_num: int
    electorate_name: str
    party_to_candidate: dict[str, str]
    party_to_votes: dict[str, int]
    electors: int
    valid: int
    rejected: int
    polled: int
