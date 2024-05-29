########################################################################################################################
import socket
from time import sleep


# import sys
# import random

########################################################################################################################
class ATE_ESMP_Restart_MSG():
    def __init__(self):
        super(ATE_ESMP_Restart_MSG, self).__init__()
        self.Packet=[]
        ################################################################################################################
        """self.s = socket.socket()  # Create a socket object
        self.port = 5555  # Reserve a port for your service every new transfer wants a new port or you must wait.

        self.s.connect(('localhost', self.port))
        self.CAL_MSG = b'CALSTART'
        if self.CAL_MSG == b'CALSTART':
            self.s.send(self.CAL_MSG)
            self.data = self.s.recv(1024)
            print(self.data)
            sleep(5)
        else:
            print(self.data)"""

    def RestartPacket(self,SM=2,Mscode=1,seqNo=1,msglen=2,footer=2):
        #self.Packet =[]

        self.Packet.append(SM.to_bytes(2,'big',signed=False))
        self.Packet.append(Mscode.to_bytes(2, 'big', signed=False))
        self.Packet.append(seqNo.to_bytes(2, 'big', signed=False))
        self.Packet.append(msglen.to_bytes(4, 'big', signed=False))
        self.Packet.append(footer.to_bytes(2, 'big', signed=False))
        """print(self.Packet)

        self.s.send(bytes(str(self.Packet), 'utf-8'))"""
        self.Packet = b"".join(self.Packet)
        print(self.Packet)


########################################################################################################################
if __name__ == "__main__":
    app = ATE_ESMP_Restart_MSG()
    app.RestartPacket(SM=0xAAAA, Mscode=5010, seqNo=1, msglen=5, footer=0xEEEE)

