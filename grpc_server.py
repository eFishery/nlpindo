from os import path
import time
import json
from concurrent import futures

import grpc
import protol

from nlpindo.worder import Worder
from nlpindo.stemmer import Stemmer

SERVER_ADDRESS = '127.0.0.1:50000'
MAX_WORKERS = 10
ONE_DAY_IN_SECONDS = 86400

nlpindo_pb2, nlpindo_pb2_grpc = protol.load(path.dirname(path.abspath(__file__)) + '/protos/nlpindo.proto')

worder = Worder()
stemmer = Stemmer()

class Server(nlpindo_pb2_grpc.NLPIndoServicer):
    def Stem(self, request, context):
        param = json.loads(request.string)
        result = stemmer.stem(param['text'])
        result = json.dumps(result)
        return nlpindo_pb2.String(string=result)

    def Tokenize(self, request, context):
        param = json.loads(request.string)
        result = worder.tokenize(param['text'])
        result = json.dumps(result)
        return nlpindo_pb2.String(string=result)

    def WordCount(self, request, context):
        param = json.loads(request.string)
        if 'remove_stopwords' in param:
            result = worder.word_count(param['text'], param['remove_stopwords'])
        else:
            result = worder.word_count(param['text'])
        result = json.dumps(result)
        return nlpindo_pb2.String(string=result)

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
    nlpindo_pb2_grpc.add_NLPIndoServicer_to_server(Server(), server)
    server.add_insecure_port(SERVER_ADDRESS)
    server.start()
    print('started')
    try:
        while True:
            time.sleep(ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
