import logging

from src.interfaces.grpc.pairpair import serve

if __name__ == '__main__':
    logging.basicConfig()
    serve()
