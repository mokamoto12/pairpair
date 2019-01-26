from typing import List

from src.domain.model.pair.history import (EvaluationService, PairsHistory,
                                           PairsHistoryRepository)
from src.domain.model.pair.pair import Members, Pairs


class NextPairsByHistory:
    pairs_repository: PairsHistoryRepository
    evaluation_service: EvaluationService

    def __init__(self, pairs_repository: PairsHistoryRepository,
                 evaluation_service: EvaluationService) -> None:
        self.pairs_repository = pairs_repository
        self.evaluation_service = evaluation_service

    def run(self, members: Members) -> List[Pairs]:
        histories: List[PairsHistory] = self.pairs_repository.load()
        return self.evaluation_service.evaluate(
            [history.pairs for history in histories], members)


class SavePairsHistory:
    pairs_repository: PairsHistoryRepository

    def __init__(self, pairs_repository: PairsHistoryRepository):
        self.pairs_repository = pairs_repository

    def run(self, pairs: Pairs) -> None:
        history_id = self.pairs_repository.next_identity()
        pairs_history = PairsHistory(history_id, pairs)
        self.pairs_repository.save(pairs_history)
