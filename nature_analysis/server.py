import zerorpc

class HelloRPC(object):
    def hello(self, name):
        '''
        测试rpc
        '''
        return "Hello, %s" % name

s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:11334")
s.run()
