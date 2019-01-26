from typing import List

from resources.protobuf import pair_pb2
from resources.protobuf.pair_pb2_grpc import PairServiceServicer
from src.domain.model.pair.pair import Members, Pairs
from src.infrastructure.serialize.protobuf.pair import ProtoBufPairSerializer
from src.registry.usecase import next_pairs_by_history, save_pairs_history


class PairService(PairServiceServicer):
    def SavePairsHistory(self, request: pair_pb2.Pairs,
                         context) -> pair_pb2.Pairs:
        pairs: Pairs = ProtoBufPairSerializer().load_pairs(request)
        save_pairs_history().run(pairs)
        return request

    def NextPairsByHistory(self, request: pair_pb2.Members,
                           context) -> pair_pb2.PossiblePairs:
        serializer = ProtoBufPairSerializer()
        members: Members = serializer.load_members(request)
        pairs_list: List[Pairs] = next_pairs_by_history().run(members)
        return serializer.dump_possible_pairs(pairs_list)
