import sys

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QDialog, QApplication


from Testing.ATEtoESMP.ATE_to_ESMP_Cal_Start_Msg import ATE_ESMP_CAL_Start_MSG
from Testing.ATEtoESMP.ATE_to_ESMP_Cal_Stop_Msg import ATE_ESMP_CAL_Stop_MSG
from Testing.ATEtoESMP.ATE_to_ESMP_DirectMode_Msg import ATE_ESMP_Direct_Mode_MSG
from Testing.ATEtoESMP.ATE_to_ESMP_DataCal_External import ATE_ESMP_DataCal_External_Mode_MSG
from Testing.ATEtoESMP.ATE_to_ESMP_DataCal_Internal import ATE_ESMP_DataCal_Internal_Mode_MSG
from Testing.ATEtoESMP.ATE_to_ESMP_Noise_Cal import ATE_ESMP_Noise_Calib_Mode
from Testing.ATEtoESMP.ATE_to_ESMP_PDW_Logging import ATE_ESMP_PDW_Logging
from Testing.ATEtoESMP.ATE_to_ESMP_Start_WarnerRx_Cal import ATE_ESMP_Start_WarnerRx_Cal_MSG
from Testing.ATEtoESMP.ATE_to_ESMP_Stop_WarnerRx_Cal import ATE_ESMP_Stop_WarnerRx_Cal_MSG
from Testing.ATEtoESMP.ATE_to_ESMP_Restart import ATE_ESMP_Restart_MSG
from Testing.ATEtoESMP.ATE_to_ESMP_ACK_NACK_MSG import ATE_ESMP_ACK_NACK_MSG

from Testing.EsmpMsgClient import Ui_msg_dialog

class MsgDlg(QDialog,Ui_msg_dialog):
    def __init__(self,parent = None):
        super().__init__(parent)

        self.setupUi(self)


        self.Startcalib=ATE_ESMP_CAL_Start_MSG()
        self.Stopcalib = ATE_ESMP_CAL_Stop_MSG()
        self.directMode = ATE_ESMP_Direct_Mode_MSG()
        self.externalMode = ATE_ESMP_DataCal_External_Mode_MSG()
        self.internalmode=ATE_ESMP_DataCal_Internal_Mode_MSG()
        self.noisecalib=ATE_ESMP_Noise_Calib_Mode()
        self.pdwlog=ATE_ESMP_PDW_Logging()
        self.start_warner=ATE_ESMP_Start_WarnerRx_Cal_MSG()
        self.stop_warner=ATE_ESMP_Stop_WarnerRx_Cal_MSG()
        self.restart=ATE_ESMP_Restart_MSG()
        self.ack_nack=ATE_ESMP_ACK_NACK_MSG()

        self.CB_msg_sel.currentTextChanged.connect(self.MsgSel)

        self.CB_direct_RB.currentIndexChanged.connect(self.DirSel)
        self.CB_internal_RB.currentIndexChanged.connect(self.InternalSel)
        self.CB_external_RB.currentIndexChanged.connect(self.ExternalSel)
        self.CB_noise_RB.currentIndexChanged.connect(self.NoiseSel)

        self.CB_Direct_Sector.addItems(["All Sectors", "0-60°", "60-120°", "120-180°", "180-240°", "240-300°", "300-360°"])
        self.CB_external_Sector.addItems(["All Sectors", "0-60°", "60-120°", "120-180°", "180-240°", "240-300°", "300-360°"])
        self.CB_Internal_Sector.addItems(["All Sectors", "0-60°", "60-120°", "120-180°", "180-240°", "240-300°", "300-360°"])
        self.CB_noise_Sector.addItems(["All Sectors", "0-60°", "60-120°", "120-180°", "180-240°", "240-300°", "300-360°"])

        self.frame_direct_mode.setVisible(False)
        self.frame_external.setVisible(False)
        self.frame_calib_internal.setVisible(False)
        self.frame_noise_calib.setVisible(False)
        self.frame_pdw.setVisible(False)
        self.frame_ack_nack.setVisible(False)
        self.frame_response.setVisible(True)

        self.PB_Send.clicked.connect(self.Send)

########################################################################################################################
    def DirSel(self):
        if self.CB_direct_RB.currentIndex()==0:
            self.CB_Direct_Sector.clear()
            self.CB_Direct_Sector.addItems(["All Sectors","0-60°","60-120°","120-180°","180-240°","240-300°","300-360°"])

        elif self.CB_direct_RB.currentIndex()==2:
            self.CB_Direct_Sector.clear()
            self.CB_Direct_Sector.addItems(["All Sectors","0-60°","60-120°","120-180°","180-240°","240-300°","300-360°"])

        elif self.CB_direct_RB.currentIndex()==1:
            self.CB_Direct_Sector.clear()
            self.CB_Direct_Sector.addItems(["All Sectors","0-90°","90-180°","180-270°","270-360°"])

    def ExternalSel(self):
        if self.CB_external_RB.currentIndex()==0:
            self.CB_external_Sector.clear()
            self.CB_external_Sector.addItems(["All Sectors","0-60°","60-120°","120-180°","180-240°","240-300°","300-360°"])

        elif self.CB_external_RB.currentIndex()==2:
            self.CB_external_Sector.clear()
            self.CB_external_Sector.addItems(["All Sectors","0-60°","60-120°","120-180°","180-240°","240-300°","300-360°"])

        elif self.CB_external_RB.currentIndex()==1:
            self.CB_external_Sector.clear()
            self.CB_external_Sector.addItems(["All Sectors","0-90°","90-180°","180-270°","270-360°"])
    def InternalSel(self):

        if self.CB_internal_RB.currentIndex()==0:
            self.CB_Internal_Sector.clear()
            self.CB_Internal_Sector.addItems(["All Sectors", "0-60°", "60-120°", "120-180°", "180-240°", "240-300°", "300-360°"])

        elif self.CB_internal_RB.currentIndex()==2:
            self.CB_Internal_Sector.clear()
            self.CB_Internal_Sector.addItems(["All Sectors", "0-60°", "60-120°", "120-180°", "180-240°", "240-300°", "300-360°"])

        elif self.CB_internal_RB.currentIndex()==1:
            self.CB_Internal_Sector.clear()
            self.CB_Internal_Sector.addItems(["All Sectors", "0-90°", "90-180°", "180-270°", "270-360°"])

    def NoiseSel(self):

        if self.CB_noise_RB.currentIndex()==0:
            self.CB_noise_Sector.clear()
            self.CB_noise_Sector.addItems(["All Sectors", "0-60°", "60-120°", "120-180°", "180-240°", "240-300°", "300-360°"])

        elif self.CB_noise_RB.currentIndex()==2:
            self.CB_noise_Sector.clear()
            self.CB_noise_Sector.addItems(["All Sectors", "0-60°", "60-120°", "120-180°", "180-240°", "240-300°", "300-360°"])

        elif self.CB_noise_RB.currentIndex()==1:
            self.CB_noise_Sector.clear()
            self.CB_noise_Sector.addItems(["All Sectors", "0-90°", "90-180°", "180-270°", "270-360°"])

    """def PdwSel(self):

        if self.CB_noise_RB.currentIndex()==0:
            self.CB_pdw_Sector.clear()
            self.CB_pdw_Sector.addItems(["All Sectors", "0-60°", "60-120°", "120-180°", "180-240°", "240-300°", "300-360°"])

        elif self.CB_noise_RB.currentIndex()==2:
            self.CB_pdw_Sector.clear()
            self.CB_pdw_Sector.addItems(["All Sectors", "0-60°", "60-120°", "120-180°", "180-240°", "240-300°", "300-360°"])

        elif self.CB_noise_RB.currentIndex()==1:
            self.CB_pdw_Sector.clear()
            self.CB_pdw_Sector.addItems(["All Sectors", "0-90°", "90-180°", "180-270°", "270-360°"])"""

########################################################################################################################
    def MsgSel(self):

        if self.CB_msg_sel.currentText() == "ATE_TO_ESMP_CAL_START":
            print("ATE_TO_ESMP_CAL_START")
            self.frame_direct_mode.setVisible(False)
            self.frame_external.setVisible(False)
            self.frame_calib_internal.setVisible(False)
            self.frame_noise_calib.setVisible(False)
            self.frame_pdw.setVisible(False)
            self.frame_ack_nack.setVisible(False)
            self.frame_response.setVisible(True)

        elif self.CB_msg_sel.currentText() == "ATE_TO_ESMP_CAL_STOP":
            print("ATE_TO_ESMP_CAL_STOP")
            self.frame_direct_mode.setVisible(False)
            self.frame_external.setVisible(False)
            self.frame_calib_internal.setVisible(False)
            self.frame_noise_calib.setVisible(False)
            self.frame_pdw.setVisible(False)
            self.frame_ack_nack.setVisible(False)
            self.frame_response.setVisible(True)

        elif self.CB_msg_sel.currentText()=="ATE_TO_ESMP_DIRECTED_MODE":

            print("ATE_TO_ESMP_DIRECTED_MODE")
            self.frame_direct_mode.setVisible(True)
            self.frame_external.setVisible(False)
            self.frame_calib_internal.setVisible(False)
            self.frame_noise_calib.setVisible(False)
            self.frame_pdw.setVisible(False)
            self.frame_ack_nack.setVisible(False)
            self.frame_response.setVisible(True)

        elif self.CB_msg_sel.currentText()=="ATE_TO_ESMP_DATA_CALIB_EXTERNAL":
            print("ATE_TO_ESMP_DATA_CALIB_EXTERNAL")
            self.frame_external.setVisible(True)
            self.frame_external.setGeometry(QRect(10, 115, 455, 235))
            self.frame_direct_mode.setVisible(False)
            self.frame_calib_internal.setVisible(False)
            self.frame_noise_calib.setVisible(False)
            self.frame_pdw.setVisible(False)
            self.frame_ack_nack.setVisible(False)
            self.frame_response.setVisible(True)

        elif self.CB_msg_sel.currentText()=="ATE_TO_ESMP_DATA_CALIB_INTERNAL":
            print("ATE_TO_ESMP_DATA_CALIB_INTERNAL")

            self.frame_calib_internal.setVisible(True)
            self.frame_calib_internal.setGeometry(QRect(10, 115, 455, 235))
            self.frame_direct_mode.setVisible(False)
            self.frame_external.setVisible(False)
            self.frame_noise_calib.setVisible(False)
            self.frame_pdw.setVisible(False)
            self.frame_ack_nack.setVisible(False)
            self.frame_response.setVisible(True)

        elif self.CB_msg_sel.currentText()=="ATE_TO_ESMP_NOISE_CALIB":
            print("ATE_TO_ESMP_NOISE_CALIB")

            self.frame_noise_calib.setVisible(True)
            self.frame_noise_calib.setGeometry(QRect(10, 115, 455, 235))
            self.frame_direct_mode.setVisible(False)
            self.frame_external.setVisible(False)
            self.frame_calib_internal.setVisible(False)
            self.frame_pdw.setVisible(False)
            self.frame_ack_nack.setVisible(False)
            self.frame_response.setVisible(True)

        elif self.CB_msg_sel.currentText()=="ATE_TO_ESMP_PDW_LOG":
            print("ATE_TO_ESMP_PDW_LOG")
            self.frame_pdw.setVisible(True)
            self.frame_pdw.setGeometry(QRect(10, 115, 455, 235))
            self.frame_direct_mode.setVisible(False)
            self.frame_external.setVisible(False)
            self.frame_calib_internal.setVisible(False)
            self.frame_noise_calib.setVisible(False)
            self.frame_ack_nack.setVisible(False)
            self.frame_response.setVisible(True)

        elif self.CB_msg_sel.currentText()=="ATE_TO_ESMP_START_WARNERRX_CAL":
            print("ATE_TO_ESMP_START_WARNERRX_CAL")
            self.frame_direct_mode.setVisible(False)
            self.frame_external.setVisible(False)
            self.frame_calib_internal.setVisible(False)
            self.frame_noise_calib.setVisible(False)
            self.frame_pdw.setVisible(False)
            self.frame_ack_nack.setVisible(False)
            self.frame_response.setVisible(True)

        elif self.CB_msg_sel.currentText()=="ATE_TO_ESMP_STOP_WARNERRX_CAL":
            print("ATE_TO_ESMP_STOP_WARNERRX_CAL")
            self.frame_direct_mode.setVisible(False)
            self.frame_external.setVisible(False)
            self.frame_calib_internal.setVisible(False)
            self.frame_noise_calib.setVisible(False)
            self.frame_pdw.setVisible(False)
            self.frame_ack_nack.setVisible(False)
            self.frame_response.setVisible(True)

        elif self.CB_msg_sel.currentText()=="ATE_TO_ESMP_RESTART":
            print("ATE_TO_ESMP_RESTART")
            self.frame_direct_mode.setVisible(False)
            self.frame_external.setVisible(False)
            self.frame_calib_internal.setVisible(False)
            self.frame_noise_calib.setVisible(False)
            self.frame_pdw.setVisible(False)
            self.frame_ack_nack.setVisible(False)
            self.frame_response.setVisible(True)

        elif self.CB_msg_sel.currentText()=="ATE_TO_ESMP_ACK_NACK":
            print("ATE_TO_ESMP_ACK_NACK")
            self.frame_ack_nack.setVisible(True)
            self.frame_ack_nack.setGeometry(QRect(10, 115, 455, 235))
            self.frame_direct_mode.setVisible(False)
            self.frame_external.setVisible(False)
            self.frame_calib_internal.setVisible(False)
            self.frame_noise_calib.setVisible(False)
            self.frame_pdw.setVisible(False)
            self.frame_response.setVisible(True)

########################################################################################################################
    def Send(self):
        self.textEdit_cmd.clear()
        # Direct Mode variables get from GUI
        ReceiverBand=int(self.CB_direct_RB.currentIndex())
        CenterFrequency=int(self.lineEdit_direct_CF.text())
        RFAttenuation1=int(self.lineEdit_direct_RF1.text())
        RFAttenuation2 = int(self.lineEdit_direct_RF2.text())
        RFAttenuation3 = int(self.lineEdit_direct_RF3.text())
        RFAttenuation4 = int(self.lineEdit_direct_RF4.text())
        RFAttenuation5 = int(self.lineEdit_direct_RF5.text())
        RFAttenuation6 = int(self.lineEdit_direct_RF6.text())
        IFAttenuation1=int(self.lineEdit_direct_IF1.text())
        IFAttenuation2 = int(self.lineEdit_direct_IF2.text())
        IFAttenuation3 = int(self.lineEdit_direct_IF3.text())
        IFAttenuation4 = int(self.lineEdit_direct_IF4.text())
        IFAttenuation5 = int(self.lineEdit_direct_IF5.text())
        IFAttenuation6 = int(self.lineEdit_direct_IF6.text())
        Threshold=int(self.lineEdit_direct_thrs.text())
        IFBandwidthSelection=int(self.lineEdit_direct_IFBWS.text())
        SectorSelectionValue=int(self.CB_Direct_Sector.currentIndex())

        #External Calib
        RB_External = int(self.CB_external_RB.currentIndex())
        CF_External = int(self.lineEdit_external_CF.text())
        RF1_External = int(self.lineEdit_external_RF1.text())
        RF2_External = int(self.lineEdit_external_RF2.text())
        RF3_External = int(self.lineEdit_external_RF3.text())
        RF4_External = int(self.lineEdit_external_RF4.text())
        RF5_External = int(self.lineEdit_external_RF5.text())
        RF6_External = int(self.lineEdit_external_RF6.text())
        IF1_External = int(self.lineEdit_external_IF1.text())
        IF2_External = int(self.lineEdit_external_IF2.text())
        IF3_External = int(self.lineEdit_external_IF3.text())
        IF4_External = int(self.lineEdit_external_IF4.text())
        IF5_External = int(self.lineEdit_external_IF5.text())
        IF6_External = int(self.lineEdit_external_IF6.text())
        Thrs_External = int(self.lineEdit_external_thrs.text())
        IFBS_External = int(self.lineEdit_external_IFBWS.text())
        SecSel_External = int(self.CB_external_Sector.currentIndex())

        # Internal Calib
        RB_Internal = int(self.CB_internal_RB.currentIndex())
        BiteFreq_Internal = int(self.lineEdit_internal_biteFreq.text())
        TuningFreq_Internal=int(self.lineEdit_internal_tun_freq.text())
        sigtype_internal=int(self.CB_internal_Sig_Type.currentIndex())
        pw_internal=int(self.lineEdit_internal_pw.text())
        pri_internal=int(self.lineEdit_internal_pri.text())
        Thrs_Internal = int(self.lineEdit_internal_thrs.text())
        IFBWS_Internal = int(self.lineEdit_internal_IFBWS.text())
        RF1_Internal = int(self.lineEdit_internal_RF1.text())
        RF2_Internal = int(self.lineEdit_internal_RF2.text())
        RF3_Internal = int(self.lineEdit_internal_RF3.text())
        RF4_Internal = int(self.lineEdit_internal_RF4.text())
        RF5_Internal = int(self.lineEdit_internal_RF5.text())
        RF6_Internal = int(self.lineEdit_internal_RF6.text())
        IF1_Internal = int(self.lineEdit_internal_IF1.text())
        IF2_Internal = int(self.lineEdit_internal_IF2.text())
        IF3_Internal = int(self.lineEdit_internal_IF3.text())
        IF4_Internal = int(self.lineEdit_internal_IF4.text())
        IF5_Internal = int(self.lineEdit_internal_IF5.text())
        IF6_Internal = int(self.lineEdit_internal_IF6.text())
        SecSel_Internal = int(self.CB_Internal_Sector.currentIndex())

        # Noise Calib
        RB_noise=int(self.CB_noise_RB.currentIndex())
        CF_noise=int(self.lineEdit_noise_CF.text())
        Thrs_noise=int(self.lineEdit_noise_Thrs.text())
        IFBWS_noise=int(self.lineEdit_noise_IFBWS.text())
        SecSel_noise=int(self.CB_noise_Sector.currentIndex())

        # PDW Logging
        Action_pdw=int(self.CB_pdw_action.currentIndex())
        SecSel_pdw=int(self.CB_pdw_Sector.currentIndex())

        # ACK-NACK
        MsgCode_ack=int(self.lineEdit_msgcode_ack.text())
        SeqNo_ack=int(self.lineEdit_seqno_ack.text())
        Status_ack=int(self.lineEdit_status_ack.text())

        if self.CB_msg_sel.currentText() == "ATE_TO_ESMP_CAL_START":
            self.Startcalib.Packet.clear()
            self.Startcalib.StartCalPacket(SM=0xAAAA, Mscode=5001, seqNo=1, msglen=5,footer=0xEEEE)

            self.textEdit_cmd.setText(str(self.Startcalib.Packet))

        elif self.CB_msg_sel.currentText() == "ATE_TO_ESMP_CAL_STOP":
            self.Stopcalib.Packet.clear()
            self.Stopcalib.StopCalPacket(SM=0xAAAA, Mscode=5002, seqNo=1, msglen=5, footer=0xEEEE)

            self.textEdit_cmd.setText(str( self.Stopcalib.Packet))

        elif self.CB_msg_sel.currentText() == "ATE_TO_ESMP_DIRECTED_MODE":
            self.directMode.Packet.clear()
            self.directMode.DirectedModePacket(SM=0xAAAA,Mscode=5003,seqNo=1,msglen=22,RB=ReceiverBand//1, CF=CenterFrequency//1, RFATT1=RFAttenuation1//2, RFATT2=RFAttenuation2//2, RFATT3=RFAttenuation3//2, RFATT4=RFAttenuation4//2,
                           RFATT5=RFAttenuation5//2, RFATT6=RFAttenuation6//2, IFATTN1=IFAttenuation1//2, IFATTN2=IFAttenuation2//2, IFATTN3=IFAttenuation3//2,
                           IFATTN4=IFAttenuation4//2, IFATTN5=IFAttenuation5//2, IFATTN6=IFAttenuation6//2, THRS= -Threshold//-1, IFBWS=IFBandwidthSelection//1, SSV=SectorSelectionValue//1,footer=0xEEEE)

            self.textEdit_cmd.setText(str(self.directMode.Packet))

        elif self.CB_msg_sel.currentText()=="ATE_TO_ESMP_DATA_CALIB_EXTERNAL":
            self.externalMode.Packet.clear()
            self.externalMode.DataCalExternalModePacket(SM=0xAAAA,Mscode=5004,seqNo=1,msglen=22,RB=RB_External//1, CF=CF_External//1, RFATT1=RF1_External//2, RFATT2=RF2_External//2, RFATT3=RF3_External//2, RFATT4=RF4_External//2,
                           RFATT5=RF5_External//2, RFATT6=RF6_External//2, IFATTN1=IF1_External//2, IFATTN2=IF2_External//2, IFATTN3=IF3_External//2,
                           IFATTN4=IF4_External//2, IFATTN5=IF5_External//2, IFATTN6=IF6_External//2, THRS=-Thrs_External//-1, IFBWS=IFBS_External//1, SSV=SecSel_External//1,footer=0xEEEE)

            self.textEdit_cmd.setText(str(self.externalMode.Packet))

        elif self.CB_msg_sel.currentText() == "ATE_TO_ESMP_DATA_CALIB_INTERNAL":
            self.internalmode.Packet.clear()
            self.internalmode.DataCalInternalModePacket(SM=0xAAAA,Mscode=5005,seqNo=1,msglen=27,RB=RB_Internal//1, BFreq=int(BiteFreq_Internal//0.01), TFreq=TuningFreq_Internal//10, SigType=sigtype_internal//1, PW=pw_internal//10, PRI=pri_internal//1,
                                  THRS=-Thrs_Internal//-1, IFBWS=IFBWS_Internal//1, SECSel=SecSel_Internal//1, RFATT1=RF1_Internal//2, RFATT2=RF2_Internal//2, RFATT3=RF3_Internal//2, RFATT4=RF4_Internal//2,
                                   RFATT5=RF5_Internal//2, RFATT6=RF6_Internal//2, IFATTN1=IF1_Internal//2, IFATTN2=IF2_Internal//2, IFATTN3=IF3_Internal//2,
                                    IFATTN4=IF4_Internal//2, IFATTN5=IF5_Internal//2, IFATTN6=IF6_Internal//2, SSV=0//1,footer=0xEEEE)

            self.textEdit_cmd.setText(str(self.internalmode.Packet))

        elif self.CB_msg_sel.currentText()=="ATE_TO_ESMP_NOISE_CALIB":
            self.noisecalib.Packet.clear()
            self.noisecalib.NoiseCalModePacket(SM=0xAAAA,Mscode=5006,seqNo=1,msglen=10,RB=RB_noise//1, CF=CF_noise//1, THRS=-Thrs_noise//-1, IFBWS=IFBWS_noise//1, SSV=SecSel_noise//1,footer=0xEEEE)
            self.textEdit_cmd.setText(str(self.noisecalib.Packet))

        elif self.CB_msg_sel.currentText() == "ATE_TO_ESMP_PDW_LOG":
            self.pdwlog.Packet.clear()
            self.pdwlog.PDWLoggingPacket(SM=0xAAAA,Mscode=5007,seqNo=1,msglen=7,Action=Action_pdw//1, SSV=SecSel_pdw//1,footer=0xEEEE)

            self.textEdit_cmd.setText(str(self.pdwlog.Packet))

        elif self.CB_msg_sel.currentText() == "ATE_TO_ESMP_START_WARNERRX_CAL":
            self.start_warner.Packet.clear()
            self.start_warner.StartWarnerPacket(SM=0xAAAA, Mscode=5008, seqNo=1, msglen=5, footer=0xEEEE)
            self.textEdit_cmd.setText(str(self.start_warner.Packet))

        elif self.CB_msg_sel.currentText() == "ATE_TO_ESMP_STOP_WARNERRX_CAL":
            self.stop_warner.Packet.clear()
            self.stop_warner.StopWarnerPacket(SM=0xAAAA, Mscode=5009, seqNo=1, msglen=5, footer=0xEEEE)

            self.textEdit_cmd.setText(str(self.stop_warner.Packet))

        elif self.CB_msg_sel.currentText() == "ATE_TO_ESMP_RESTART":
            self.restart.Packet.clear()
            self.restart.RestartPacket(SM=0xAAAA, Mscode=5010, seqNo=1, msglen=5, footer=0xEEEE)

            self.textEdit_cmd.setText(str(self.restart.Packet))

        elif self.CB_msg_sel.currentText() == "ATE_TO_ESMP_ACK_NACK":
            self.ack_nack.Packet.clear()
            self.ack_nack.ACK_NACKPacket(SM=0xAAAA,Mscode=5020,seqNo=1,msglen=8,MC=MsgCode_ack//1, SeqNum=SeqNo_ack//1, ACKStatus=Status_ack//1,footer=0xEEEE)
            self.textEdit_cmd.setText(str(self.ack_nack.Packet))
########################################################################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main =MsgDlg()
    main.show()
    sys.exit(app.exec_())
