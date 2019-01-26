from abc import ABC, abstractmethod
from typing import List

from dataclasses import dataclass
from src.domain.model.pair.pair import Members, Pairs, PairTree


@dataclass
class PairsHistoryId:
    value: str


class PairsHistory:
    identity: PairsHistoryId
    pairs: Pairs

    def __init__(self, identity: PairsHistoryId, pairs: Pairs) -> None:
        self.identity = identity
        self.pairs = pairs


class PairsHistoryRepository(ABC):
    @abstractmethod
    def next_identity(self) -> PairsHistoryId:
        pass

    @abstractmethod
    def save(self, pairs_history: PairsHistory) -> None:
        pass

    @abstractmethod
    def load(self) -> List[Pairs]:
        pass


class EvaluationService:
    def evaluate(self, history: List[Pairs], members: Members) -> List[Pairs]:
        if not history:
            return PairTree.possible_pairs(members.combinations())

        filtered_pair_trees = self.pair_must_have_only_either_member_of_last_pair(
            history[-1], members.combinations())

        if not filtered_pair_trees:
            filtered_pair_trees = members.combinations()

        possible_pairs: List[Pairs] = PairTree.possible_pairs(
            filtered_pair_trees)

        possible_pairs = self.member_is_must_not_in_same_position_at_three_times(
            history, possible_pairs)

        good_pairs = possible_pairs
        for i in range(1, len(history) + 1):
            tmp = self.pair_should_not_exist_same_pair_in_near_history(
                history[-i:], possible_pairs)
            if not tmp:
                break
            else:
                good_pairs = tmp

        return good_pairs

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

    def member_is_must_not_in_same_position_at_three_times(
            self, history: List[Pairs],
            possible_pairs: List[Pairs]) -> List[Pairs]:
        if len(history) < 2:
            return possible_pairs

        def member_in_same_position_at_three_times(pairs: Pairs) -> bool:
            return any(
                map(
                    lambda old_pair1, old_pair2, current_pair: (current_pair.first in old_pair1 and current_pair.first in old_pair2) or (current_pair.second in old_pair1 and current_pair.second in old_pair2),
                    history[-1], history[-2], pairs))

        return [
            pairs for pairs in possible_pairs
            if not member_in_same_position_at_three_times(pairs)
        ]

    def pair_should_not_exist_same_pair_in_near_history(
            self, history: List[Pairs],
            possible_pairs: List[Pairs]) -> List[Pairs]:

        return [
            pairs for pairs in possible_pairs
            if all(not pairs.have_same(old_pairs) for old_pairs in history)
        ]
