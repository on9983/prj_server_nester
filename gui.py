from tkinter import *
from tkinter import ttk
from ScannerNesterByIp import ScannerNester
import DataScanSaver
import threading


data = {}
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
    for i in range(2,255,1):
        try:
            data = ScannerNester.MakeScanWithHarvester("192.168.15."+str(i))
            listbox.insert("end",data)
        except:
            i+=1
            i-=1


def submit():
    chainHVRScan()

def start_submit_thread(event):
    global submit_thread
    submit_thread = threading.Thread(target=submit)
    submit_thread.daemon = True
    progressbar.start()
    submit_thread.start()
    gui.after(20, check_submit_thread)

def check_submit_thread():
    if submit_thread.is_alive():
        gui.after(20, check_submit_thread)
    else:
        progressbar.stop()





# ==== GUI ====
gui = Tk()
gui.title('Port Scanner')
gui.geometry("400x800+20+20")

gui_ypos = 120

# ==== Colors ====
m1c = '#00ee00'
bgc = '#222222'
dbg = '#000000'
fgc = '#111111'

gui.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc,activeForeground=bgc, highlightColor=m1c, highlightBackground=m1c)


# ==== Chercheur d'harvester ====
L011 = Label(gui, text = "Chercheur d'harvester",  font=("Helvetica", 16))
L011.place(x = 16, y = 20)

B011 = Button(gui, text = "Start Scan", command=lambda:start_submit_thread(None))
B011.place(x = 16, y = 50, width = 170)
B012 = Button(gui, text = "Stop Scan", command=lambda:start_submit_thread(None))
B012.place(x = 210, y = 50, width = 170)
progressbar = ttk.Progressbar(gui, orient=HORIZONTAL, length=100, mode='indeterminate')
progressbar.place(x = 32, y = 85)


# ==== Labels ====
L11 = Label(gui, text = "Seahawks Harvester",  font=("Helvetica", 16))
L11.place(x = 16, y = 10 + gui_ypos)

L21 = Label(gui, text = "Nom du harvester : ")
L21.place(x = 16, y = 90 + gui_ypos)
L22 = Label(gui, text = "???")
L22.place(x = 180, y = 90 + gui_ypos)

L23 = Label(gui, text = "IP du harvester : ")
L23.place(x = 16, y = 120 + gui_ypos)
L23 = Label(gui, text = "???")
L23.place(x = 180, y = 120 + gui_ypos)

L24 = Label(gui, text = "Nb de clients detectés : ")
L24.place(x = 16, y = 150 + gui_ypos)
L25 = Label(gui, text = "???")
L25.place(x = 180, y = 150 + gui_ypos)

L26 = Label(gui, text = "Liste des connexions LAN ")
L26.place(x = 16, y = 240 + gui_ypos)


# ==== Ports list ====
frame = Frame(gui)
frame.place(x = 16, y = 275 + gui_ypos, width = 370, height = 215)
listbox = Listbox(frame, width = 59, height = 12 )
listbox.place(x = 0, y = 0)
listbox.bind('<<ListboxSelect>>')
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# ==== Buttons / Scans ====
B11 = Button(gui, text = "Start Scan", command=lambda:start_submit_thread(None))
B11.place(x = 16, y = 500 + gui_ypos, width = 170)
B21 = Button(gui, text = "Save Result", command=lambda:DataScanSaver.saveScanTxt(data))
B21.place(x = 210, y = 500 + gui_ypos, width = 170)

# ==== Start GUI ====
gui.mainloop()
