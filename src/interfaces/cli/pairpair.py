from typing import List

from src.domain.model.pair.pair import Members, Pairs
from src.registry.usecase import next_pairs_by_history, save_pairs_history


class PairPair:
    def save(self, *history: str) -> str:
        """e.g. pairpair.py save test1,test2 test3,test4 test5,"""

        pairs = Pairs.from_list([list(h) for h in history])
        save_pairs_history().run(pairs)
        return str(pairs)

    def next(self, *members) -> List[Pairs]:
        """e.g. pairpair.py next test1 test2 test3"""

        pairs_list = next_pairs_by_history().run(Members.from_list(list(members)))
        return pairs_list
