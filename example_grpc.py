from os import path
import json
import grpc
import protol

SERVER_ADDRESS = '127.0.0.1:50000'

nlpindo_pb2, nlpindo_pb2_grpc = protol.load(path.dirname(path.abspath(__file__)) + '/protos/nlpindo.proto')

with open('example.peterpan.txt', 'r') as f:
    text = f.read()

if __name__ == '__main__':
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = nlpindo_pb2_grpc.NLPIndoStub(channel)

    param = nlpindo_pb2.String(string=json.dumps({
        'text': text,
    }))

    # response = stub.Stem(param)
    # response = stub.Tokenize(param)
    response = stub.WordCount(param)

    response = json.loads(response.string)
    print(response)
