import socket
from time import sleep


# import sys
# import random

import pandas as pd

df = pd.read_csv('C:/Users/jaswa/PycharmProjects/ATEC/Testing/ESMPtoATE/ATE_to_System_Msg_Format.csv')


PM1 = df.loc[(df['cmd_id'] == 'SM'), 'cmd_code'].values[0]
PM2 = df.loc[(df['cmd_id'] == 'ESMP_ATE_Track_Data_Mscode'), 'cmd_code'].values[0]
PM3 = df.loc[(df['cmd_id'] == 'seqNo'), 'cmd_code'].values[0]
PM4 = df.loc[(df['cmd_id'] == 'ESMP_ATE_Track_Data_msglen'), 'cmd_code'].values[0]
PM5 = df.loc[(df['cmd_id'] == 'footer'), 'cmd_code'].values[0]


########################################################################################################################
class ESMP_ATE_Track_Data():
    def __init__(self):
        super(ESMP_ATE_Track_Data, self).__init__()
        self.Packet = []
    #########################################################################################################################
        '''self.s = socket.socket()  # Create a socket object
        self.port = 5555  # Reserve a port for your service every new transfer wants a new port or you must wait.
        self.s.connect(('localhost', self.port))
        self.data = self.s.recv(1024)
        print(self.data)
        sleep(3)'''

    #########################################################################################################

    def TrackDataPacket(self,SM,Mscode,seqNo,msglen, TrackNo, TrackStatus, DOA, Frequency, FreqAttributes, PW, PRF, PRIAttributes, Amplitude, ScanType,
                        AntennaScanPeriod, TOFA, TOLA, ActivityCount, TrackAge, TrackHitCount, Identity1, ConfidenceLevel1, Identity2, ConfidenceLevel2,
                        Identity3, ConfidenceLevel3, Identity4, ConfidenceLevel4, Identity5, ConfidenceLevel5, Reserved, FreqMin, FreqMax, PWMin, PWMax,
                        PGRI, SpotPRFs, SpotPWs, SpotFreqencies, DOAAccuracy, PRI, PRIMin, PRIMax, ANtennaScanRate, TrackPDCount, BinNumber, BinType,
                        ProfileCount, ProfileFreq, ProfileAmp, ProfilePW, ProfilePRI, footer):
        #self.Packet =[]

        self.Packet.append(SM.to_bytes(2,'big',signed=False))
        self.Packet.append(Mscode.to_bytes(2, 'big', signed=False))
        self.Packet.append(seqNo.to_bytes(2, 'big', signed=False))
        self.Packet.append(msglen.to_bytes(4, 'big', signed=False))
        self.Packet.append(TrackNo.to_bytes(2, 'big', signed=False))
        self.Packet.append(TrackStatus.to_bytes(2, 'big', signed=False))
        self.Packet.append(DOA.to_bytes(2, 'big', signed=False))
        self.Packet.append(Frequency.to_bytes(4, 'big', signed=False))
        self.Packet.append(FreqAttributes.to_bytes(4, 'big', signed=False))
        self.Packet.append(PW.to_bytes(4, 'big', signed=False))
        self.Packet.append(PRF.to_bytes(4, 'big', signed=False))
        self.Packet.append(PRIAttributes.to_bytes(4, 'big', signed=False))
        self.Packet.append(Amplitude.to_bytes(1, 'big', signed=False))
        self.Packet.append(ScanType.to_bytes(1, 'big', signed=False))
        self.Packet.append(AntennaScanPeriod.to_bytes(2, 'big', signed=False))
        self.Packet.append(TOFA.to_bytes(4, 'big', signed=False))
        self.Packet.append(TOLA.to_bytes(4, 'big', signed=False))
        self.Packet.append(ActivityCount.to_bytes(2, 'big', signed=False))
        self.Packet.append(TrackAge.to_bytes(2, 'big', signed=False))
        self.Packet.append(TrackHitCount.to_bytes(2, 'big', signed=False))
        self.Packet.append(Identity1.to_bytes(4, 'big', signed=False))
        self.Packet.append(ConfidenceLevel1.to_bytes(1, 'big', signed=False))
        self.Packet.append(Identity2.to_bytes(4, 'big', signed=False))
        self.Packet.append(ConfidenceLevel2.to_bytes(1, 'big', signed=False))
        self.Packet.append(Identity3.to_bytes(4, 'big', signed=False))
        self.Packet.append(ConfidenceLevel3.to_bytes(1, 'big', signed=False))
        self.Packet.append(Identity4.to_bytes(4, 'big', signed=False))
        self.Packet.append(ConfidenceLevel4.to_bytes(1, 'big', signed=False))
        self.Packet.append(Identity5.to_bytes(4, 'big', signed=False))
        self.Packet.append(ConfidenceLevel5.to_bytes(1, 'big', signed=False))
        self.Packet.append(Reserved.to_bytes(1, 'big', signed=False))
        self.Packet.append(FreqMin.to_bytes(4, 'big', signed=False))
        self.Packet.append(FreqMax.to_bytes(4, 'big', signed=False))
        self.Packet.append(PWMin.to_bytes(4, 'big', signed=False))
        self.Packet.append(PWMax.to_bytes(4, 'big', signed=False))
        self.Packet.append(PGRI.to_bytes(4, 'big', signed=False))
        self.Packet.append(SpotPRFs.to_bytes(4, 'big', signed=False))
        self.Packet.append(SpotPWs.to_bytes(4, 'big', signed=False))
        self.Packet.append(SpotFreqencies.to_bytes(4, 'big', signed=False))
        self.Packet.append(DOAAccuracy.to_bytes(1, 'big', signed=False))
        self.Packet.append(PRI.to_bytes(4, 'big', signed=False))
        self.Packet.append(PRIMin.to_bytes(4, 'big', signed=False))
        self.Packet.append(PRIMax.to_bytes(4, 'big', signed=False))
        self.Packet.append(ANtennaScanRate.to_bytes(2, 'big', signed=False))
        self.Packet.append(TrackPDCount.to_bytes(4, 'big', signed=False))
        self.Packet.append(BinNumber.to_bytes(2, 'big', signed=False))
        self.Packet.append(BinType.to_bytes(1, 'big', signed=False))
        self.Packet.append(ProfileCount.to_bytes(2, 'big', signed=False))
        self.Packet.append(ProfileFreq.to_bytes(4, 'big', signed=False))
        self.Packet.append(ProfileAmp.to_bytes(1, 'big', signed=False))
        self.Packet.append(ProfilePW.to_bytes(2, 'big', signed=False))
        self.Packet.append(ProfilePRI.to_bytes(2, 'big', signed=False))
        self.Packet.append(footer.to_bytes(2, 'big', signed=False))

##########################################################################################################


        self.Packet = b"".join(self.Packet)
        print(self.Packet)

        #self.s.send(FP)

        #print(bytes(self.Packet))
        #self.s.send(bytes(str(self.Packet), 'utf-8'))

########################################################################################################################
if __name__ == "__main__":
    app = ESMP_ATE_Track_Data()
    app.TrackDataPacket(SM=int(PM1),Mscode=int(PM2),seqNo=int(PM3),msglen=int(PM4),TrackNo=1*1, TrackStatus=0, DOA=int(0*0.1), Frequency=int(50000*0.01), FreqAttributes=0, PW=5*10, PRF=50*1, PRIAttributes=0, Amplitude=-100*-1, ScanType=0,
                        AntennaScanPeriod=20*1, TOFA=250000*1, TOLA=250000*1, ActivityCount=0*1, TrackAge=20*1, TrackHitCount=1*1, Identity1=0*1, ConfidenceLevel1=0*1, Identity2=0*1, ConfidenceLevel2=0*1,
                        Identity3=0*1, ConfidenceLevel3=0*1, Identity4=0*1, ConfidenceLevel4=0*1, Identity5=0*1, ConfidenceLevel5=0*1, Reserved=0, FreqMin=int(50000*0.01), FreqMax=int(50000*0.01), PWMin=0*10, PWMax=0*10,
                        PGRI=0*10, SpotPRFs=50*1, SpotPWs=5*10, SpotFreqencies=int(50000*0.01), DOAAccuracy=0*1, PRI=1*1, PRIMin=1*1, PRIMax=1*1, ANtennaScanRate=int(50*0.001), TrackPDCount=1*1, BinNumber=1*1, BinType=1*1,
                        ProfileCount=1*1, ProfileFreq=int(50000*0.01), ProfileAmp=-90*-1, ProfilePW=2*20, ProfilePRI=1*1,footer=int(PM5))




