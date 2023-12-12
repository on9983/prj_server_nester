import os
import socket,json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(("192.168.15.19", 9999))
# client.close()

checkCon_HVR01 = s.bind(("192.168.15.18", 55300))



s.listen(5)
while True:

    HVR01, address = s.accept()
    print("Connexion à "+str(address)+" réussie.")
    HVR01.send(bytes("MakeScan", "utf-8")) #bytes ou .encode()
    


    data = HVR01.recv(55300).decode("utf8")
    print(data)

    HVR01.close()
    break

s.close()






    
