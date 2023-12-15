import os
import socket,json

class ScannerNester:

    def MakeScanWithHarvester(ip_harvester):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_harvester, 9999))

        print("Connexion à "+ip_harvester+" réussie.")
        s.send(bytes("MakeScan", "utf-8")) #bytes ou .encode()

        data = eval(s.recv(9999).decode("utf8")) #eval sert à convertir en dict
        print(data)

        s.close()
        return data






    
