import time
from concurrent import futures
from typing import List

import grpc

from resources.protobuf import pair_pb2, pair_pb2_grpc
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


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pair_pb2_grpc.add_PairServiceServicer_to_server(PairService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)
