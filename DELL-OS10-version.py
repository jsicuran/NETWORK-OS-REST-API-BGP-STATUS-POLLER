# Monitors BGP peer 6 connections state status and displays color code per state  #
# Simple Text version - with no error handling yet - not pythonic or elegant      #
# GUI and REST Cookie use version forthcoming based on Framework selected         #
# Usage - run from command line or "compiled" then login and leave alone          #
# Coded for specific devices ONLY - for client's use                              #
# Not interactive use Crtl + C to exit anytime                                    #
# IDE(PyCharm)/(VS CODE) based and complied runtime versions available            #
# For DELL OS10 rest api call use                                                 #
#                                                                                 #
#                        Dual switch version                                      #
#                         6/12/2024   V1.0                                        #
#                         6/x/2024    V1.1                                        #      
#                                                                                 #
#2024 Appplied Methodologeis, inc                                                 #
#Author: Jeffrey Sicuranza                                                        #
###################################################################################

######################## IMPORTS ####################################################

import urllib3
import requests
import json
import os
import sys
import time
import pprint
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

url1 = 'https://1.2.3.4/restconf/data/dell-bgp:bgp-oper'  ### >>>> DELL-OS10-VxRAIL-SW1
url2 = 'https://1.2.3.5/restconf/data/dell-bgp:bgp-oper'  ### >>>> DELL-OS10-VxRAIL-SW2

#####################################################################################################


######## Replace these variables with your actual credentials and URL ---- USE GETPASS function for production use ##########
#username = 'BLA BLA'
#password = 'BLA BLA'
##########################################################################################################################

#################### REVERSE FOR COLO2 HAVING COMMACK PEERS IN LIST ###############################

########## BGP PEER ENDPOINT NAME TABLE #################
DC1 = "DC1-L3-SW1  \u25ba "
DC2 = "DC2-L3-SW2  \u25ba "
fs_1 = "FISERV1  \u25ba "
fs_2 = "FISERV2  \u25ba "
off = "Office    \u25ba "
ws = "Windstream    \u25ba "
###################################################

######## BGP NEIGHBOR PEER STATUS ENDPOINT TABLE #######################################################
COLO1 = '1.2.3.4'  ####  neighbor 10.190.100.1 description PtP to DC365 FNBLI-365DC-L3-SW1 
COLO2 = '1.2.3.5'  ####  neighbor 10.190.100.1 description PtP to DC365 FNBLI-365DC-L3-SW2 
off = '5.6.7.8'  ####  neighbor 10.170.100.3 description 275  Networks 
WSVELO = '9.10.11.12' ####  description WINDSTREAM-SD-WAN-VELOCLOUD-HA-PAIR
FISERV1 = '13.14.15.16' ####  description FISERV-DNA-PRIMARY
FISERV2 = '13.14.15.17' ####  description FISERV-DNA-SECONDARY
######################################################################################################



#data = response.json()

##################### GENERAL FUNCTION DEFINITIONS ####################################################

def cls():
    os.system('cls')
def beep():
    winsound.Beep(3000, 500)

def banner():
    result = pyfiglet.figlet_format("            B A N K ", font="slant")
    print(Fore.BLUE + Style.BRIGHT + result)
    print(Fore.YELLOW + Style.BRIGHT + '                         NOC - CORE INTERNAL WAN BGP PEER STATUS')

def topline():
    print(Fore.GREEN + Style.BRIGHT + "\u2550" * 145)

def bottomline():
    print(Fore.GREEN + Style.BRIGHT + "\u2550" * 145)

def splitline():
    print(Fore.YELLOW + Style.BRIGHT + "-" * 145)

def footer():
    print(Fore.YELLOW + Style.BRIGHT +  "\u00a9 " '2024 Applied Methodologies, Inc. ')

############################################ LOGIN FUNCTIONS ###############################################################

def login():
    login = requests.get(url1, headers=headers, auth=(username, password), verify=False)
    if login.status_code == 200:
         print(f"DELL-OS10-VxRAIL-SW1 login code: {login.status_code} - OK!")
         print(Fore.GREEN + Style.BRIGHT + "\u2591" * 165)
         time.sleep(3)


        #print(f"DELL-OS10-VxRAIL-SW1 login code: {login.status_code} - OK!")
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
         print(f"DELL-OS10-VxRAIL-SW2 login code: {login1.status_code} - OK!")
         print(Fore.GREEN + Style.BRIGHT + "\u2591" * 165)
         time.sleep(3)

        #print(f"DELL-OS10-VxRAIL-SW2 login code: {login1.status_code} - OK!")
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
        if peer['remote-address'] == COLO1 and peer['bgp-state'] == 'established':
            print(DC1, COLO1, Back.GREEN + Style.BRIGHT + 'peer is in Established state')
        if peer['remote-address'] == COLO1 and peer['bgp-state'] == 'openConfirm':
            print(DC1, COLO1, Back.YELLOW + 'peer is in OpenConfirm state')
        if peer['remote-address'] == COLO1 and peer['bgp-state'] == 'openSent':
            print(DC1, COLO1, Back.CYAN + 'peer is in OpenSent state')
        if peer['remote-address'] == COLO1 and peer['bgp-state'] == 'active':
            print(DC1, COLO1, Back.BLUE + 'peer is in Active state')
        if peer['remote-address'] == COLO1 and peer['bgp-state'] == 'connect':
            print(DC1, COLO1, Back.MAGENTA + 'peer is in Connect state')
        if peer['remote-address'] == COLO1 and peer['bgp-state'] == 'idle':
            print(DC1, COLO1, Back.RED + 'peer is in Idle state')
            beep()
        if peer['remote-address'] == COLO1 and peer['bgp-state'] == '':   
            print(DC1, COLO2, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit')) 

        #else: 
             #print(DC1, COLO1, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))     

        
        if peer['remote-address'] == COLO2 and peer['bgp-state'] == 'established':
            print(DC2, COLO2, Back.GREEN + Style.BRIGHT + 'peer is in Established state')
        if peer['remote-address'] == COLO2 and peer['bgp-state'] == 'openConfirm':
            print(DC2, COLO2, Back.YELLOW + 'peer is in OpenConfirm state')
        if peer['remote-address'] == COLO2 and peer['bgp-state'] == 'openSent':
            print(DC2, COLO2, Back.CYAN + 'peer is in OpenSent state')
        if peer['remote-address'] == COLO2 and peer['bgp-state'] == 'active':
            print(DC2, COLO2, Back.BLUE + 'peer is in Active state')
        if peer['remote-address'] == COLO2 and peer['bgp-state'] == 'connect':
            print(DC2, COLO2, Back.MAGENTA + 'peer is in Connect state')
        if peer['remote-address'] == COLO2 and peer['bgp-state'] == 'idle':
            print(DC2, COLO2, Back.RED + 'peer is in Idle state')
            beep()
        if peer['remote-address'] == COLO2 and peer['bgp-state'] == '':
            print(DC2, COLO2, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))

        #else: 
             #print(DC2, COLO2, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))  
        
        if peer['remote-address'] == off and peer['bgp-state'] == 'established':
            print(off, off, Back.GREEN + Style.BRIGHT + 'peer is in Established state')
        if peer['remote-address'] == off and peer['bgp-state'] == 'openConfirm':
            print(off, off, Back.YELLOW + 'peer is in OpenConfirm state')
        if peer['remote-address'] == off and peer['bgp-state'] == 'openSent':
            print(off, off, Back.CYAN + 'peer is in OpenSent state')
        if peer['remote-address'] == off and peer['bgp-state'] == 'active':
            print(off, off, Back.BLUE + 'peer is in Active state')
        if peer['remote-address'] == off and peer['bgp-state'] == 'connect':
            print(off, off, Back.MAGENTA + 'peer is in Connect state')
        if peer['remote-address'] == off and peer['bgp-state'] == 'idle':
            print(off, off, Back.RED + 'peer is in Idle state')
            #beep()
        if peer['remote-address'] == off and peer['bgp-state'] == '':
            print(off, off, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))

        #else: 
         #   print(off, off, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))  

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



        if peer['remote-address'] == FISERV1 and peer['bgp-state'] == 'established':
            print(fs_1, FISERV1, Back.GREEN + Style.BRIGHT + 'peer is in Established state')
        if peer['remote-address'] == FISERV1 and peer['bgp-state'] == 'openConfirm':
            print(fs_1, FISERV1, Back.YELLOW + 'peer is in OpenConfirm state')
        if peer['remote-address'] == FISERV1 and peer['bgp-state'] == 'openSent':
            print(fs_1, FISERV1, Back.CYAN + 'peer is in OpenSent state')
        if peer['remote-address'] == FISERV1 and peer['bgp-state'] == 'active':
            print(fs_1, FISERV1, Back.BLUE + 'peer is in Active state')
        if peer['remote-address'] == FISERV1 and peer['bgp-state'] == 'connect':
            print(fs_1, FISERV1, Back.MAGENTA + 'peer is in Connect state')
        if peer['remote-address'] == FISERV1 and peer['bgp-state'] == 'idle':
            print(fs_1, FISERV1, Back.RED + 'peer is in Idle state')
            beep()
        if peer['remote-address'] == FISERV1 and peer['bgp-state'] == '':
            print(fs_1, FISERV1, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))

        #else: 
         #   print(fs_1, FISERV1, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))
              
        if peer['remote-address'] == FISERV2 and peer['bgp-state'] == 'established':
            print(fs_2, FISERV2, Back.GREEN + Style.BRIGHT + 'peer is in Established state')
        if peer['remote-address'] == FISERV2 and peer['bgp-state'] == 'openConfirm':
            print(fs_2, FISERV2, Back.YELLOW + 'peer is in OpenConfirm state')
        if peer['remote-address'] == FISERV2 and peer['bgp-state'] == 'openSent':
             print(fs_2, FISERV2, Back.CYAN + 'peer is in OpenSent state')
        if peer['remote-address'] == FISERV2 and peer['bgp-state'] == 'active':
             print(fs_2, FISERV2, Back.BLUE + 'peer is in Active state')
        if peer['remote-address'] == FISERV2 and peer['bgp-state'] == 'connect':
             print(fs_2, FISERV2, Back.MAGENTA + 'peer is in Connect state')
        if peer['remote-address'] == FISERV2 and peer['bgp-state'] == 'idle':
             print(fs_2, FISERV2, Back.RED + 'peer is in Idle state')
             beep()
        if peer['remote-address'] == FISERV2 and peer['bgp-state'] == '':
            print(fs_2, FISERV2, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit')) 

        #else: 
        #    print(fs_2, FISERV2, (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))
           
        splitline()

################################ RUNTIME LOGIN #####################################################################
############ NON TOKEN VERSION - LOGIN ONCE USING GET PASS SAVE CREDS USE IN API FOR FOLLOW ON CALLS ###############
####################################################################################################################

######START RUN###### LOGIN PROMPTS TO FOLLOW - GETPASS FUNCTION ETC###################################################
cls()
topline()
username = input('Enter username:  ')
password = getpass.getpass(prompt='Enter password:  ')
#creds = {"username": username, "password": password}
login()
login1()
bottomline()
time.sleep(3)
cls()
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
        print(Back.BLUE + Fore.WHITE + Style.BRIGHT +  '    COLO2 DC \u25ba SWITCH DELL-OS10-VxRAIL-SW1 \u25c4 PEER CHECK    ')
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
        print(Back.BLUE + Fore.WHITE + Style.BRIGHT + '    COLO2 DC \u25ba SWITCH DELL-OS10-VxRAIL-SW2 \u25c4 PEER CHECK    ')
        bottomline()
        bgpblock()
        bottomline()
        footer()
        #time.sleep(3)
        
      
    
###############################################CLEANUP#######################################################################
    # sw_resp.clear()

##############################################END RUN#######################################################################


#########################################EXTRAS##############################################################################
## DELL SWITCH OS10 REST API SCHEMA DUMP 
#data = response.json()
#pprint.pprint(data)
#############################################################################################################################

