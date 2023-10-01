"""
~ KEYBOARD ASSIST ~
Author: Chethas L Pramod (github.com/chethaslp)
Date: 20-10-2022

"""

from re import findall
import subprocess
from pynput import keyboard
from win10toast import ToastNotifier

from os import path, mkdir, environ, system
import shutil
import json
import requests
from swinlnk.swinlnk import SWinLnk
from pyperclip import paste

toast = ToastNotifier()

def_s_url = path.join(environ['USERPROFILE'],"Music","Youtube")
lnk_path = rf'{environ["USERPROFILE"]}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'

s_url:str = ''
s_key = []

def get_vk(key):
    return key.vk if hasattr(key, 'vk') else key.value.vk

def chng_url():
    global s_url
    try:
        if path.isdir(paste()):
            s_url = paste()
            toast.show_toast("Working directory changed.",s_url,duration=2,threaded=True,icon_path="img.ico")
        else:
            s_url = def_s_url
    except:
        pass

    
        
def grab_yt(s_url):
    v_url = paste()
    if len(findall("youtube.com/watch?", v_url)) == 0 and len(findall("youtu.be", v_url)) == 0:
        try:
            toast.show_toast("URL Not Supported.",v_url,duration=2,threaded=True,icon_path="img.ico")
        except Exception:
            pass
        return
    else:
        try:
            toast.show_toast("Url Captured !","Fetching video...",duration=2,threaded=True,icon_path="img.ico")
        except Exception:
            pass
    g_url="https://www.y2mate.com/mates/analyze/ajax"
    c_url = "https://www.y2mate.com/mates/mp3Convert?hl=en30"
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.",
        "Referer": "https://y2mate.com/",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    g_data = {
        "url": v_url,
        "q_auto": 0,
        "ajax": 1
    }
    g_req = requests.post(g_url,data=g_data)
    q_resp = json.loads(g_req.text)['result']

    v_id = q_resp.split('k_data_vid = "')[1].split('"')[0]
    _id = q_resp.split('k__id = "')[1].split('"')[0]
    v_name = q_resp.split('k_data_vtitle = "')[1].split('"')[0]

    if g_req.status_code == 200:
        try:
            toast.show_toast("Video obtained!","Converting "+v_name,duration=2,threaded=True,icon_path="img.ico")
        except Exception:
            pass
    c_data = {
        "type": "youtube",
        "_id": _id,
        "v_id": v_id,
        "mp3_type": 320,
        "token":""
    }

    c_req = requests.post(c_url,data=c_data)
    if c_req.status_code == 200:
        try:
            toast.show_toast("Downloading Started...",v_name+".mp3",duration=2,threaded=True,icon_path="img.ico")
        except Exception:
            pass
    q_resp = json.loads(c_req.text)['result']
    d_url = q_resp.split('a href="')[1].split('"')[0]
    with open(path.join(s_url,"".join(x for x in v_name if x.isalnum() or x==" ")+".mp3"), "wb") as file:
        file.write(requests.get(d_url).content)

def on_press(key):
    if get_vk(key) == s_key[0]:
        grab_yt(s_url)

# add_to_startup()


def initWorkflow():
    print("~ KEYBOARD ASSIST ~")
    if not path.exists("config.json"):
        system('python init.py')
        # with subprocess.Popen(["python", "init.py"]) as p:
        #     p.wait()

    with open("config.json",'r') as c:
        global s_url,s_key
        s = json.load(c)
        s_url, s_key = s[1],s[0]
    print("Listening...")

    def for_canonical(f):
        return lambda k: f(l.canonical(k))
    hotkey = keyboard.HotKey( keyboard.HotKey.parse('<ctrl>+<alt>+q'), chng_url)
    with keyboard.Listener(on_press=for_canonical(hotkey.press),on_release=for_canonical(hotkey.release)) as l:
        with keyboard.Listener(on_press=on_press) as listener:
            l.join()
            
initWorkflow()
