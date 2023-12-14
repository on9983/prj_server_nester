import os
import socket,json

class ScannerNester:

    def MakeScanWithHarvester(port_harvester):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("192.168.15.18", int(port_harvester)))
        s.listen(5)
        while True:

            HVR, address = s.accept()
            print("Connexion à "+str(address)+" réussie.")
            HVR.send(bytes("MakeScan", "utf-8")) #bytes ou .encode()
            


            data = HVR.recv(55300).decode("utf8")
            print(data)

            HVR.close()
            break

        s.close()
        return data






    
