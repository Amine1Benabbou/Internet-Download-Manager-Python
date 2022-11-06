import speedtest
import PySimpleGUI as gui

wifi  = speedtest.Speedtest()

    
layout = [
            [gui.Text("Speed Test: ",text_color="RED")],
            [gui.Button("Start"),
            [gui.Text("Download Speed:",key='up')],
            [gui.Text("Upload Speed:",key='down')]]
         ]

ws = gui.Window(title="Speed Test",layout=layout,size=(300,150),location=(400,400))

while True:
        
        event,values = ws.read()

        if event == gui.WIN_CLOSED:
            break  
        if event == "Start":

            ws['up'].update('Download Speed: '+str(round(int(wifi.download())/1048576,2))+' Mb')
            ws['down'].update('Upload Speed: '+str(round(int(wifi.upload())/1048576,2))+' Mb')
            
