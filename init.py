from os import path, mkdir, environ, system
import json
from swinlnk.swinlnk import SWinLnk
from pyperclip import paste
from pynput import keyboard

def_s_url = path.join(environ['USERPROFILE'],"Music","Youtube")
lnk_path = rf'{environ["USERPROFILE"]}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'

def get_vk(key):
    return key.vk if hasattr(key, 'vk') else key.value.vk

print("~ KEYBOARD ASSIST ~")
if not path.exists("config.json"):
    print("Initiating...")
    print("Press a key to map for: 'Automated youtube to mp3 downloads'")

    def completeWorkflow(k):
        if not path.exists(def_s_url): mkdir(def_s_url)
        with open("config.json",'w') as c:
            json.dump([[get_vk(k),k.name],def_s_url],c)
        print("[i] -> KEY MAPPED.")
        print(f"[i] -> Download location defaults to : '{def_s_url}'"+'\n       To change, edit config.json')
        # shutil.copyfile(__file__,lnk_path+"\KeyboardAssist.pyw") # Adds program to startup
        # shutil.copyfile("config.json",lnk_path+"\config.json")
        SWinLnk().create_lnk(path.join(path.dirname(__file__),"KeyboardAssist.exe"),lnk_path+"\KeyboardAssist.lnk")
        print("[i] -> Program will run automatically on startup.")
        input("Press any key to exit.")
        # subprocess.run(["pythonw", f"'{lnk_path}\KeyboardAssist.pyw'"], capture_output=False)
        return False 

    with keyboard.Listener(on_press=completeWorkflow) as listener:
        listener.join()