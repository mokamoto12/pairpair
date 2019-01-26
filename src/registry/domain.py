from src.domain.model.pair.history import (EvaluationService,
                                           PairsHistoryRepository)
from src.infrastructure.persistence.pair.sqlite3 import \
    Sqlite3PairsHistoryRepository


def evaluation_service() -> EvaluationService:
    return EvaluationService()


def pairs_history_repository() -> PairsHistoryRepository:
    return Sqlite3PairsHistoryRepository()
    # return InMemoryPairsHistoryRepository()
