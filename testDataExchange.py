import os
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(("192.168.15.19", 9999))
# client.close()

checkCon_HVR01 = s.bind(("192.168.15.18", 55300)) #4286 est le mdp de la con
print(socket.gethostname())
s.listen(5) #envoie le bind 5 fois
while True:
    HVR01, address = s.accept()
    print("Connexion à "+str(address)+" réussie.")
    HVR01.send(bytes("Bienvenue à Roubaix", "utf-8")) #bytes ou .encode()
    HVR01.close()
    


