from typing import List

from src.domain.model.pair.pair import (EvaluationService, Members, Pairs,
                                        PairsHistoryRepository)


class NextPairsByHistory:
    pairs_repository: PairsHistoryRepository
    evaluation_service: EvaluationService

    def __init__(self, pairs_repository: PairsHistoryRepository,
                 evaluation_service: EvaluationService) -> None:
        self.pairs_repository = pairs_repository
        self.evaluation_service = evaluation_service

    def run(self, members: Members) -> Pairs:
        history: List[Pairs] = self.pairs_repository.load()
        return self.evaluation_service.evaluate(history, members)


class SavePairsHistory:
    pairs_repository: PairsHistoryRepository

    def __init__(self, pairs_repository: PairsHistoryRepository):
        self.pairs_repository = pairs_repository

    def run(self, pairs: Pairs) -> None:
        self.pairs_repository.save(pairs)
