import PySimpleGUI as gui
import platform

my_system = platform.uname()

pclayout = [
                [gui.Text("System: "+str(my_system.system))],
                [gui.Text("Node name: "+str(my_system.node))],
                [gui.Text("Release: "+str(my_system.release))],
                [gui.Text("Version: "+str(my_system.version))],
                [gui.Text("Machine: "+str(my_system.machine))],
                [gui.Text("Processor: "+str(my_system.processor))]
            ]

wpc = gui.Window(title="PC info",layout=pclayout,size=(600,180),location=(400,400))

while True:
            
    event,values = wpc.read()

    if event == gui.WIN_CLOSED:
         break  