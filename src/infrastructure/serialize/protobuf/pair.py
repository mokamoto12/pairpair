from typing import List

from resources.protobuf import pair_pb2
from src.domain.model.pair.pair import Member, Members, Pair, Pairs


class ProtoBufPairSerializer:
    def load_member(self, message: pair_pb2.Member) -> Member:
        return Member(message.name)

    def load_pair(self, message: pair_pb2.Pair) -> Pair:
        return Pair(
            self.load_member(message.first),
            self.load_member(message.second)
            if message.second is not None else None)

    def load_pairs(self, message: pair_pb2.Pairs) -> Pairs:
        return Pairs([self.load_pair(pair) for pair in message.pairs])

    def load_members(self, message: pair_pb2.Members) -> Members:
        return Members([self.load_member(m) for m in message.members])

    def dump_member(self, member: Member) -> pair_pb2.Member:
        return pair_pb2.Member(name=member.name)

    def dump_pair(self, pair: Pair) -> pair_pb2.Pair:
        return pair_pb2.Pair(
            first=self.dump_member(pair.first),
            second=self.dump_member(pair.second)
            if pair.second is not None else None)

    def dump_pairs(self, pairs: Pairs) -> pair_pb2.Pairs:
        return pair_pb2.Pairs(
            pairs=[self.dump_pair(pair) for pair in pairs.list])

    def dump_possible_pairs(self,
                            pairs_list: List[Pairs]) -> pair_pb2.PossiblePairs:
        return pair_pb2.PossiblePairs(
            pairs_list=[self.dump_pairs(pairs) for pairs in pairs_list])
