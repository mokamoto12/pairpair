from itertools import combinations
from typing import Dict, Iterator, List, Optional, Tuple

from dataclasses import dataclass


@dataclass
class Member:
    name: str


@dataclass
class Pair:
    first: Member
    second: Optional[Member]

    def __contains__(self, item: Optional[Member]) -> bool:
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

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            'first': self.first.name,
            'second': self.second.name if self.second is not None else None
        }

    @staticmethod
    def from_dict(data: Dict[str, Optional[str]]) -> 'Pair':
        if data['first'] is None:
            raise RuntimeError()

        return Pair(
            Member(data['first']),
            Member(data['second']) if data['second'] is not None else None)


@dataclass
class Pairs:
    list: List[Pair]

    def __iter__(self) -> Iterator[Pair]:
        yield from self.list

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

    def have_same(self, other: 'Pairs') -> bool:
        return any(
            map(lambda self_pair, other_pair: self_pair == other_pair, self,
                other))

    def to_list(self) -> List[Dict[str, Optional[str]]]:
        return [pair.to_dict() for pair in self.list]

    @staticmethod
    def from_list(list: List[Dict[str, Optional[str]]]) -> 'Pairs':
        return Pairs([Pair.from_dict(d) for d in list])

    @staticmethod
    def from_list2(data: List[List[str]]) -> 'Pairs':
        return Pairs([
            Pair(Member(l[0]),
                 Member(l[1]) if len(l) == 2 else None) for l in data
        ])


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

    @staticmethod
    def possible_pairs(trees: List['PairTree']) -> List[Pairs]:
        return [pairs for pair_tree in trees for pairs in pair_tree.fold()]


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

    @staticmethod
    def from_list(data: List[str]) -> 'Members':
        return Members([Member(l) for l in data])
