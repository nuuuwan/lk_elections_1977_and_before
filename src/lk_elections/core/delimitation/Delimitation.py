from dataclasses import dataclass

from lk_elections.core.delimitation.DELIMITATION_1946 import DELIMITATION_1946
from lk_elections.core.delimitation.DELIMITATION_1959 import DELIMITATION_1959
from lk_elections.core.delimitation.DELIMITATION_1976 import DELIMITATION_1976


@dataclass
class Delimitation:
    id: str
    name_to_pd_list: dict[str, list[str]]

    @staticmethod
    def idx():
        return {
            1946: Delimitation('1946', DELIMITATION_1946),
            1959: Delimitation('1959', DELIMITATION_1959),
            1976: Delimitation('1976', DELIMITATION_1976),
        }

    @staticmethod
    def get_delim_id_for_year(year):
        return {
            1947: 1946,
            1952: 1946,
            1956: 1946,
            1960: 1959,
            1965: 1959,
            1970: 1959,
            1977: 1976,
        }.get(year)

    @staticmethod
    def from_year(year):
        return Delimitation.idx()[Delimitation.get_delim_id_for_year(year)]

    @staticmethod
    def get_pd_id_list(year, electorate_name):
        search_key = electorate_name
        return Delimitation.from_year(year).name_to_pd_list.get(
            search_key, []
        )
