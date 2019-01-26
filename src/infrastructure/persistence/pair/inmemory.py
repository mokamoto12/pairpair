from typing import List

from src.domain.model.pair.history import (PairsHistory, PairsHistoryId,
                                           PairsHistoryRepository)


class InMemoryPairsHistoryRepository(PairsHistoryRepository):
    cnt: int
    list: List[PairsHistory]

    def __init__(self) -> None:
        self.cnt = 0
        self.list = []

    def next_identity(self) -> PairsHistoryId:
        identity = PairsHistoryId(str(self.cnt))
        self.cnt += 1
        return identity

    def load(self) -> List[PairsHistory]:
        return self.list

    def save(self, pairs_history: PairsHistory) -> None:
        self.list.append(pairs_history)

    def flush(self) -> None:
        self.list = []
