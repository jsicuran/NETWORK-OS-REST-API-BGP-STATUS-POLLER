#############################################################
### INITIAL LOGIN TESTING VIA REST POST NON COOKIE VERSION  #
#############################################################


###########################################IMPORT##########################################################
import os
import sys
import json
import requests
import urllib3
import getpass
import pprint
import time
from colorama import just_fix_windows_console, Fore, Back, Style
from colorama import init
import fixpath
import pyfiglet
import datetime
import winsound
#######################################################################################################################
#import keyboard
#import pynput
#from pynput import keyboard

init(autoreset=True)
just_fix_windows_console()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()

sw1 = "192.168.1.210"


def cls():
    os.system('cls')

def topline():
    print(Fore.GREEN + Style.BRIGHT + "\u2550" * 165)

def bottomline():
    print(Fore.GREEN + Style.BRIGHT + "\u2550" * 165)   

def login():
    login = session.post(f"https://{sw1}/rest/v10.11/login", data=creds, verify=False)
    print(f"This is the DC-L3-SW1 login code: {login.status_code} - OK!")
    print(Fore.GREEN + Style.BRIGHT + "\u2591" * 165)
    time.sleep(3)
  
def logout():
    logout = session.post(f"https://{sw1}/rest/v10.11/logout")
    print(Fore.GREEN + Style.BRIGHT + "\u2591" * 165)
    print(f"This is the DC-L3-SW1 logout code: {logout.status_code} - Goodbye!")
 



cls()
topline()
user = input('username:  ')
pwd = getpass.getpass(prompt='password:  ')
creds = {"username": user, "password": pwd}
bottomline()
login()
logout()




###############pickup with hot key method or use other like -----    https://pypi.org/project/pynput/  ### or use os.system calls for simple keyboard input detection for exit #####
 
#def hotkey_pressed():
#    print(Fore.RED + "hotkey was pressed Exiting Application ")
#    logout()
#    sys.exit() 

#keyboard.add_hotkey('ctrl+alt+j', hotkey_pressed)   
    

#keyboard.add_hotkey('ctrl+alt+j', lambda: print(Fore.RED + "hotkey was pressed Exiting Application ")) 
#############################################################################

#keyboard.wait()
#while True:
##    event = keyboard.read_event()
#    if event.event_type == keyboard.KEY_DOWN and event.name == 'ctrl+alt+j':
#        logout()



    




