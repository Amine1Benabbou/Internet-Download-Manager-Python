
import PySimpleGUI as gui
import requests
import time
import winsound
import threading




def downloadForm():
    layout =[
            [gui.Text("Add a URL to Download: ")],
            [gui.InputText(key='url'),gui.Button("OK")],
            [gui.Text("Size of file:",key="status")],
            [gui.FolderBrowse("Choose Download Path",target="path"),gui.InputText(key="path")],
            [gui.Button("Start Download")],
            [gui.Text('Progress Meter:'),gui.Text(key='meter')],
            [gui.ProgressBar(100,key='pb',size=(100,10),bar_color=['blue','white'])]
            ]

    w = gui.Window(title="Download Manager",layout=layout,size=(840,200),location=(400,400))
    
    def download(values):
        urlin=values['url']  
        liste=urlin.split('/')
        
        urlout=values['path']
        urlout+='/'+liste[len(liste)-1]


        result = requests.get(urlin)
        
        f=open(urlout, "wb")
        f.write(result.content) 
        f.close()
    
    while True:
        
        event,values = w.read()

        threaddownload=threading.Thread(target=download,args=(values,))
        
        if event == gui.WIN_CLOSED:
            break  

        if event == "OK":
            urlin=values['url']
            info = requests.head(urlin)
            headers=info.headers
            if (info.status_code == 200):
                w['status'].update('Size of file: '+str(round(int(headers['Content-Length'])/1024,2))+" Ko")
            else:
                w['status'].update('File not found ')

        if event == "Start Download" :

            threaddownload.start()
            
            for val in range(100):       
                w['meter'].update(str(val+1)+'%')
                pbar=w['pb']
                pbar.UpdateBar(val+1)
                time.sleep(0.01)

            threaddownload.join()

            winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
            w['meter'].update("Download successfull")          

    w.close()
    
