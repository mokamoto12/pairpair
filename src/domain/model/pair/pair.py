from abc import ABC, abstractmethod
from functools import reduce
from itertools import combinations
from typing import Iterator, List, Optional, Tuple

from dataclasses import dataclass


@dataclass
class Member:
    name: str


@dataclass
class Pair:
    first: Member
    second: Optional[Member]

    def __contains__(self, item: Member) -> bool:
        if not isinstance(item, Member):
            return False
        return self.first == item or self.second == item

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pair):
            return False
        return (self.first == other.first and self.second == other.second) or (
            self.first == other.second and self.second == other.first)

    def only_has_either(self, other: 'Pair') -> bool:
        return (self.first == other.first and self.second != other.second) or (
            self.first == other.second and self.second != other.first) or (
                self.second == other.first and self.first != other.second) or (
                    self.second == other.second and self.first != other.first)


@dataclass
class Pairs:
    list: List[Pair]

    def __getitem__(self, item: int) -> Pair:
        return self.list[item]

    def __len__(self) -> int:
        return len(self.list)

    def __contains__(self, item: Pair) -> bool:
        if not isinstance(item, Pair):
            return False
        return item in self.list

    def tail(self) -> 'Pairs':
        return Pairs(self.list[1:])

    def prepend(self, pair: Pair) -> 'Pairs':
        return Pairs([pair, *self.list])

    def merge(self, other: 'Pairs') -> 'Pairs':
        return Pairs(self.list + other.list)


@dataclass
class PairTree:
    pair: Pair
    remainder: List['PairTree']

    def fold(self) -> List[Pairs]:
        if not self.remainder:
            return [Pairs([self.pair])]

        return [
            pairs.prepend(self.pair) for pair_tree in self.remainder
            for pairs in pair_tree.fold()
        ]


@dataclass
class Members:
    list: List[Member]

    def __iter__(self) -> Iterator[Member]:
        yield from self.list

    def __len__(self) -> int:
        return len(self.list)

    def remaining_members(self, pair: Pair) -> 'Members':
        return Members([member for member in self if member not in pair])

    def select_first_pairs(self) -> List[Tuple[Optional[Pair], 'Members']]:
        if len(self) == 0:
            return [(None, Members([]))]
        elif len(self) == 1:
            return [(Pair(self.list[0], None), Members([]))]
        first_pairs = [Pair(a, b) for a, b in combinations(self, 2)]
        return [(pair, self.remaining_members(pair)) for pair in first_pairs]

    def combinations(self) -> List[PairTree]:
        """
        e.g. [(Pair(a, b), [
               (Pair(c, d), [(Pair(e, None), [])]),
               (Pair(c, e), [(Pair(d, None), [])]),
               (Pair(e, d), [(Pair(c, None), [])])]),
              (Pair(a, c), [...])]
        """
        return [
            PairTree(pair, remaining_members.combinations())
            for pair, remaining_members in self.select_first_pairs()
            if pair is not None
        ]

    def possible_pair(self) -> List[Pairs]:
        pass


class PairsHistoryRepository(ABC):
    @abstractmethod
    def save(self, pairs: Pairs) -> None:
        pass

    @abstractmethod
    def load(self) -> List[Pairs]:
        pass


class EvaluationService:
    def evaluate(self, history: List[Pairs], members: Members) -> Pairs:
        filtered_pair_trees = self.pair_must_have_only_either_member_of_last_pair(
            history[-1], members.combinations())

        if not filtered_pair_trees:
            filtered_pair_trees = members.combinations()

        filtered_pair_trees2 = filtered_pair_trees
        for i in range(1, len(history) + 1):
            tmp = self.pair_should_not_exist_same_pair_in_near_history(
                history[-i:], filtered_pair_trees)
            if not tmp:
                continue
            else:
                filtered_pair_trees2 = tmp

        possible_pairs: List[Pairs] = [
            pairs for pair_tree in filtered_pair_trees2
            for pairs in pair_tree.fold()
        ]
        return possible_pairs[0]

    def pair_must_have_only_either_member_of_last_pair(
            self, last_pairs: Pairs,
            pair_trees: List[PairTree]) -> List[PairTree]:
        if not last_pairs:
            return pair_trees

        return [
            PairTree(
                tree.pair,
                self.pair_must_have_only_either_member_of_last_pair(
                    last_pairs.tail(), tree.remainder)) for tree in pair_trees
            if tree.pair.only_has_either(last_pairs[0]) and (
                not last_pairs.tail() or (last_pairs.tail(
                ) and self.pair_must_have_only_either_member_of_last_pair(
                    last_pairs.tail(), tree.remainder)))
        ]

    def pair_should_not_exist_same_pair_in_near_history(
            self, history: List[Pairs],
            pair_trees: List[PairTree]) -> List[PairTree]:
        if not history:
            return pair_trees

        old_pairs: Pairs = reduce(lambda acc, pairs: acc.merge(pairs), history)

        def aux(trees: List[PairTree], remainder_depth: int) -> List[PairTree]:
            return [
                PairTree(tree.pair, aux(tree.remainder, remainder_depth - 1))
                for tree in trees if tree.pair not in old_pairs and
                (remainder_depth - 1 == 0 or (remainder_depth - 1 > 0 and aux(
                    tree.remainder, remainder_depth - 1)))
            ]

        return aux(pair_trees, len(history[0]))
