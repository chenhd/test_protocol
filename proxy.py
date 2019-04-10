import socket
import asyncore
import struct
import time
import json
from modify_data import get_modify_data


# length + pid + data
HEAD_SIZE = struct.calcsize(">II")


class Proxy(asyncore.dispatcher):
    def __init__(self, host, port, gs_address):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("0.0.0.0", port))
        self.listen(5)
        
        self.gs_address = gs_address
        
        self.host = host
        self.port = port
        
    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
    def handle_accept(self):
        client, addr = self.accept()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect(self.gs_address)
        
#         接收到来自客户端的链接client，创建链接服务端的链接server
#         互相持有对象引用，并加入异步特性

#         核心功能 单纯的转发协议，所以只需实现handle read接口，读取所有数据，转发出去即可
#         拓展功能 读取协议、改写协议并将改写之后的协议转发出去（具体是改写从客户端发往服务器的协议，因为假设服务器的行为为正确行为）
        ProxyClientHandle(client, server)
        ProxyServerHandle(client, server)
        
        
class ProxyClientHandle(asyncore.dispatcher):
    def __init__(self, client, server):
        asyncore.dispatcher.__init__(self, client)
        self.server = server
        
        self.recvStat = 1
        self.recvHeader = b""
        self.recvBody = b""
        
        self.length = -1
        self.pid = -1
        
        
    def handle_read(self):
        if self.recvStat == 1:
            self.recvHeader = self.recvHeader + self.recv(HEAD_SIZE - len(self.recvHeader))
            if len(self.recvHeader) < HEAD_SIZE:
                return
            self.length, self.pid = struct.unpack(">II", self.recvHeader)
            self.recvStat = 2
        else:
            self.recvBody = self.recvBody + self.recv(self.length - len(self.recvBody))
            if len(self.recvBody) < self.length:
                return
            
            
            
            # modify protocol
            data = self.recvHeader+self.recvBody
##################################################################
#             修改客户端协议的位置
            data = modify_protocol(data)
##################################################################
            
            self.server.send(data)
#             self.server.send(self.recvHeader+self.recvBody)
            print("send: ", self.pid, self.length, self.recvBody)

            
            self.recvStat = 1
            self.recvHeader = b""
            self.recvBody = b""
            
            self.length = -1
            self.pid = -1
        
    def handle_close(self):
        self.close()
        
class ProxyServerHandle(asyncore.dispatcher):
    def __init__(self, client, server):
        asyncore.dispatcher.__init__(self, server)
        self.client = client
        
        self.recvStat = 1
        self.recvHeader = b""
        self.recvBody = b""
        
        self.length = -1
        self.pid = -1
        
    def handle_read(self):
        if self.recvStat == 1:
            self.recvHeader = self.recvHeader + self.recv(HEAD_SIZE - len(self.recvHeader))
            if len(self.recvHeader) < HEAD_SIZE:
                return
            self.length, self.pid = struct.unpack(">II", self.recvHeader)
            self.recvStat = 2
        else:
            self.recvBody = self.recvBody + self.recv(self.length - len(self.recvBody))
            if len(self.recvBody) < self.length:
                return
            
            self.client.send(self.recvHeader+self.recvBody)
            print("recv: ", self.pid, self.length, self.recvBody)

            
            self.recvStat = 1
            self.recvHeader = b""
            self.recvBody = b""
            
            self.length = -1
            self.pid = -1
        
    def handle_close(self):
        self.close()






def modify_protocol(protocol_data):
    data = protocol_data
    
    _, pid = struct.unpack(">II", protocol_data[:HEAD_SIZE])
#     data_body = protocol_data[HEAD_SIZE:]
    
    modify_data_dict = get_modify_data()
        
    if str(pid) in modify_data_dict:
        modify_data_body = modify_data_dict[str(pid)]
        data = struct.pack('>II', len(modify_data_body), pid) + bytes(modify_data_body, "ascii")
    
    return data




if __name__ == "__main__":
    print("Proxy")
    gs_address = ("0.0.0.0", 60000)
    proxy = Proxy("0.0.0.0", 60001, gs_address)
    asyncore.loop()