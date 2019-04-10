import asyncore
import struct

def get_current_func_name():
    import sys
    return sys._getframe(1).f_code.co_name

protocol_data_dict = {
    101: "verify data",
    102: "login data",
    
    201: "enter_scene data",
    202: "switch_map data",
    
    301: "logout data",
    }


class EchoClient(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.connect( (host, port) )
    
    def handle_close(self):
        self.close()
        
    def handle_connect(self):
#         connect done. 
                
        self.send_first_protocol()
        
    def send_first_protocol(self):
        self.send_verify_req()
        
    def send_data(self, data):
        pid_size = struct.calcsize(">I")
        data = struct.pack(">I", len(data)-pid_size) + data
        self.send(data)

    def handle_read(self):

#         decode here usually
        
#         todo: recv data without handling boundary
        data = self.recv(8192)
        print("data ", data)
        
        head_size = struct.calcsize(">II")
        
        length, pid, = struct.unpack(">II", data[:head_size])
        protocol_data = data[head_size:]
         
        self.on_protocol(pid, protocol_data)



    
    def on_protocol(self, pid, protocol_data):
# #         不合理思路
#         try:
#             handle = getattr(self, "on_" + protocol_data.decode('ascii'))
#         except AttributeError as e:
#             print("unhandle protocol:")
#             print(e)
#             return
#             
#         handle(pid, protocol_data)
        

        EchoClient.res_handle[pid](self, pid, protocol_data)
        
    
    def send_verify_req(self):
        pid = 101
        data = struct.pack(">I", pid) + bytes(protocol_data_dict[pid], "ascii")
        self.send_data(data)
    def on_verify(self, pid, protocol_data):
        print(get_current_func_name(), pid, protocol_data)
        
        self.send_login_req()

    def send_login_req(self):
        pid = 102
        data = struct.pack(">I", pid) + bytes(protocol_data_dict[pid], "ascii")
        self.send_data(data)
    def on_login(self, pid, protocol_data):
        print(get_current_func_name(), pid, protocol_data)
        
        self.send_enter_scene_req()

    def send_enter_scene_req(self):
        pid = 201
        data = struct.pack(">I", pid) + bytes(protocol_data_dict[pid], "ascii")
        self.send_data(data)
    def on_enter_scene(self, pid, protocol_data):
        print(get_current_func_name(), pid, protocol_data)
        
        self.send_switch_map_req()
    
    def send_switch_map_req(self):
        pid = 202
        data = struct.pack(">I", pid) + bytes(protocol_data_dict[pid], "ascii")
        self.send_data(data)
    def on_switch_map(self, pid, protocol_data):
        print(get_current_func_name(), pid, protocol_data)
        
        self.send_logout_req()
    
    def send_logout_req(self):
        pid = 301
        data = struct.pack(">I", pid) + bytes(protocol_data_dict[pid], "ascii")
        self.send_data(data)
    def on_logout(self, pid, protocol_data):
        print(get_current_func_name(), pid, protocol_data)
        
        self.close()
    
    
    res_handle = {
        101: on_verify,
        102: on_login,
        
        201: on_enter_scene,
        202: on_switch_map,
        
        301: on_logout,
        }
if __name__ == '__main__':
    print("Client")
    # server
#     server = EchoClient('0.0.0.0', 60000)
    # proxy
    server = EchoClient('0.0.0.0', 60001)
    
    asyncore.loop()