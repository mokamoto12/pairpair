from unittest import TestCase

from src.application.usecase.pair.pair import (NextPairsByHistory,
                                               SavePairsHistory)
from src.domain.model.pair.pair import (EvaluationService, Member, Members,
                                        Pair, Pairs)
from src.infrastructure.persistence.pair.inmemory import \
    InMemoryPairsHistoryRepository


class NextPairsByHistoryTest(TestCase):
    def setUp(self):
        self.repository = InMemoryPairsHistoryRepository()
        self.use_case = NextPairsByHistory(self.repository,
                                           EvaluationService())

    def test_run(self):
        pairs_list = self.use_case.run(
            Members([Member('a'), Member('b'),
                     Member('c')]))
        self.assertEqual(pairs_list, [
            Pairs([Pair(Member('a'), Member('b')),
                   Pair(Member('c'), None)]),
            Pairs([Pair(Member('a'), Member('c')),
                   Pair(Member('b'), None)]),
            Pairs([Pair(Member('b'), Member('c')),
                   Pair(Member('a'), None)])
        ])


class SavePairsHistoryTest(TestCase):
    def setUp(self):
        self.repository = InMemoryPairsHistoryRepository()
        self.use_case = SavePairsHistory(self.repository)

    def test_run(self):
        save_pairs = Pairs(
            [Pair(Member('a'), Member('b')),
             Pair(Member('c'), None)])
        self.use_case.run(save_pairs)

        self.assertEqual(self.repository.list, [save_pairs])
