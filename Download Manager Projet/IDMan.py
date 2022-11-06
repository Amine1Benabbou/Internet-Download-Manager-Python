
from msilib.schema import Media
from operator import truediv
import PySimpleGUI as gui
import requests
import time
import winsound
import threading
import speedtest
import platform
import multiprocessing
import psutil
import os
my_system = platform.uname()

wifi  = speedtest.Speedtest()

dirname = os.path.dirname("C:/Users/AMINE/Documents/GitHub/")
relp="./Internet-Download-Manager-Project-Python/Download Manager Projet/IDM"
fullpath= os.path.join(dirname, relp)

#-------------------------------------------------------------------------------------------------------------------------------
def get_size(url):
    response = requests.head(url)
    size = int(response.headers['Content-Length'])
    return size
#-------------------------------------------------------------------------------------------------------------------------------
def download(urlin,urlout,nb):
        
        liste=urlin.split('/')
        
        urlout+='/'+liste[len(liste)-1]

        size=get_size(urlin)
        partsize=size//nb
        if size%nb!=0:
            nb+=1
        start=0
        end=partsize
        i=int(1)
        print(partsize)
        listeth=[]
        while i<=nb:
            threadpart=threading.Thread(target=downloadpart,args=(urlin,i,start,end,urlout,))
            listeth.append(threadpart)
            threadpart.start()  
            i+=1
            start=end+1
            end=end+partsize

        for i in range(0,nb):
            listeth[i].join()
        print("All threads finished")
        
        f=open(urlout,"wb")
        i=int(1)
        while i<=nb:
            g=open(urlout+f'.part{i}','rb')
            f.write(g.read())
            g.close()
            os.remove(urlout+f'.part{i}')
            i+=1
        f.close()
        
        
def downloadpart(urlin,i,start,end,urlout):
    f=open(urlout+f'.part{i}', "wb")          
    result = requests.get(urlin,headers={'Range':f'bytes={start}-{end}'})
    f.write(result.content)
    f.close()
        

#------------------------------------------------------------------------------------------------------------------------
def form2():
    
    layout =[
            [gui.Text("Add a URL to Download: ")],
            [gui.InputText(key='url'),gui.Button("OK")],
            [gui.Text("Size of file:",key="status")],
            [gui.Text("Type Number of Threads: "),
             gui.InputText(key='nb',size=(10,100)),gui.Button("Validate"),
             gui.Text("",key="nbs",text_color="lightgreen")],
            [gui.FolderBrowse("Choose Download Path",target="path"),gui.InputText(key="path")],
            [gui.Button("Start Download")],
            [gui.Text('Progress Meter:'),gui.Text(key='meter')],
            [gui.ProgressBar(100,key='pb',size=(100,10),bar_color=['blue','white'])]
            ]

    w = gui.Window(title="Download Manager",layout=layout,size=(840,250),location=(600,500)) 

    while True:
        
        event,values = w.read()
        if values is not None:
            urlin=values['url']
            urlout=values['path']
                 
    
        
        if event == gui.WIN_CLOSED:
            break  

        if event == "OK":

            info = requests.head(urlin)
            headers=info.headers
            if (info.status_code == 200):
                w['status'].update('Size of file: '+str(round(int(headers['Content-Length'])/1024,2))+" Ko")
            else:
                w['status'].update('File not found ')

        if event == "Validate":
            nb=int(values["nb"])
            w["nbs"].update('Validé')



        if event == "Start Download" :
            threaddownload=threading.Thread(target=download,args=(urlin,urlout,nb,)) 
            threaddownload.start()
            
            for val in range(99):       
                w['meter'].update(str(val+1)+'%')
                pbar=w['pb']
                pbar.UpdateBar(val+1)
                time.sleep(0.01)

            threaddownload.join()

            w['meter'].update(str(100)+'%')
            pbar.UpdateBar(100)
            winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
            w['meter'].update("Download successfull")  
            
        
    w.close()

#--------------------------------------------------------------------------------------------------------------------
def form3():

    def UP():
        ws['ups'].update(str(round(int(wifi.download())/1048576,2))+' Mb')

    def DOWN():
        ws['downs'].update(str(round(int(wifi.upload())/1048576,2))+' Mb')
        ws["init"].update('')
        
    clayout = [
                [gui.Text("Speed Test: ",text_color="RED")],
                [gui.Button("Start"),gui.Text("",key="init"),
                [gui.Text("Download Speed:",key='up'),
                 gui.Text("",key='ups',text_color="lightgreen")],
                [gui.Text("Upload Speed:",key='down'),
                 gui.Text("",key='downs',text_color="yellow")]]
            ]

    ws = gui.Window(title="Speed Test",layout=clayout,size=(300,130),location=(600,500))

    while True:
            threadup=threading.Thread(target=UP,args=())
            threaddown=threading.Thread(target=DOWN,args=())
                
            event,values = ws.read()

            if event == gui.WIN_CLOSED:
                break  
            if event == "Start":
                ws["init"].update("Loading...")
                threadup.start()
                threaddown.start()
                
                            

    ws.close()
#--------------------------------------------------------------------------------------------------------------------------
def form4():
    pclayout = [
                [gui.Text("PC Informations: ",text_color="LIGHTBLUE")],
                [gui.Text("System: "+str(my_system.system))],
                [gui.Text("Node name: "+str(my_system.node))],
                [gui.Text("Release: "+str(my_system.release))],
                [gui.Text("Version: "+str(my_system.version))],
                [gui.Text("Machine: "+str(my_system.machine))],
                [gui.Text("Processor: "+str(my_system.processor))],
                [gui.Text("Number of CPU cores: "+str(multiprocessing.cpu_count()),text_color="LIGHTGREEN")]
            ]

    wpc = gui.Window(title="PC info",layout=pclayout,size=(600,220),location=(600,500))

    while True:
                
        event,values = wpc.read()

        if event == gui.WIN_CLOSED:
            break  
#----------------------------------------------------------------------------------------------------------------------------
def form5():
    ramlayout = [
                [gui.Text("RAM usage: ",key="rams")],
                [gui.Text("CPU usage: ",key="cpu")],
                [gui.Button("Refresh")]
            ]

    wram = gui.Window(title="RAM and CPU usage",layout=ramlayout,size=(200,100),location=(600,500))

    while True:
                
        event,values = wram.read()

        if event == gui.WIN_CLOSED:
            break  
        if event == "Refresh":
            wram["rams"].update("RAM usage: "+str(psutil.virtual_memory()[2])+"%")
            wram["cpu"].update("CPU usage: "+str(psutil.cpu_percent(4))+"%")

#-------------------------------------------------------------------------------------------------------------------------------
def form6():
    infolayout = [
                 [gui.Text("Realisé par : Mohamed Amine BENABBOU",text_color="yellow")],
                 [gui.Text("Encadré par : Pr.Mohamed LAHMER",text_color="lightgreen")]
                 ]

    winfo = gui.Window(title="Credits",layout=infolayout,size=(370,70),location=(600,500))
    while True:
                
        event,values = winfo.read()

        if event == gui.WIN_CLOSED:
            break  

#-------------------------------------------------------------------------------------------------------------------------------
#main form
#----------------------------------------------------------------------------------------------------------------------------
playout=[
            [
            gui.Button(image_filename=fullpath+"/down.png",image_size=(64,64),key='download'),
            gui.Button(image_filename=fullpath+"/st.png",image_size=(64,64),key='st'),
            gui.Button(image_filename=fullpath+"/pcstat.png",image_size=(64,64),key='pcstat'),
            gui.Button(image_filename=fullpath+"/rams.png",image_size=(64,64),key='ram'),
            gui.Button(image_filename=fullpath+"/info.png",image_size=(64,64),key='credits')
            ]
        ]
wp=gui.Window(title='Download Manager',layout=playout,size=(400,80))

while True:
    events,values=wp.read()

    if events==gui.WIN_CLOSED:
        break
    if events=='download':
        form2()
    if events=="st":
        form3()
    if events=="pcstat":
        form4()   
    if events=="ram":
        form5()
    if events=="credits":
        form6()

wp.close()