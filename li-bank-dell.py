# Monitors BGP peer 6 connections state status and displays color code per state  #
# Simple Text version - with no error handling yet - not pythonic or elegant      #
# GUI and REST Cookie use version forthcoming based on Framework selected         #
# Usage - run from command line or "compiled" then login and leave alone          #
# Coded for specific devices ONLY - for client's use                              #
# Not interactive use Crtl + C to exit anytime                                    #
# IDE(PyCharm)/(VS CODE) based and complied runtime versions available            #
# For DELL OS10 OS Version: 10.5.4.5 rest api call use.                           #
# Compiled using PyInstaller 6.5.0 -                                              #
# pyinstaller -F  dell.py --collect-all pyfiglet                                  #
#                                                                                 #
#                        Dual switch version                                      #
#                         6/12/2024   V1.0                                        #
#                         6/13/2024   V1.1                                        #
#                         7/25/2024   V1.2                                        #
#                         9/27/2024   v1.3                                        #    
#                         3/6/2025    V1.5 add BANK migration peer                #   
#                                                                                 #
#2025 Appplied Methodologeis, inc                                                 #
#Author: Jeffrey Sicuranza                                                        #
###################################################################################

######################## IMPORTS ##################################################

import urllib3
import requests
import json
import os
import sys
import time
import pprint
import getpass
import time
from colorama import just_fix_windows_console, Fore, Back, Style
from colorama import init
import fixpath
import pyfiglet
import pyfiglet.fonts
import datetime
import winsound


############################### INITS, GLOBALS AND OTHER STARTUPS ############################################
init(autoreset=True)
just_fix_windows_console()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()
headers = {
    'Accept': 'application/yang-data+json',
    'Content-Type': 'application/yang-data+json',
    'Cookie': 'session_cookie'
}
####################################################################################################

###################################### SCREEN COLOR SCHEMA #######################################################

# Fore, Back and Style are convenience classes for the constant ANSI strings that set
#     the foreground, background and style. The don't have any magic of their own.
FORES = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
BACKS = [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE]
STYLES = [Style.DIM, Style.NORMAL, Style.BRIGHT]
################################################################################################################

################### NETWORK SWITCH REST API LOGIN ENDPOINT TABLE #################################################

############################### DNS HOSTNAME VERSION ############################################################
url1 = 'https://CO-LO-VxR-SW1.BANK.com/restconf/data/dell-bgp:bgp-oper'  ### >>>> CO-LO-VxR-SW1
url2 = 'https://CO-LO-VxR-SW2.BANK.com/restconf/data/dell-bgp:bgp-oper'  ### >>>> CO-LO-VxR-SW2

#url1 = 'https://99.66.200.230/restconf/data/dell-bgp:bgp-oper'  ### >>>> CO-LO-VxR-SW1
#url2 = 'https://99.66.200.231/restconf/data/dell-bgp:bgp-oper'  ### >>>> CO-LO-VxR-SW2

#####################################################################################################


######## Replace these variables with your actual credentials and URL ---- USE GETPASS function from Aruba code ##########
#username = 'admin'
#password = 'admin'
##########################################################################################################################

#################### REVERSE FOR LI-BANK-DC-2 HAVING LI-DC1 PEERS IN LIST ###############################

########## BGP PEER ENDPOINT NAME TABLE #################
CMK1 = "365DC-L3-SW1  \u25ba "
CMK2 = "365DC-L3-SW2  \u25ba "
fs_1 = "Fiserv DNA 1  \u25ba "
fs_2 = "Fiserv DNA 2  \u25ba "
mel = "Melville HQ   \u25ba "
ws = "Windstream    \u25ba "
BANK2 = "BANK2    \u25ba "
###################################################

######## BGP NEIGHBOR PEER STATUS ENDPOINT TABLE #######################################################
LI-DC11 = '53.91.100.1'  ####  neighbor 53.91.100.1 description PtP to DC365 BANK-365DC-L3-SW1 
LI-DC12 = '53.91.100.2'  ####  neighbor 53.91.100.1 description PtP to DC365 BANK-365DC-L3-SW2 
MELHQ = '63.92.100.3'  ####  neighbor 63.92.100.3 description NET HQ Networks 
WSVELO = '99.66.100.10' ####  description WINDSTREAM-SD-WAN-VELOCLOUD-HA-PAIR
DNA1 = '99.66.100.20' ####  description FISERV-DNA-PRIMARY
DNA2 = '99.66.100.21' ####  description FISERV-DNA-SECONDARY
BANK2 = '42.21.65.30'     ####  description BANK2-SD-WAN
######################################################################################################



#data = response.json()

##################### GENERAL FUNCTION DEFINITIONS ####################################################

def cls():
    os.system('cls')

def beep():
    winsound.Beep(3000, 500)

def banner():
    result = pyfiglet.figlet_format('F N B L I', justify='center', font='banner')
    print(Fore.BLUE + Style.BRIGHT + result)
    print(Fore.YELLOW + Style.BRIGHT + '                         NOC - CORE INTERNAL WAN BGP PEER STATUS')

def topline():
    print(Fore.GREEN + Style.BRIGHT + "\u2550" * 80)

def bottomline():
    print(Fore.GREEN + Style.BRIGHT + "\u2550" * 80)

def splitline():
    print(Fore.YELLOW + Style.BRIGHT + "-" * 80)

def footer():
    print(Fore.YELLOW + Style.BRIGHT +  "\u00a9 " '2025 Applied Methodologies, Inc. ')

############################################ LOGIN FUNCTIONS ###############################################################

def login():
    login = requests.get(url1, headers=headers, auth=(username, password), verify=False)
    if login.status_code == 200:
         print(f"CO-LO-VxR-SW1 login code: {login.status_code} - OK!")
         print(Fore.GREEN + Style.BRIGHT + "\u2591" * 80)
         time.sleep(3)


        #print(f"CO-LO-VxR-SW1 login code: {login.status_code} - OK!")
        #print(f"This is the session cookies:\n {login.cookies}")
    
    else:
    #    if login.status_code == 401:
            cls()
            #print("Failed to retrieve data:", login.status_code, login.text)
            print("PLEASE RE-RUN APP AND RE-ENTER CREDENTIALS")
            exit()
    
def login1():
   # Make the GET request
    login1 = requests.get(url2, headers=headers, auth=(username, password), verify=False)
#Check if the login1 request was successful
    if login1.status_code == 200:
         print(f"CO-LO-VxR-SW2 login code: {login1.status_code} - OK!")
         print(Fore.GREEN + Style.BRIGHT + "\u2591" * 80)
         time.sleep(3)

        #print(f"CO-LO-VxR-SW2 login code: {login1.status_code} - OK!")
        #print(f"This is the session cookies:\n {login1.cookies}")
    
    else:
    #     if login1.status_code == 401:
              cls()
              #print("Failed to retrieve data:", login1.status_code, login.text)
              print("PLEASE RE-RUN APP AND RE-ENTER CREDENTIALS")
              exit()
##########################################################################################################################

################################################LOAD PAGE HEADER################################################

def pageheader():
    topline()
    banner()
    bottomline()
################################################################################################################


#################################### MAIN LOGIC PEER STATUS CHECK FUNCTIONS ##############################################
def bgpblock():
    for peer in bgp_peers:
        if peer['remote-address'] == LI-DC11 and peer['bgp-state'] == 'established':
            print(CMK1, LI-DC11, Back.GREEN + Style.BRIGHT + 'peer is in Established state')
        if peer['remote-address'] == LI-DC11 and peer['bgp-state'] == 'openConfirm':
            print(CMK1, LI-DC11, Back.YELLOW + 'peer is in OpenConfirm state')
        if peer['remote-address'] == LI-DC11 and peer['bgp-state'] == 'openSent':
            print(CMK1, LI-DC11, Back.CYAN + 'peer is in OpenSent state')
        if peer['remote-address'] == LI-DC11 and peer['bgp-state'] == 'active':
            print(CMK1, LI-DC11, Back.BLUE + 'peer is in Active state')
        if peer['remote-address'] == LI-DC11 and peer['bgp-state'] == 'connect':
            print(CMK1, LI-DC11, Back.MAGENTA + 'peer is in Connect state')
        if peer['remote-address'] == LI-DC11 and peer['bgp-state'] == 'idle':
            print(CMK1, LI-DC11, Back.RED + 'peer is in Idle state')
            beep()
        if peer['remote-address'] == LI-DC11 and peer['bgp-state'] == '':   
            print(CMK1, LI-DC11, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit')) 

        #else: 
             #print(CMK1, LI-DC11, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))     

        
        if peer['remote-address'] == LI-DC12 and peer['bgp-state'] == 'established':
            print(CMK2, LI-DC12, Back.GREEN + Style.BRIGHT + 'peer is in Established state')
        if peer['remote-address'] == LI-DC12 and peer['bgp-state'] == 'openConfirm':
            print(CMK2, LI-DC12, Back.YELLOW + 'peer is in OpenConfirm state')
        if peer['remote-address'] == LI-DC12 and peer['bgp-state'] == 'openSent':
            print(CMK2, LI-DC12, Back.CYAN + 'peer is in OpenSent state')
        if peer['remote-address'] == LI-DC12 and peer['bgp-state'] == 'active':
            print(CMK2, LI-DC12, Back.BLUE + 'peer is in Active state')
        if peer['remote-address'] == LI-DC12 and peer['bgp-state'] == 'connect':
            print(CMK2, LI-DC12, Back.MAGENTA + 'peer is in Connect state')
        if peer['remote-address'] == LI-DC12 and peer['bgp-state'] == 'idle':
            print(CMK2, LI-DC12, Back.RED + 'peer is in Idle state')
            beep()
        if peer['remote-address'] == LI-DC12 and peer['bgp-state'] == '':
            print(CMK2, LI-DC12, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))

        #else: 
             #print(CMK2, LI-DC12, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))  
        
        if peer['remote-address'] == MELHQ and peer['bgp-state'] == 'established':
            print(mel, MELHQ, Back.GREEN + Style.BRIGHT + 'peer is in Established state')
        if peer['remote-address'] == MELHQ and peer['bgp-state'] == 'openConfirm':
            print(mel, MELHQ, Back.YELLOW + 'peer is in OpenConfirm state')
        if peer['remote-address'] == MELHQ and peer['bgp-state'] == 'openSent':
            print(mel, MELHQ, Back.CYAN + 'peer is in OpenSent state')
        if peer['remote-address'] == MELHQ and peer['bgp-state'] == 'active':
            print(mel, MELHQ, Back.BLUE + 'peer is in Active state')
        if peer['remote-address'] == MELHQ and peer['bgp-state'] == 'connect':
            print(mel, MELHQ, Back.MAGENTA + 'peer is in Connect state')
        if peer['remote-address'] == MELHQ and peer['bgp-state'] == 'idle':
            print(mel, MELHQ, Back.RED + 'peer is in Idle state')
            #beep()
        if peer['remote-address'] == MELHQ and peer['bgp-state'] == '':
            print(mel, MELHQ, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))

        #else: 
         #   print(mel, MELHQ, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))  

        if peer['remote-address'] == WSVELO and peer['bgp-state'] == 'established':
            print(ws, WSVELO, Back.GREEN + Style.BRIGHT + 'peer is in Established state')
        if peer['remote-address'] == WSVELO and peer['bgp-state'] == 'openConfirm':
            print(ws, WSVELO, Back.YELLOW + 'peer is in OpenConfirm state')
        if peer['remote-address'] == WSVELO and peer['bgp-state'] == 'openSent':
            print(ws, WSVELO, Back.CYAN + 'peer is in OpenSent state')
        if peer['remote-address'] == WSVELO and peer['bgp-state'] == 'active':
            print(ws, WSVELO, Back.BLUE + 'peer is in Active state')
        if peer['remote-address'] == WSVELO and peer['bgp-state'] == 'connect':
            print(ws, WSVELO, Back.MAGENTA + 'peer is in Connect state')
        if peer['remote-address'] == WSVELO and peer['bgp-state'] == 'idle':
            print(ws, WSVELO, Back.RED + 'peer is in Idle state')
            beep()
        if peer['remote-address'] == WSVELO and peer['bgp-state'] == '':
            print(ws, WSVELO, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit')) 

        #else: 
        #    print(ws, WSVELO, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))  



        if peer['remote-address'] == DNA1 and peer['bgp-state'] == 'established':
            print(fs_1, DNA1, Back.GREEN + Style.BRIGHT + 'peer is in Established state')
        if peer['remote-address'] == DNA1 and peer['bgp-state'] == 'openConfirm':
            print(fs_1, DNA1, Back.YELLOW + 'peer is in OpenConfirm state')
        if peer['remote-address'] == DNA1 and peer['bgp-state'] == 'openSent':
            print(fs_1, DNA1, Back.CYAN + 'peer is in OpenSent state')
        if peer['remote-address'] == DNA1 and peer['bgp-state'] == 'active':
            print(fs_1, DNA1, Back.BLUE + 'peer is in Active state')
        if peer['remote-address'] == DNA1 and peer['bgp-state'] == 'connect':
            print(fs_1, DNA1, Back.MAGENTA + 'peer is in Connect state')
        if peer['remote-address'] == DNA1 and peer['bgp-state'] == 'idle':
            print(fs_1, DNA1, Back.RED + 'peer is in Idle state')
            beep()
        if peer['remote-address'] == DNA1 and peer['bgp-state'] == '':
            print(fs_1, DNA1, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))

        #else: 
         #   print(fs_1, DNA1, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))
              
        if peer['remote-address'] == DNA2 and peer['bgp-state'] == 'established':
            print(fs_2, DNA2, Back.GREEN + Style.BRIGHT + 'peer is in Established state')
        if peer['remote-address'] == DNA2 and peer['bgp-state'] == 'openConfirm':
            print(fs_2, DNA2, Back.YELLOW + 'peer is in OpenConfirm state')
        if peer['remote-address'] == DNA2 and peer['bgp-state'] == 'openSent':
             print(fs_2, DNA2, Back.CYAN + 'peer is in OpenSent state')
        if peer['remote-address'] == DNA2 and peer['bgp-state'] == 'active':
             print(fs_2, DNA2, Back.BLUE + 'peer is in Active state')
        if peer['remote-address'] == DNA2 and peer['bgp-state'] == 'connect':
             print(fs_2, DNA2, Back.MAGENTA + 'peer is in Connect state')
        if peer['remote-address'] == DNA2 and peer['bgp-state'] == 'idle':
             print(fs_2, DNA2, Back.RED + 'peer is in Idle state')
             beep()
        if peer['remote-address'] == DNA2 and peer['bgp-state'] == '':
            print(fs_2, DNA2, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit')) 

        #else: 
        #    print(fs_2, DNA2, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))

        if peer['remote-address'] == BANK2 and peer['bgp-state'] == 'established':
                print(BANK2, BANK2, Back.GREEN + Style.BRIGHT + 'peer is in Established state')
        if peer['remote-address'] == BANK2 and peer['bgp-state'] == 'openConfirm':
                print(BANK2, BANK2, Back.YELLOW + 'peer is in OpenConfirm state')
        if peer['remote-address'] == BANK2 and peer['bgp-state'] == 'openSent':
                print(BANK2, BANK2, Back.CYAN + 'peer is in OpenSent state')
        if peer['remote-address'] == BANK2 and peer['bgp-state'] == 'active':
                print(BANK2, BANK2, Back.BLUE + 'peer is in Active state')
        if peer['remote-address'] == BANK2 and peer['bgp-state'] == 'connect':
                print(BANK2, BANK2, Back.MAGENTA + 'peer is in Connect state')
        if peer['remote-address'] == BANK2 and peer['bgp-state'] == 'idle':
                print(BANK2, BANK2, Back.RED + 'peer is in Idle state')
                beep()
        if peer['remote-address'] == BANK2 and peer['bgp-state'] == '':
                print(BANK2, BANK2, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit')) 

        #else: 
        #    print(BANK2, BANK2, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))


           
        splitline()

############################### RUNTIME LOGIN #####################################################################
########## NON TOKEN VERSION - LOGIN ONCE USING GET PASS SAVE CREDS USE IN API FOR FOLLOW ON CALLS ################
#login()

#login1()
##########################################################################################################

######START RUN###### LOGIN PROMPTS TO FOLLOW - GETPASS FUNCTION ETC###################################################
cls()
topline()
username = input('Enter username:  ')
password = getpass.getpass(prompt='Enter password:  ')
#creds = {"username": username, "password": password}
bottomline()
login()
login1()
#time.sleep(3)
#cls()
#####################################################################################################################




############################## MAIN RUNTIME LOOP LOGIC ###################################################

while True: 
    response = requests.get(url1, headers=headers, auth=(username, password), verify=False)
    data = response.json()
   
    bgp_peers = []
    vrfs = data.get("dell-bgp:bgp-oper", {}).get("vrf", [])
    for vrf in vrfs:
        #vrf_name = vrf.get("vrf-name")
        peer_ops = vrf.get("peer-oper", [])
        for peer_op in peer_ops:
            remote_address = peer_op.get("remote-address")
            bgp_state = peer_op.get("bgp-state")
            bgp_peers.append({
            #"vrf-name": vrf_name,
            "remote-address": remote_address,
            "bgp-state": bgp_state
                 })
        time.sleep(5)
        cls()
        pageheader()
        print(Back.BLUE + Fore.WHITE + Style.BRIGHT +  '    LI-BANK-DC-2 DC \u25ba SWITCH CO-LO-VxR-SW1 \u25c4 PEER CHECK    ')
        bottomline()
        bgpblock()
        

    ##################### SECOND REST API CALL TO SECOND DC SWITCH ##############
     
    response = requests.get(url2, headers=headers, auth=(username, password), verify=False)
    data = response.json()
   
    bgp_peers = []
    vrfs = data.get("dell-bgp:bgp-oper", {}).get("vrf", [])
    for vrf in vrfs:
        #vrf_name = vrf.get("vrf-name")
        peer_ops = vrf.get("peer-oper", [])
        for peer_op in peer_ops:
            remote_address = peer_op.get("remote-address")
            bgp_state = peer_op.get("bgp-state")
            bgp_peers.append({
            #"vrf-name": vrf_name,
            "remote-address": remote_address,
            "bgp-state": bgp_state
                 })
        topline()
        print(Back.BLUE + Fore.WHITE + Style.BRIGHT + '    LI-BANK-DC-2 DC \u25ba SWITCH CO-LO-VxR-SW2 \u25c4 PEER CHECK    ')
        bottomline()
        bgpblock()
        bottomline()
        footer()
        #time.sleep(3)
        
      
    
###############################################CLEANUP#######################################################################
    # sw_resp.clear()

##############################################END RUN#######################################################################


#########################################EXTRAS##############################################################################


