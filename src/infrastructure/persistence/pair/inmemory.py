from typing import List

from src.domain.model.pair.pair import Pairs, PairsHistoryRepository


class InMemoryPairsHistoryRepository(PairsHistoryRepository):
    list: List[Pairs]

    def __init__(self) -> None:
        self.list = []

    def load(self) -> List[Pairs]:
        return self.list

    def save(self, pairs: Pairs) -> None:
        self.list.append(pairs)

    def flush(self) -> None:
        self.list = []
