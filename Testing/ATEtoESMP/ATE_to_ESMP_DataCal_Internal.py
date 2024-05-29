
import socket
from time import sleep


# import sys
# import random

########################################################################################################################
class ATE_ESMP_DataCal_Internal_Mode_MSG():
    def __init__(self):
        super(ATE_ESMP_DataCal_Internal_Mode_MSG, self).__init__()
        self.Packet = []
    #########################################################################################################################
        """self.s = socket.socket()  # Create a socket object
        self.port = 5555  # Reserve a port for your service every new transfer wants a new port or you must wait.

        self.s.connect(('localhost', self.port))
        self.CAL_MSG = b'Platinum'  ##### DataCal_Internal_Mode msg to be written
        self.s.send(self.CAL_MSG)
        self.data = self.s.recv(1024)
        print(self.data)
        sleep(3)"""

    #########################################################################################################

    def DataCalInternalModePacket(self, SM=2,Mscode=1,seqNo=1,msglen=2,RB=0, BFreq=500, TFreq=500, SigType=0, PW=0, PRI=0, THRS=35, IFBWS=1,
                                  SECSel=1, RFATT1=0, RFATT2=0, RFATT3=0, RFATT4=0, RFATT5=0, RFATT6=0, IFATTN1=0,
                                  IFATTN2=0, IFATTN3=0, IFATTN4=0, IFATTN5=0, IFATTN6=0, SSV=0,footer=2):
        #self.Packet =[]
        self.Packet.append(SM.to_bytes(2, 'big', signed=False))
        self.Packet.append(Mscode.to_bytes(2, 'big', signed=False))
        self.Packet.append(seqNo.to_bytes(2, 'big', signed=False))
        self.Packet.append(msglen.to_bytes(4, 'big', signed=False))
        self.ReceiverBand = self.Packet.append(RB.to_bytes(1, 'big', signed=False))
        self.BITEFrequency = self.Packet.append(BFreq.to_bytes(4, 'big', signed=False))
        self.TuningFrequency = self.Packet.append(TFreq.to_bytes(4, 'big', signed=False))
        self.SignalType = self.Packet.append(SigType.to_bytes(1, 'big', signed=False))
        self.PulseWidth = self.Packet.append(PW.to_bytes(4, 'big', signed=False))
        self.PRI = self.Packet.append(PRI.to_bytes(4, 'big', signed=False))
        self.Threshold = self.Packet.append(THRS.to_bytes(1, 'big', signed=False))
        self.IFBandwidthSelection = self.Packet.append(IFBWS.to_bytes(1, 'big', signed=False))
        self.SectorSelection = self.Packet.append(SECSel.to_bytes(1, 'big', signed=False))
        self.RFAttenuation1 = self.Packet.append(RFATT1.to_bytes(1, 'big', signed=False))
        self.RFAttenuation2 = self.Packet.append(RFATT2.to_bytes(1, 'big', signed=False))
        self.RFAttenuation3 = self.Packet.append(RFATT3.to_bytes(1, 'big', signed=False))
        self.RFAttenuation4 = self.Packet.append(RFATT4.to_bytes(1, 'big', signed=False))
        self.RFAttenuation5 = self.Packet.append(RFATT5.to_bytes(1, 'big', signed=False))
        self.RFAttenuation6 = self.Packet.append(RFATT6.to_bytes(1, 'big', signed=False))
        self.IFAttenuation1 = self.Packet.append(IFATTN1.to_bytes(1, 'big', signed=False))
        self.IFAttenuation2 = self.Packet.append(IFATTN2.to_bytes(1, 'big', signed=False))
        self.IFAttenuation3 = self.Packet.append(IFATTN3.to_bytes(1, 'big', signed=False))
        self.IFAttenuation4 = self.Packet.append(IFATTN4.to_bytes(1, 'big', signed=False))
        self.IFAttenuation5 = self.Packet.append(IFATTN5.to_bytes(1, 'big', signed=False))
        self.IFAttenuation6 = self.Packet.append(IFATTN6.to_bytes(1, 'big', signed=False))
        self.SectorSelectionValue = self.Packet.append(SSV.to_bytes(1, 'big', signed=False))
        self.Packet.append(footer.to_bytes(2, 'big', signed=False))

##########################################################################################################

        self.Packet=b"".join(self.Packet)
        print(self.Packet)

        #self.s.send(bytes(str(self.Packet), 'utf-8'))

########################################################################################################################
if __name__ == "__main__":
    app = ATE_ESMP_DataCal_Internal_Mode_MSG()
    app.DataCalInternalModePacket(SM=0xAAAA,Mscode=5005,seqNo=1,msglen=27,RB=1//1, BFreq=int(500//0.01), TFreq=500//10, SigType=1//1, PW=50//10, PRI=2//1,
                                  THRS=-40//-1, IFBWS=1//1, SECSel=1//1, RFATT1=0//2, RFATT2=0//2, RFATT3=0//2, RFATT4=0//2,
                                   RFATT5=0//2, RFATT6=0//2, IFATTN1=0//2, IFATTN2=0//2, IFATTN3=0//2,
                                    IFATTN4=0//2, IFATTN5=0//2, IFATTN6=0//2, SSV=0//1,footer=0xEEEE)














