from src.domain.model.pair.pair import (EvaluationService,
                                        PairsHistoryRepository)
from src.infrastructure.persistence.pair.inmemory import \
    InMemoryPairsHistoryRepository


def evaluation_service() -> EvaluationService:
    return EvaluationService()


def pairs_history_repository() -> PairsHistoryRepository:
    return InMemoryPairsHistoryRepository()
