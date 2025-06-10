###################################################################################
#                        Color Code BGP Peer State Monitor                        #   
# Monitors BGP peer 6 connections state status and displays color code per state  #
# Simple Text version - with no error handling yet - not pythonic or elegant      # 
# GUI and REST Cookie use version forthcoming based on Framework selected         #
# Usage - run from command line or "compiled" then login and leave alone          #
# Coded for specific devices ONLY - for client's use                              #
# Not interactive use Crtl + C to exit anytime                                    #
# IDE(PyCharm)/(VS CODE) based and complied runtime versions available            #
# For ArubaOS-CX LL.10.11.0001   rest api call use.                               #  
# Compiled using PyInstaller 6.5.0 -                                              #
# pyinstaller -F  XXX.py --collect-all pyfiglet                                   #
#                                                                                 #
#                        Dual switch version                                      #
#                         2/20/2024   V1.0                                        #
#                         3/7/2024    V1.2                                        # 
#                         3/14/2024   V1.3                                        #
#                         9/27/2024   V1.4                                        #
#                         3/6/2025    V1.5 add BANK MERGER migration peer         #      
#                                                                                 #
#2025 Appplied Methodologeis, inc                                                 #
#Author: Jeffrey Sicuranza                                                        #
###################################################################################

########################IMPORTS####################################################
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
############################################################################################################

###############################INITS, GLOBALS AND OTHER STARTUPS############################################
init(autoreset=True)
just_fix_windows_console()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()
################################################################################################################

######################################SCREEN COLOR SCHEMA#######################################################

# Fore, Back and Style are convenience classes for the constant ANSI strings that set
#     the foreground, background and style. The don't have any magic of their own.
FORES = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
BACKS = [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE]
STYLES = [Style.DIM, Style.NORMAL, Style.BRIGHT]
################################################################################################################

################### NETWORK SWITCH REST API LOGIN ENDPOINT TABLE #################################################

############################### DNS HOSTNAME VERSION ############################################################

sw1 = 'BANK-365DC-SW1'
sw2 = 'BANK-365DC-SW2'

######REST API LOGIN ENDPOINT TABLE#################################################################

#sw1 = '88.72.254.1'
#sw2 = '88.72.254.2'

#####################################################################################################

##########PEER ENDPOINT NAME TABLE###################################################################
ob_1 = "CO-LO-VxR-SW1 \u25ba "
ob_2 = "CO-LO-VxR-SW2 \u25ba "
fs_1 = "Fiserv DNA 1  \u25ba "
fs_2 = "Fiserv DNA 2  \u25ba "
mel = "Melville HQ   \u25ba "
ws = "Windstream    \u25ba "
BANK2 = "BANK2    \u25ba "
######################################################################################################

########BGP NEIGHBOR PEER STATUS ENDPOINT TABLE#######################################################
peer1 = '10.85.100.3'  ####  neighbor 10.85.100.3 description PtP to VERTUIT-CO-LO-DC-SW1
peer2 = '10.85.100.4'  ####  neighbor 10.85.100.4 description PtP to VERTUIT-CO-LO-DC-SW2
peer3 = '10.31.100.3'  ####  neighbor 10.31.100.3 description NET HQ Networks
peer4 = '88.72.100.10' ####  description WINDSTREAM-SD-WAN-VELOCLOUD-HA-PAIR
peer5 = '88.72.100.20' ####  description FISERV-DNA-PRIMARY
peer6 = '88.72.100.21' ####  description FISERV-DNA-SECONDARY
peer7 = '89.53.62.71'     ####  description CNOB-SD-WAN
######################################################################################################



##################### GENERAL FUNCTION DEFINITIONS####################################################

def cls():
    os.system('cls')

def beep():
    winsound.Beep(3000, 500)

def banner():
    result = pyfiglet.figlet_format("            B A N K ", font="slant")
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

def login():
    login = session.post(f"https://{sw1}/rest/v10.11/login", data=creds, verify=False)
    print(f"This is the BANK-365DC-L3-SW1 login code: {login.status_code} - OK!")
    print(Fore.GREEN + Style.BRIGHT + "\u2591" * 80)
    time.sleep(2)
    login = session.post(f"https://{sw2}/rest/v10.11/login", data=creds, verify=False)
    print(f"This is the BANK-365DC-L3-SW2 login code: {login.status_code} - OK!")
    print(Fore.GREEN + Style.BRIGHT + "\u2591" * 80)
    time.sleep(2)
  
def logout():
    logout = session.post(f"https://{sw1}/rest/v10.11/logout")
    print(Fore.GREEN + Style.BRIGHT + "\u2591" * 80)
    print(f"This is the BANK-365DC-L3-SW2 logout code: {logout.status_code} - Goodbye!")
    time.sleep(2)
    logout = session.post(f"https://{sw2}/rest/v10.11/logout")
    print(Fore.GREEN + Style.BRIGHT + "\u2591" * 80)
    print(f"This is the BANK-365DC-L3-SW2 logout code: {logout.status_code} - Goodbye!")
    time.sleep(2)

################################################LOAD PAGE HEADER################################################

def pageheader():
    topline()
    banner()
    bottomline()
################################################################################################################
    
    
##################################START CHECKING PEER STATUS####################################################

################################################################################################################

##############################ORANGEBURG BGP PEER#1#############################################################
def bgp_block1():
    if k == peer1 and v == {'status': {'bgp_peer_state': 'Established'}}:
        print(ob_1, (k), (Back.GREEN + Style.BRIGHT + 'peer is in Established state'))
    if k == peer1 and v == {'status': {'bgp_peer_state': 'Open-confirm'}}:
        print(ob_1, (k), (Back.YELLOW + 'peer is in OpenConfirm state'))
    if k == peer1 and v == {'status': {'bgp_peer_state': 'OpenSent'}}:
        print(ob_1, (k), (Back.CYAN + 'peer is in OpenSent state'))
    if k == peer1 and v == {'status': {'bgp_peer_state': 'Active'}}:
        print(ob_1, (k), (Back.BLUE + 'peer is in Active state'))
    if k == peer1 and v == {'status': {'bgp_peer_state': 'Connect'}}:
        print(ob_1, (k), (Back.MAGENTA + 'peer is in Connect state'))
    if k == peer1 and v == {'status': {'bgp_peer_state': 'Idle'}}:
        print(ob_1, (k), (Back.RED + 'peer is in Idle state'))
        beep()
    if k == peer1 and v == {'status': {"bgp_peer_state": "Connect", "bgp_sent_err_code": "Hold Timer Expired",
                                       "bgp_sent_err_sub_code": "Unspecific"}}:
        print(ob_1, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))
        beep()
    if k == peer1 and v != {'status': {'bgp_peer_state': 'Established'}}:
            print(ob_1, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Peer is UP but check Peer BGP STATUS on CLI'))


########################################################################################################################

##############################ORANGEBURG BGP PEER#2#####################################################################

def bgp_block2():
    if k == peer2 and v == {'status': {'bgp_peer_state': 'Established'}}:
        print(ob_2, (k), (Back.GREEN + Style.BRIGHT + 'peer is in Established state'))
    if k == peer2 and v == {'status': {'bgp_peer_state': 'Open-confirm'}}:
        print(ob_2, (k), (Back.YELLOW + 'peer is in OpenConfirm state'))
    if k == peer2 and v == {'status': {'bgp_peer_state': 'OpenSent'}}:
        print(ob_2, (k), (Back.CYAN + 'peer is in OpenSent state'))
    if k == peer2 and v == {'status': {'bgp_peer_state': 'Active'}}:
        print(ob_2, (k), (Back.BLUE + 'peer is in Active state'))
    if k == peer2 and v == {'status': {'bgp_peer_state': 'Connect'}}:
        print(ob_2, (k), (Back.MAGENTA + 'peer is in Connect state'))
    if k == peer2 and v == {'status': {'bgp_peer_state': 'Idle'}}:
        print(ob_2, (k), (Back.RED + 'peer is in Idle state'))
        beep()
    if k == peer2 and v == {'status': {"bgp_peer_state": "Connect", "bgp_sent_err_code": "Hold Timer Expired",
                                       "bgp_sent_err_sub_code": "Unspecific"}}:
        print(ob_2, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))
        beep()
    if k == peer2 and v != {'status': {'bgp_peer_state': 'Established'}}:
            print(ob_2, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Peer is UP but check Peer BGP STATUS on CLI'))

########################################################################################################################

#######################################MELVILLE HQ BGP PEER#############################################################
def bgp_block3():
    if k == peer3 and v == {'status': {'bgp_peer_state': 'Established'}}:
        print(mel, (k), (Back.GREEN + Style.BRIGHT + 'peer is in Established state'))
    if k == peer3 and v == {'status': {'bgp_peer_state': 'Open-confirm'}}:
        print(mel, (k), (Back.YELLOW + 'peer is in OpenConfirm state'))
    if k == peer3 and v == {'status': {'bgp_peer_state': 'OpenSent'}}:
        print(mel, (k), (Back.CYAN + 'peer is in OpenSent state'))
    if k == peer3 and v == {'status': {'bgp_peer_state': 'Active'}}:
        print(mel, (k), (Back.BLUE + 'peer is in Active state'))
    if k == peer3 and v == {'status': {'bgp_peer_state': 'Connect'}}:
        print(mel, (k), (Back.MAGENTA + 'peer is in Connect state'))
    if k == peer3 and v == {'status': {'bgp_peer_state': 'Idle'}}:
        print(mel, (k), (Back.RED + 'peer is in Idle state'))
        beep()
    if k == peer3 and v == {'status': {"bgp_peer_state": "Connect", "bgp_sent_err_code": "Hold Timer Expired",
                                       "bgp_sent_err_sub_code": "Unspecific"}}:
        print(mel, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))
        beep()
    if k == peer3 and v != {'status': {'bgp_peer_state': 'Established'}}:
            print(mel, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Peer is UP but check Peer BGP STATUS on CLI'))

#########################################################################################################################################

#######################################WINDSTREAM BGP PEER################################################################################

def bgp_block4():
    if k == peer4 and v == {'status': {'bgp_peer_state': 'Established'}}:
        print(ws, (k), (Back.GREEN + Style.BRIGHT + 'peer is in Established state'))
    if k == peer4 and v == {'status': {'bgp_peer_state': 'Open-confirm'}}:
        print(ws, (k), (Back.YELLOW + 'peer is in OpenConfirm state'))
    if k == peer4 and v == {'status': {'bgp_peer_state': 'OpenSent'}}:
        print(ws, (k), (Back.CYAN + 'peer is in OpenSent state'))
    if k == peer4 and v == {'status': {'bgp_peer_state': 'Active'}}:
        print(ws, (k), (Back.BLUE + 'peer is in Active state'))
    if k == peer4 and v == {'status': {'bgp_peer_state': 'Connect'}}:
        print(ws, (k), (Back.MAGENTA + 'peer is in Connect state'))
    if k == peer4 and v == {'status': {'bgp_peer_state': 'Idle'}}:
        print(ws, (k), (Back.RED + 'peer is in Idle state'))
        beep()
    if k == peer4 and v == {'status': {"bgp_peer_state": "Connect", "bgp_sent_err_code": "Hold Timer Expired",
                                       "bgp_sent_err_sub_code": "Unspecific"}}:
        print(ws, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))
        beep()
    if k == peer4 and v != {'status': {'bgp_peer_state': 'Established'}}:
            print(ws, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Peer is UP but check Peer BGP STATUS on CLI'))

############################################################################################################################################

############################################FISERV-DNA-1 BGP PEER###########################################################################

def bgp_block5():
    if k == peer5 and v == {'status': {'bgp_peer_state': 'Established'}}:
        print(fs_1, (k), (Back.GREEN + Style.BRIGHT +  'peer is in Established state'))
    if k == peer5 and v == {'status': {'bgp_peer_state': 'Open-confirm'}}:
        print(fs_1, (k), (Back.YELLOW + 'peer is in OpenConfirm state'))
    if k == peer5 and v == {'status': {'bgp_peer_state': 'OpenSent'}}:
        print(fs_1, (k), (Back.CYAN + 'peer is in OpenSent state'))
    if k == peer5 and v == {'status': {'bgp_peer_state': 'Active'}}:
        print(fs_1, (k), (Back.BLUE + 'peer is in Active state'))
    if k == peer5 and v == {'status': {'bgp_peer_state': 'Connect'}}:
        print(fs_1, (k), (Back.MAGENTA + 'peer is in Connect state'))
    if k == peer5 and v == {'status': {'bgp_peer_state': 'Idle'}}:
        print(fs_1, (k), (Back.RED + 'peer is in Idle state'))
        beep()
    if k == peer5 and v == {'status': {"bgp_peer_state": "Connect", "bgp_sent_err_code": "Hold Timer Expired",
                                       "bgp_sent_err_sub_code": "Unspecific"}}:
        print(fs_1, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))
        beep()
    if k == peer5 and v != {'status': {'bgp_peer_state': 'Established'}}:
            print(fs_1, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Peer is UP but check Peer BGP STATUS on CLI'))

#####################################################################################################################################

############################################FISERV-DNA-2 BGP PEER####################################################################
def bgp_block6():
    if k == peer6 and v == {'status': {'bgp_peer_state': 'Established'}}:
        print(fs_2, (k), (Back.GREEN + Style.BRIGHT +  'peer is in Established state'))
    if k == peer6 and v == {'status': {'bgp_peer_state': 'Open-confirm'}}:
        print(fs_2, (k), (Back.YELLOW + 'peer is in OpenConfirm state'))
    if k == peer6 and v == {'status': {'bgp_peer_state': 'OpenSent'}}:
        print(fs_2, (k), (Back.CYAN + 'peer is in OpenSent state'))
    if k == peer6 and v == {'status': {'bgp_peer_state': 'Active'}}:
        print(fs_2, (k), (Back.BLUE + 'peer is in Active state'))
    if k == peer6 and v == {'status': {'bgp_peer_state': 'Connect'}}:
        print(fs_2, (k), (Back.MAGENTA + 'peer is in Connect state'))
    if k == peer6 and v == {'status': {'bgp_peer_state': 'Idle'}}:
        print(fs_2, (k), (Back.RED + 'peer is in Idle state'))
        beep()
    if k == peer6 and v == {'status': {"bgp_peer_state": "Connect", "bgp_sent_err_code": "Hold Timer Expired",
                                       "bgp_sent_err_sub_code": "Unspecific"}}:
        print(fs_2, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))
        beep()
    if k == peer6 and v != {'status': {'bgp_peer_state': 'Established'}}:
            print(fs_2, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Peer is UP but check Peer BGP STATUS on CLI'))
#######################################################################################################################


############################################CONNECT ONE BANK BGP PEER####################################################################
def bgp_block7():
    if k == peer7 and v == {'status': {'bgp_peer_state': 'Established'}}:
        print(cnob, (k), (Back.GREEN + Style.BRIGHT +  'peer is in Established state'))
    if k == peer7 and v == {'status': {'bgp_peer_state': 'Open-confirm'}}:
        print(cnob, (k), (Back.YELLOW + 'peer is in OpenConfirm state'))
    if k == peer7 and v == {'status': {'bgp_peer_state': 'OpenSent'}}:
        print(cnob, (k), (Back.CYAN + 'peer is in OpenSent state'))
    if k == peer7 and v == {'status': {'bgp_peer_state': 'Active'}}:
        print(cnob, (k), (Back.BLUE + 'peer is in Active state'))
    if k == peer7 and v == {'status': {'bgp_peer_state': 'Connect'}}:
        print(cnob, (k), (Back.MAGENTA + 'peer is in Connect state'))
    if k == peer7 and v == {'status': {'bgp_peer_state': 'Idle'}}:
        print(cnob, (k), (Back.RED + 'peer is in Idle state'))
        beep()
    if k == peer7 and v == {'status': {"bgp_peer_state": "Connect", "bgp_sent_err_code": "Hold Timer Expired",
                                       "bgp_sent_err_sub_code": "Unspecific"}}:
        print(cnob, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))
        beep()
    if k == peer7 and v != {'status': {'bgp_peer_state': 'Established'}}:
            print(cnob, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Peer is UP but check Peer BGP STATUS on CLI'))
#######################################################################################################################


######START RUN###### LOGIN PROMPTS TO FOLLOW - GETPASS FUNCTION ETC###################################################
cls()
topline()
user = input('username:  ')
pwd = getpass.getpass(prompt='password:  ')
creds = {"username": user, "password": pwd}
bottomline()
login()
cls()
#####################################################################################################################

##########################MAIN PROGRAM LOOP##########################################################################
#########################REST BGP PEER STATUS CALLS##################################################################
while True:
    bgp = session.get(
       f"https://{sw1}/rest/v10.11/system/vrfs/default/bgp_routers/65999/bgp_neighbors?attributes=status&depth=2&selector=status", verify=False)
    sw_resp = (bgp.json())
    time.sleep(6)
    cls()
    pageheader()


 ####################################MAIN STATUS CHECK DECISION TREE################################################    
    print(Back.BLUE + Fore.WHITE + Style.BRIGHT +  '    LI-DC DC \u25ba SWITCH BANK-365DC-L3-SW1 \u25c4 PEER CHECK    ')
    bottomline()
    for k, v in sw_resp.items():
        bgp_block1()
        bgp_block2()
        bgp_block3()
        bgp_block4()
        bgp_block5()
        bgp_block6()
        bgp_block7()
        splitline()
    topline()
    print(Back.BLUE + Fore.WHITE + Style.BRIGHT + '    LI-DC DC \u25ba SWITCH BANK-365DC-L3-SW2 \u25c4 PEER CHECK    ')
    bottomline()
    bgp = session.get(
        f"https://{sw2}/rest/v10.11/system/vrfs/default/bgp_routers/65999/bgp_neighbors?attributes=status&depth=2&selector=status", verify=False)
    sw_resp = (bgp.json())
    for k, v in sw_resp.items():
        bgp_block1()
        bgp_block2()
        bgp_block3()
        bgp_block4()
        bgp_block5()
        bgp_block6()
        bgp_block7()
        splitline()
    bottomline()
    footer()
 ############################################################################################################################  


###############################################CLEANUP#######################################################################
    # sw_resp.clear()

##############################################END RUN#######################################################################



#########################################EXTRAS##############################################################################

