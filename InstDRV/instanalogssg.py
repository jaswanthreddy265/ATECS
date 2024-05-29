import pyvisa

rm = pyvisa.ResourceManager()
print(rm.list_resources())
#rm.open_resource(rm.list_resources()[0])
class InstDrv():
    def __init__(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        self.Ssg = rm.open_resource("SSG")
    def Reset(self):
        self.Ssg.write("*RST")

    def GetID(self):
        self.Ssg.query('*IDN?')


