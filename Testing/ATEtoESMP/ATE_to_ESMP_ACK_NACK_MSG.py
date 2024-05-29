
import socket
from time import sleep


# import sys
# import random

########################################################################################################################
class ATE_ESMP_ACK_NACK_MSG():
    def __init__(self):
        super(ATE_ESMP_ACK_NACK_MSG, self).__init__()
        self.Packet = []
    #########################################################################################################################
        """self.s = socket.socket()  # Create a socket object
        self.port = 5555  # Reserve a port for your service every new transfer wants a new port or you must wait.

        self.s.connect(('localhost', self.port))
        self.CAL_MSG = b'Platinum'  ##### DataCal_Internal_Mode msg to be written
        self.s.send(self.CAL_MSG)
        self.data = self.s.recv(1024)     ###sock.send('NACK'.encode('ascii'))
        print(self.data.decode('utf-8'))
        sleep(1)"""

    #########################################################################################################

    def ACK_NACKPacket(self,SM=2,Mscode=1,seqNo=1,msglen=2, MC=0, SeqNum=0, ACKStatus=1,footer=2):
        #self.Packet =[]

        self.Packet.append(SM.to_bytes(2, 'big', signed=False))
        self.Packet.append(Mscode.to_bytes(2, 'big', signed=False))
        self.Packet.append(seqNo.to_bytes(2, 'big', signed=False))
        self.Packet.append(msglen.to_bytes(4, 'big', signed=False))
        self.MessageCode = self.Packet.append(MC.to_bytes(2, 'big', signed=False))
        self.SequenceNumber = self.Packet.append(SeqNum.to_bytes(2, 'big', signed=False))
        self.AcknowledgementStatus = self.Packet.append(ACKStatus.to_bytes(1, 'big', signed=False))

        self.Packet.append(footer.to_bytes(2, 'big', signed=False))

##########################################################################################################
        """print(self.Packet)


        self.s.send(bytes(str(self.Packet), 'utf-8'))
"""
        self.Packet = b"".join(self.Packet)
        print(self.Packet)



########################################################################################################################
if __name__ == "__main__":
    app = ATE_ESMP_ACK_NACK_MSG()
    app.ACK_NACKPacket(SM=0xAAAA,Mscode=5020,seqNo=1,msglen=8,MC=2050//1, SeqNum=5555//1, ACKStatus=1//1,footer=0xEEEE)














