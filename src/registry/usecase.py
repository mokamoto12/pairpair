from src.application.usecase.pair.pair import (NextPairsByHistory,
                                               SavePairsHistory)
from src.registry.domain import evaluation_service, pairs_history_repository


def next_pairs_by_history() -> NextPairsByHistory:
    return NextPairsByHistory(pairs_history_repository(), evaluation_service())


def save_pairs_history() -> SavePairsHistory:
    return SavePairsHistory(pairs_history_repository())
