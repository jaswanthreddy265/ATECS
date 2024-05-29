import sys

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication

from EsmpTrackData import Ui_ESMP_ATE
from Testing.ESMPtoATE.ESMP_to_ATE_Track_Data import ESMP_ATE_Track_Data


########################################################################################################################
class ESMPDlg(QDialog,Ui_ESMP_ATE):
    def __init__(self):
        super(ESMPDlg,self).__init__()
        self.setupUi(self)

        self.trackdata=ESMP_ATE_Track_Data()
        self.df = pd.read_csv('C:/Users/jaswa/PycharmProjects/ATEC/Testing/ESMPtoATE/ATE_to_System_Msg_Format.csv')

        self.PM1 = self.df.loc[(self.df['cmd_id'] == 'SM'), 'cmd_code'].values[0]
        self.PM2 = self.df.loc[(self.df['cmd_id'] == 'ESMP_ATE_Track_Data_Mscode'), 'cmd_code'].values[0]
        self.PM3 = self.df.loc[(self.df['cmd_id'] == 'seqNo'), 'cmd_code'].values[0]
        self.PM4 = self.df.loc[(self.df['cmd_id'] == 'ESMP_ATE_Track_Data_msglen'), 'cmd_code'].values[0]
        self.PM5 = self.df.loc[(self.df['cmd_id'] == 'footer'), 'cmd_code'].values[0]

        self.PB_Send.clicked.connect(self.SendCmd)

########################################################################################################################
    def SendCmd(self):

        trackno=int(self.lineEdit_Track_No.text())
        trackstatus=int(self.CB_Track_Status.currentIndex())
        doa=int(self.lineEdit_DOA.text())
        freq=int(self.lineEdit_Freq.text())
        Freq_Attr=int(self.CB_Sig_Type.currentIndex())
        pw=int(self.lineEdit_PW.text())
        prf=int(self.lineEdit_PRF.text())
        Pri_Attr=int(self.CB_PRI_Type.currentIndex())
        Ampl=int(self.lineEdit_Amp.text())
        scantype=int(self.CB_ScanType.currentIndex())
        Anntenna_Scan=int(self.lineEdit_Anntenna_Scan.text())
        tofa=int(self.lineEdit_TOFA.text())
        tola=int(self.lineEdit_TOLA.text())

        self.trackdata.TrackDataPacket(SM=int(self.PM1),Mscode=int(self.PM2),seqNo=int(self.PM3),msglen=int(self.PM4),TrackNo=trackno,TrackStatus=trackstatus,DOA=doa,Frequency=freq,
                                       FreqAttributes=Freq_Attr,PW=pw,PRF=prf,PRIAttributes=Pri_Attr,Amplitude=Ampl,ScanType=scantype,AntennaScanPeriod=Anntenna_Scan,TOFA=tofa,
                                       TOLA=tola,ActivityCount=0,TrackAge=20,TrackHitCount=1,Identity1=0,ConfidenceLevel1=0,Identity2=0,ConfidenceLevel2=0,Identity3=0,
                                       ConfidenceLevel3=0,Identity4=0,ConfidenceLevel4=0,Identity5=0,ConfidenceLevel5=0,Reserved=0,FreqMin=50000,FreqMax=50000,PWMin=0,
                                       PWMax=0,PGRI=0,SpotPRFs=50,SpotPWs=5,SpotFreqencies=50000,DOAAccuracy=0,PRI=1,PRIMin=1,PRIMax=1,ANtennaScanRate=50,TrackPDCount=1,
                                       BinNumber=1,BinType=1,ProfileCount=1,ProfileFreq=50000,ProfileAmp=90,ProfilePW=2,ProfilePRI=1,footer=int(self.PM5))

        self.textEdit_cmd.setText(str(self.trackdata.Packet))


########################################################################################################################
if __name__=="__main__":
    app=QApplication(sys.argv)
    win=ESMPDlg()
    win.show()
    sys.exit(app.exec_())