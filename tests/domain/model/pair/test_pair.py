from unittest import TestCase

from src.domain.model.pair.history import EvaluationService
from src.domain.model.pair.pair import Member, Members, Pair, Pairs, PairTree


class PairTest(TestCase):
    def setUp(self):
        self.m1 = Member('a')
        self.m2 = Member('b')

    def test_equals(self):
        self.assertEqual(Pair(self.m1, self.m2), Pair(self.m1, self.m2))

    def test_equals2(self):
        self.assertEqual(Pair(self.m2, self.m1), Pair(self.m1, self.m2))

    def test_equals3(self):
        self.assertEqual(Pair(self.m2, None), Pair(self.m2, None))


class PairsTest(TestCase):
    def setUp(self):
        self.pairs = Pairs(
            [Pair(Member('a'), Member('b')),
             Pair(Member('c'), None)])

        self.one_pairs = Pairs([Pair(Member('a'), Member('b'))])

        self.empty_pairs = Pairs([])

    def test_getitem__pairs(self):
        self.assertEqual(self.pairs[1], Pair(Member('c'), None))

    def test_tail__pairs(self):
        self.assertEqual(self.pairs.tail(), Pairs([Pair(Member('c'), None)]))

    def test_tail__one_pairs(self):
        self.assertEqual(self.one_pairs.tail(), Pairs([]))

    def test_tail__empty_pairs(self):
        self.assertEqual(self.one_pairs.tail(), Pairs([]))

    def test_in__pairs(self):
        self.assertTrue(Pair(Member('c'), None) in self.pairs)

    def test_have_same__pairs(self):
        self.assertTrue(
            self.pairs.have_same(
                Pairs(
                    [Pair(Member('x'), Member('y')),
                     Pair(Member('c'), None)])))

    def test_have_same__pairs2(self):
        self.assertTrue(not self.pairs.have_same(
            Pairs([Pair(Member('x'), Member('y')),
                   Pair(Member('z'), None)])))


class PairTreeTest(TestCase):
    def test_fold(self):
        tree = PairTree(
            Pair(Member('a'), Member('b')),
            [PairTree(Pair(Member('c'), None), [])])
        self.assertEqual(
            [Pairs([Pair(Member('a'), Member('b')),
                    Pair(Member('c'), None)])], tree.fold())

    def test_fold2(self):
        tree = PairTree(
            Pair(Member('a'), Member('b')), [
                PairTree(
                    Pair(Member('c'), Member('d')),
                    [PairTree(Pair(Member('e'), None), [])]),
                PairTree(
                    Pair(Member('c'), Member('e')),
                    [PairTree(Pair(Member('d'), None), [])])
            ])
        self.assertEqual([
            Pairs([
                Pair(Member('a'), Member('b')),
                Pair(Member('c'), Member('d')),
                Pair(Member('e'), None)
            ]),
            Pairs([
                Pair(Member('a'), Member('b')),
                Pair(Member('c'), Member('e')),
                Pair(Member('d'), None)
            ])
        ], tree.fold())


class MembersTest(TestCase):
    def setUp(self):
        self.members = Members([Member('a'), Member('b'), Member('c')])
        self.single_members = Members([Member('a')])

    def test_select_first_pairs(self):
        self.assertEqual(
            self.members.select_first_pairs(),
            [(Pair(Member('a'), Member('b')), Members([Member('c')])),
             (Pair(Member('a'), Member('c')), Members([Member('b')])),
             (Pair(Member('b'), Member('c')), Members([Member('a')]))])

    def test_select_first_pairs_with_single_members(self):
        self.assertEqual(self.single_members.select_first_pairs(),
                         [(Pair(Member('a'), None), Members([]))])

    def test_combinations(self):
        self.assertEqual(self.members.combinations(), [
            PairTree(
                Pair(Member('a'), Member('b')),
                [PairTree(Pair(Member('c'), None), [])]),
            PairTree(
                Pair(Member('a'), Member('c')),
                [PairTree(Pair(Member('b'), None), [])]),
            PairTree(
                Pair(Member('b'), Member('c')),
                [PairTree(Pair(Member('a'), None), [])])
        ])

    def test_possible_pair(self):
        pass
        # self.assertEqual(
        #     list(self.members.possible_pair()),
        #     [[Pair(Member('a'), Member('b')),
        #       Pair(Member('c'), None)],
        #      [Pair(Member('a'), Member('c')),
        #       Pair(Member('b'), None)],
        #      [Pair(Member('b'), Member('c')),
        #       Pair(Member('a'), None)]])


class EvaluationServiceTest(TestCase):
    def setUp(self):
        self.last_pairs3 = Pairs(
            [Pair(Member('a'), Member('b')),
             Pair(Member('c'), None)])
        self.members3 = Members([Member('a'), Member('b'), Member('c')])

        self.last_pairs5 = Pairs([
            Pair(Member('a'), Member('b')),
            Pair(Member('c'), Member('d')),
            Pair(Member('e'), None)
        ])
        self.members5 = Members(
            [Member('a'),
             Member('b'),
             Member('c'),
             Member('d'),
             Member('e')])

    def test_filter(self):
        tree = self.members3.combinations()
        filtered_tree = EvaluationService(
        ).pair_must_have_only_either_member_of_last_pair(
            self.last_pairs3, tree)
        self.assertEqual(filtered_tree, [
            PairTree(
                Pair(Member('a'), Member('c')),
                [PairTree(Pair(Member('b'), None), [])]),
            PairTree(
                Pair(Member('b'), Member('c')),
                [PairTree(Pair(Member('a'), None), [])])
        ])

    def test_filter2(self):
        tree = self.members5.combinations()
        filtered_tree = EvaluationService(
        ).pair_must_have_only_either_member_of_last_pair(
            self.last_pairs5, tree)
        self.assertEqual(filtered_tree, [
            PairTree(
                Pair(Member('a'), Member('c')), [
                    PairTree(
                        Pair(Member('d'), Member('e')),
                        [PairTree(Pair(Member('b'), None), [])])
                ]),
            PairTree(
                Pair(Member('a'), Member('d')), [
                    PairTree(
                        Pair(Member('c'), Member('e')),
                        [PairTree(Pair(Member('b'), None), [])])
                ]),
            PairTree(
                Pair(Member('a'), Member('e')), [
                    PairTree(
                        Pair(Member('b'), Member('c')),
                        [PairTree(Pair(Member('d'), None), [])]),
                    PairTree(
                        Pair(Member('b'), Member('d')),
                        [PairTree(Pair(Member('c'), None), [])])
                ]),
            PairTree(
                Pair(Member('b'), Member('c')), [
                    PairTree(
                        Pair(Member('d'), Member('e')),
                        [PairTree(Pair(Member('a'), None), [])])
                ]),
            PairTree(
                Pair(Member('b'), Member('d')), [
                    PairTree(
                        Pair(Member('c'), Member('e')),
                        [PairTree(Pair(Member('a'), None), [])])
                ]),
            PairTree(
                Pair(Member('b'), Member('e')), [
                    PairTree(
                        Pair(Member('a'), Member('c')),
                        [PairTree(Pair(Member('d'), None), [])]),
                    PairTree(
                        Pair(Member('a'), Member('d')),
                        [PairTree(Pair(Member('c'), None), [])])
                ])
        ])

    def test_filter_and_empty(self):
        members = Members([Member('a'), Member('b')])
        tree = members.combinations()
        filtered = EvaluationService(
        ).pair_must_have_only_either_member_of_last_pair(
            Pairs([Pair(Member('a'), Member('b'))]), tree)
        self.assertEqual(filtered, [])

    def test_position_filter(self):
        history = [
            Pairs([Pair(Member('a'), Member('b')),
                   Pair(Member('c'), None)]),
            Pairs([Pair(Member('a'), Member('c')),
                   Pair(Member('b'), None)])
        ]
        tree = self.members3.combinations()
        possible_pairs = PairTree.possible_pairs(tree)
        filtered_tree = EvaluationService(
        ).member_is_must_not_in_same_position_at_three_times(
            history, possible_pairs)
        self.assertEqual(
            filtered_tree,
            [Pairs([Pair(Member('b'), Member('c')),
                    Pair(Member('a'), None)])])

    def test_filter_same_pair(self):
        history = [
            Pairs([Pair(Member('a'), Member('b')),
                   Pair(Member('c'), None)])
        ]
        pairs = PairTree.possible_pairs(self.members3.combinations())
        filtered_pairs = EvaluationService(
        ).pair_should_not_exist_same_pair_in_near_history(history, pairs)
        self.assertEqual(filtered_pairs, [
            Pairs([Pair(Member('a'), Member('c')),
                   Pair(Member('b'), None)]),
            Pairs([Pair(Member('b'), Member('c')),
                   Pair(Member('a'), None)])
        ])

    def test_filter_same_pair2(self):
        history = [
            Pairs([Pair(Member('a'), Member('b')),
                   Pair(Member('c'), None)]),
            Pairs([Pair(Member('a'), Member('c')),
                   Pair(Member('b'), None)])
        ]
        pairs = PairTree.possible_pairs(self.members3.combinations())
        filtered_pairs = EvaluationService(
        ).pair_should_not_exist_same_pair_in_near_history(history, pairs)
        self.assertEqual(
            filtered_pairs,
            [Pairs([Pair(Member('b'), Member('c')),
                    Pair(Member('a'), None)])])

    def test_filter_same_pair3(self):
        history = [
            Pairs([
                Pair(Member('a'), Member('c')),
                Pair(Member('d'), Member('e')),
                Pair(Member('b'), None)
            ]),
            Pairs([
                Pair(Member('a'), Member('b')),
                Pair(Member('c'), Member('d')),
                Pair(Member('e'), None)
            ])
        ]
        tree = self.members5.combinations()
        s = EvaluationService()
        filtered_pairs = s.pair_should_not_exist_same_pair_in_near_history(
            history,
            PairTree.possible_pairs(
                s.pair_must_have_only_either_member_of_last_pair(
                    history[-1], tree)))
        self.assertEqual(filtered_pairs, [
            Pairs([
                Pair(Member('a'), Member('e')),
                Pair(Member('b'), Member('c')),
                Pair(Member('d'), None)
            ]),
            Pairs([
                Pair(Member('a'), Member('e')),
                Pair(Member('b'), Member('d')),
                Pair(Member('c'), None)
            ]),
            Pairs([
                Pair(Member('b'), Member('d')),
                Pair(Member('c'), Member('e')),
                Pair(Member('a'), None)
            ]),
            Pairs([
                Pair(Member('b'), Member('e')),
                Pair(Member('a'), Member('c')),
                Pair(Member('d'), None)
            ]),
            Pairs([
                Pair(Member('b'), Member('e')),
                Pair(Member('a'), Member('d')),
                Pair(Member('c'), None)
            ])
        ])

    def test_evaluate(self):
        last_pairs = Pairs([
            Pair(Member('a'), Member('b')),
            Pair(Member('c'), Member('d')),
            Pair(Member('e'), None)
        ])
        members = Members(
            [Member('a'),
             Member('b'),
             Member('c'),
             Member('d'),
             Member('e')])
        pairs = EvaluationService().evaluate([last_pairs], members)
        self.assertEqual(pairs, [
            Pairs([
                Pair(Member('a'), Member('c')),
                Pair(Member('d'), Member('e')),
                Pair(Member('b'), None)
            ]),
            Pairs([
                Pair(Member('a'), Member('d')),
                Pair(Member('c'), Member('e')),
                Pair(Member('b'), None)
            ]),
            Pairs([
                Pair(Member('a'), Member('e')),
                Pair(Member('b'), Member('c')),
                Pair(Member('d'), None)
            ]),
            Pairs([
                Pair(Member('a'), Member('e')),
                Pair(Member('b'), Member('d')),
                Pair(Member('c'), None)
            ]),
            Pairs([
                Pair(Member('b'), Member('c')),
                Pair(Member('d'), Member('e')),
                Pair(Member('a'), None)
            ]),
            Pairs([
                Pair(Member('b'), Member('d')),
                Pair(Member('c'), Member('e')),
                Pair(Member('a'), None)
            ]),
            Pairs([
                Pair(Member('b'), Member('e')),
                Pair(Member('a'), Member('c')),
                Pair(Member('d'), None)
            ]),
            Pairs([
                Pair(Member('b'), Member('e')),
                Pair(Member('a'), Member('d')),
                Pair(Member('c'), None)
            ]),
        ])

    def test_evaluate_twice(self):
        history = [
            Pairs([
                Pair(Member('a'), Member('b')),
                Pair(Member('c'), Member('d')),
                Pair(Member('e'), None)
            ]),
            Pairs([
                Pair(Member('a'), Member('c')),
                Pair(Member('d'), Member('e')),
                Pair(Member('b'), None)
            ])
        ]
        members = Members(
            [Member('a'),
             Member('b'),
             Member('c'),
             Member('d'),
             Member('e')])
        pairs = EvaluationService().evaluate(history, members)
        self.assertEqual(pairs, [
            Pairs([
                Pair(Member('b'), Member('c')),
                Pair(Member('a'), Member('e')),
                Pair(Member('d'), None)
            ]),
            Pairs([
                Pair(Member('c'), Member('d')),
                Pair(Member('b'), Member('e')),
                Pair(Member('a'), None)
            ])
        ])

    def test_evaluate_three_times(self):
        history = [
            Pairs([
                Pair(Member('a'), Member('b')),
                Pair(Member('c'), Member('d')),
                Pair(Member('e'), None)
            ]),
            Pairs([
                Pair(Member('a'), Member('c')),
                Pair(Member('d'), Member('e')),
                Pair(Member('b'), None)
            ]),
            Pairs([
                Pair(Member('c'), Member('d')),
                Pair(Member('b'), Member('e')),
                Pair(Member('a'), None)
            ])
        ]
        members = Members(
            [Member('a'),
             Member('b'),
             Member('c'),
             Member('d'),
             Member('e')])
        pairs = EvaluationService().evaluate(history, members)
        self.assertEqual(pairs, [
            Pairs([
                Pair(Member('d'), Member('e')),
                Pair(Member('a'), Member('b')),
                Pair(Member('c'), None)
            ])
        ])

    def test_evaluate_four_times(self):
        history = [
            Pairs([
                Pair(Member('a'), Member('b')),
                Pair(Member('c'), Member('d')),
                Pair(Member('e'), None)
            ]),
            Pairs([
                Pair(Member('a'), Member('c')),
                Pair(Member('d'), Member('e')),
                Pair(Member('b'), None)
            ]),
            Pairs([
                Pair(Member('c'), Member('d')),
                Pair(Member('b'), Member('e')),
                Pair(Member('a'), None)
            ]),
            Pairs([
                Pair(Member('d'), Member('e')),
                Pair(Member('a'), Member('b')),
                Pair(Member('c'), None)
            ])
        ]
        members = Members(
            [Member('a'),
             Member('b'),
             Member('c'),
             Member('d'),
             Member('e')])
        pairs = EvaluationService().evaluate(history, members)
        self.assertEqual(pairs, [
            Pairs([
                Pair(Member('b'), Member('e')),
                Pair(Member('a'), Member('c')),
                Pair(Member('d'), None)
            ])
        ])

    def test_evaluate_five_times(self):
        history = [
            Pairs([
                Pair(Member('a'), Member('b')),
                Pair(Member('c'), Member('d')),
                Pair(Member('e'), None)
            ]),
            Pairs([
                Pair(Member('a'), Member('c')),
                Pair(Member('d'), Member('e')),
                Pair(Member('b'), None)
            ]),
            Pairs([
                Pair(Member('c'), Member('d')),
                Pair(Member('b'), Member('e')),
                Pair(Member('a'), None)
            ]),
            Pairs([
                Pair(Member('d'), Member('e')),
                Pair(Member('a'), Member('b')),
                Pair(Member('c'), None)
            ]),
            Pairs([
                Pair(Member('b'), Member('e')),
                Pair(Member('a'), Member('c')),
                Pair(Member('d'), None)
            ])
        ]
        members = Members(
            [Member('a'),
             Member('b'),
             Member('c'),
             Member('d'),
             Member('e')])
        pairs = EvaluationService().evaluate(history, members)
        self.assertEqual(pairs, [
            Pairs([
                Pair(Member('a'), Member('b')),
                Pair(Member('c'), Member('d')),
                Pair(Member('e'), None)
            ])
        ])
