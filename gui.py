from tkinter import *
from tkinter import ttk
from ScannerNesterByIp import ScannerNester
import DataSaver
from threading import Event
import threading
import nmap3, socket


nmap = nmap3.Nmap()

event = Event()
data = {}
sondeSelected = None

# HVR01 = {
#     "nom":"HVR01",
#     "port":"1519"
# }
harvesters = {
    "HVR01" : {
        "nom":"HVR01",
        "ip":"192.168.15.19"
    },
    "HVR02" : {
        "nom":"HVR02",
        "ip":"192.168.15.22"
    }
}


def chainHVRScan():
    
    progressbar.start()
    data={}
    listboxListHVR.delete(0,END)

    
    nmapResult = nmap.scan_top_ports(socket.gethostbyname(socket.gethostname()+".local") + "/24")
    contacts = {}
    j=0
    for ip,data_ip in nmapResult.items():
        if('ports' in data_ip):
            if(data_ip["ports"] != []):
                contacts[j] = ip
                j+=1

    # print(contacts)

    for contact_ip in contacts.values():
        global event
        if event.is_set():
            event.clear()
            progressbar.stop()
            break
        try:
            print("1")
            data[contact_ip] = ScannerNester.MakeScanWithHarvester(contact_ip)
            print("2")
            DataSaver.saveScanJson("scanData",data)
            print("3")
            listboxListHVR.insert("end",contact_ip)
            print("4")
        except:
            pass
    # if data !={}:
    #     DataSaver.saveScanJson("scanData",data)


def chainHVRTrouverScan():
    data={}
    progressbar2.start()
    try:
        data_load= DataSaver.loadScanJson("scanData")
        for ip in list(data_load):
            global event
            if event.is_set():
                event.clear()
                progressbar2.stop()
                break
            try:
                data = ScannerNester.MakeScanWithHarvester(ip)
                data_load[ip] = data 
            except:
                pass
        DataSaver.saveScanJson("scanData",data_load)
    except: 
        pass


def HVRSelectedScan():
    global sondeSelected
    progressbar3.start()
    try:
        data_load = DataSaver.loadScanJson("scanData")
        data = ScannerNester.MakeScanWithHarvester(sondeSelected)

        data_load[sondeSelected] = data 

        DataSaver.saveScanJson("scanData",data_load)
    except: 
        pass





def submit():
    chainHVRScan()

def start_submit_thread(targetFunction):
    global submit_thread
    submit_thread = threading.Thread(target=targetFunction) #, args=(event,))
    submit_thread.daemon = True
    # progressbar.start()
    submit_thread.start()
    gui.after(20, check_submit_thread)

def check_submit_thread():
    if submit_thread.is_alive():
        gui.after(20, check_submit_thread)
    else:
        progressbar.stop()
        progressbar2.stop()
        progressbar3.stop()

def stopChainHVRScan():
    global event
    event.set()


def onselectHVR(event):
    global sondeSelected
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        strSelected = event.widget.get(index)
        sondeSelected = strSelected

        data = DataSaver.loadScanJson("scanData")
        data = data[strSelected]
        L22.configure(text=str(data["hostName"]))#list(data.keys())[0])
        L24.configure(text=strSelected)
        L26.configure(text=str(data["nb_clients"]))
        L22.config(fg=mgrey)
        L24.config(fg=mgrey)
        L26.config(fg=mgrey)
        B31["state"] = "normal"
        
        listboxClients.delete(0,END)
        for ip in list(data):
            if ip !="nb_clients" and ip !="hostName":
                listboxClients.insert(END,ip)
                
    else:
        L22.configure(text="No probe selected")
        L24.configure(text="No probe selected")
        L26.configure(text="No probe selected")
        L22.config(fg=m1c_blk)
        L24.config(fg=m1c_blk)
        L26.config(fg=m1c_blk)
        B31["state"] = "disabled"
        listboxClients.delete(0,END)

def onselectClient(event):
    global sondeSelected
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        strSelected = event.widget.get(index)

        data = DataSaver.loadScanJson("scanData")
        data = data[sondeSelected]
        data = data[strSelected]
        data = data["ports"]
        # print(data)

        listboxPorts.delete(0,END)
        if data == {}:
            listboxPorts.insert(END,"Pas de ports ouverts trouvés.")
        else:
            for port in list(data):
                listboxPorts.insert(END,port)
    else:
        listboxClients.delete(0,END)

# ==== GUI ====
gui = Tk()
gui.title('Seaweak harvester')
gui.geometry("800x800+20+20")

gui_ypos = 220
gui_xpos = 400

# ==== Colors ====
m1c = '#00ee00'
m1c_blk = '#006400'
mgrey = '#999999'
bgc = '#222222'
dbg = '#000000'
fgc = '#111111'

gui.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc,activeForeground=bgc, highlightColor=m1c, highlightBackground=m1c)

stl = ttk.Style()
stl.theme_use('clam')
stl.configure("red.Horizontal.TProgressbar", background=bgc, troughcolor =bgc, bordercolor=m1c, lightcolor=m1c, darkcolor=m1c)

# ==== Chercheur d'harvester ====
L011 = Label(gui, text = "Chercheur de sondes",  font=("Helvetica", 16))
L011.place(x = 16, y = 20)

B011 = Button(gui, text = "Start Scan", command=lambda:start_submit_thread(chainHVRScan))
B011.place(x = 16, y = 50, width = 170)
B012 = Button(gui, text = "Stop Scan", command=lambda:stopChainHVRScan())
B012.place(x = 210, y = 50, width = 170)
progressbar = ttk.Progressbar(gui, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=60, mode='indeterminate')
progressbar.place(x = 72, y = 85)

# ==== Liste des sondes trouvés ====
L012 = Label(gui, text = "Liste des sondes trouvés :",  font=("Helvetica", 11))
L012.place(x = 80, y = 120)
frameListHVR = Frame(gui)
frameListHVR.place(x = 80, y = 140, width = 240, height = 309)
listboxListHVR = Listbox(frameListHVR, width = 240, height = 17, exportselection=False )
listboxListHVR.place(x = 0, y = 0)
listboxListHVR.bind('<<ListboxSelect>>', onselectHVR)
listboxListHVR.config(fg=mgrey)
try:
    prevList = DataSaver.loadScanJson("scanData")
    for ip in prevList.keys():
        listboxListHVR.insert(END,ip)
except: 
    pass
scrollbar = Scrollbar(frameListHVR)
scrollbar.pack(side=RIGHT, fill=Y)
listboxListHVR.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listboxListHVR.yview)


# ==== Lancer un scanne général ====
LSG_ypos = 230
L013 = Label(gui, text = "Lancer un scan réseaux",  font=("Helvetica", 16))
L013.place(x = 16, y = 280+LSG_ypos)
L014 = Text(gui, height=10, width=40, wrap=WORD, highlightthickness=0,borderwidth=0, font=("Helvetica", 9))
L014.insert(END, "Met à jours les informations des sondes trouvés.")
L014.place(x = 16, y = 310+LSG_ypos)
B11 = Button(gui, text = "Start Scan", command=lambda:start_submit_thread(chainHVRTrouverScan))
B11.place(x = 16, y = 336+LSG_ypos, width = 170)
progressbar2 = ttk.Progressbar(gui, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=60, mode='indeterminate')
progressbar2.place(x = 72, y = 370+LSG_ypos)
B21 = Button(gui, text = "Export All Result", command=lambda:DataSaver.saveScanJson("nofing",data))
B21.place(x = 210, y = 336+LSG_ypos, width = 170)
B21["state"] = "disabled"





# ==== Infos de l'harvester ====
L11 = Label(gui, text = "Infos sur la sonde sélectionnée",  font=("Helvetica", 16))
L11.place(x = 16 + gui_xpos, y = 20)

L21 = Label(gui, text = "Nom de la sonde : ")
L21.place(x = 16 + gui_xpos, y = 70)
L22 = Label(gui, text = "No probe selected")
L22.place(x = 180 + gui_xpos, y = 70)

L23 = Label(gui, text = "IP de la sonde : ")
L23.place(x = 16 + gui_xpos, y = 100)
L24 = Label(gui, text = "No probe selected")
L24.place(x = 180 + gui_xpos, y = 100)

L25 = Label(gui, text = "Nb de clients detectés : ")
L25.place(x = 16 + gui_xpos, y = 130)
L26 = Label(gui, text = "No probe selected")
L26.place(x = 180 + gui_xpos, y = 130)

L22.config(fg=m1c_blk)
L24.config(fg=m1c_blk)
L26.config(fg=m1c_blk)

B31 = Button(gui, text = "Refresh Scan", command=lambda:start_submit_thread(HVRSelectedScan))
B31.place(x = 64 + gui_xpos, y = 180, width = 170)
B31["state"] = "disabled"
progressbar3 = ttk.Progressbar(gui, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=60, mode='indeterminate')
progressbar3.place(x = 120 + gui_xpos, y = 214)

# ==== Liste des clients ====
L27 = Label(gui, text = "Liste des clients détectés :")
L27.place(x = 16 + gui_xpos, y = 240)
frame = Frame(gui)
frame.place(x = 16 + gui_xpos, y = 262, width = 370, height = 255)
listboxClients = Listbox(frame, width = 59, height = 14, exportselection=False)
listboxClients.place(x = 0, y = 0)
listboxClients.bind('<<ListboxSelect>>', onselectClient)
listboxClients.config(fg=mgrey)
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
listboxClients.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listboxClients.yview)

# ==== Ports list ====
L28 = Label(gui, text = "Liste des ports ouverts du client selectionné :")
L28.place(x = 16 + gui_xpos, y = 340 + gui_ypos)

frame = Frame(gui)
frame.place(x = 16 + gui_xpos, y = 362 + gui_ypos, width = 370, height = 165)
listboxPorts = Listbox(frame, width = 59, height = 9, exportselection=False )
listboxPorts.place(x = 0, y = 0)
listboxPorts.bind('<<ListboxSelect>>')
listboxPorts.config(fg=mgrey)
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
listboxPorts.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listboxPorts.yview)



# ==== Start GUI ====
gui.mainloop()
