###################################################################################
#                        Color Code BGP Peer State Monitor                        #   
# Monitors BGP peer 6 connections state status and displays color code per state  #
# Simple Text version - with no error handling yet - not pythonic or elegant      #
# GUI and REST Cookie use version forthcoming based on Framework selected         #
# Usage - run from command line or "compiled" then login and leave alone          #
# Coded for specific devices ONLY - for client's use                              #
# Not interactive use Crtl + C to exit anytime                                    #
# IDE(PyCharm)/(VS CODE) based and complied runtime versions available            #
# For ArubaOS-CX rest api call use                                                #
#                                                                                 #
#                        Dual switch version                                      #
#                         2/20/2024   V1.0                                        #
#                         3/1/2024    V1.1                                        #      
#                                                                                 #
#2024 Appplied Methodologeis, inc                                                 #
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
from colorama import just_fix_windovsb_console, Fore, Back, Style
from colorama import init
import fixpath
import pyfiglet
import datetime
import winsound
############################################################################################################

###############################INITS, GLOBALS AND OTHER STARTUPS############################################
init(autoreset=True)
just_fix_windovsb_console()
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



##########################REST API ENDPOINTS ######################################################

######REST API LOGIN ENDPOINT TABLE#################################################################
sw1 = "192.168.1.210"
sw2 = "192.168.1.211"



#####################################################################################################

##########PEER ENDPOINT NAME TABLE#################
site_a = "DC-SW1 \u25ba "
site_b = "DC-SW2 \u25ba "
fs_1 =   "Finance 1  \u25ba "
fs_2 =   "Finance 2  \u25ba "
vsa =    "Vendor site a   \u25ba "
vsb =    "Vendor site b    \u25ba "
###################################################

########BGP NEIGHBOR PEER STATUS ENDPOINT TABLE###############
peer1 = '1.1.1.1'  ####  mock neighbor to someplace 
peer2 = '2.2.2.2'  ####  mock neighbor to someplace 
peer3 = '3.3.3.3'  ####  mock neighbor to someplace 
peer4 = '4.4.4.4' ####  mock neighbor to someplace 
peer5 = '5.5.5.5' ####  mock neighbor to someplace 
peer6 = '6.6.6.6' ####  mock neighbor to someplace 
###############################################################



##################### GENERAL FUNCTION DEFINITIONS####################################################

def cls():
    os.system('cls')

def beep():
    winsound.Beep(3000, 500)

def banner():
    result = pyfiglet.figlet_format("            C L I E N T ", font="slant")
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

def login():
    login = session.post(f"https://{sw1}/rest/v10.11/login", data=creds, verify=False)
    print(f"This is the DC-L3-SW1 login code: {login.status_code} - OK!")
    print(Fore.GREEN + Style.BRIGHT + "\u2591" * 165)
    time.sleep(3)
    login = session.post(f"https://{sw2}/rest/v10.11/login", data=creds, verify=False)
    print(f"This is the DC-L3-SW2 login code: {login.status_code} - OK!")
    print(Fore.GREEN + Style.BRIGHT + "\u2591" * 165)
    time.sleep(3)
  
def logout():
    logout = session.post(f"https://{sw1}/rest/v10.11/logout")
    print(Fore.GREEN + Style.BRIGHT + "\u2591" * 165)
    print(f"This is the DC-L3-SW2 logout code: {logout.status_code} - Goodbye!")
    time.sleep(3)
    logout = session.post(f"https://{sw2}/rest/v10.11/logout")
    print(Fore.GREEN + Style.BRIGHT + "\u2591" * 165)
    print(f"This is the DC-L3-SW2 logout code: {logout.status_code} - Goodbye!")
    time.sleep(3)

################################################LOAD PAGE HEADER################################################

def pageheader():
    topline()
    banner()
    bottomline()
################################################################################################################
    
    
##################################START CHECKING PEER STATUS####################################################

################################################################################################################

##############################SITE A BGP PEER#1#############################################################
def bgp_block1():
    if k == peer1 and v == {'status': {'bgp_peer_state': 'Established'}}:
        print(site_a, (k), (Back.GREEN + Style.BRIGHT + 'peer is in Established state'))
    if k == peer1 and v == {'status': {'bgp_peer_state': 'Open-confirm'}}:
        print(site_a, (k), (Back.YELLOW + 'peer is in OpenConfirm state'))
    if k == peer1 and v == {'status': {'bgp_peer_state': 'OpenSent'}}:
        print(site_a, (k), (Back.CYAN + 'peer is in OpenSent state'))
    if k == peer1 and v == {'status': {'bgp_peer_state': 'Active'}}:
        print(site_a, (k), (Back.BLUE + 'peer is in Active state'))
    if k == peer1 and v == {'status': {'bgp_peer_state': 'Connect'}}:
        print(site_a, (k), (Back.MAGENTA + 'peer is in Connect state'))
    if k == peer1 and v == {'status': {'bgp_peer_state': 'Idle'}}:
        print(site_a, (k), (Back.RED + 'peer is in Idle state'))
        beep()
    if k == peer1 and v == {'status': {"bgp_peer_state": "Connect", "bgp_sent_err_code": "Hold Timer Expired",
                                       "bgp_sent_err_sub_code": "Unspecific"}}:
        print(site_a, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))
        beep()


########################################################################################################################

##############################SITE B BGP PEER#2#####################################################################

def bgp_block2():
    if k == peer2 and v == {'status': {'bgp_peer_state': 'Established'}}:
        print(site_b, (k), (Back.GREEN + 'peer is in Established state'))
    if k == peer2 and v == {'status': {'bgp_peer_state': 'Open-confirm'}}:
        print(site_b, (k), (Back.YELLOW + 'peer is in OpenConfirm state'))
    if k == peer2 and v == {'status': {'bgp_peer_state': 'OpenSent'}}:
        print(site_b, (k), (Back.CYAN + 'peer is in OpenSent state'))
    if k == peer2 and v == {'status': {'bgp_peer_state': 'Active'}}:
        print(site_b, (k), (Back.BLUE + 'peer is in Active state'))
    if k == peer2 and v == {'status': {'bgp_peer_state': 'Connect'}}:
        print(site_b, (k), (Back.MAGENTA + 'peer is in Connect state'))
    if k == peer2 and v == {'status': {'bgp_peer_state': 'Idle'}}:
        print(site_b, (k), (Back.RED + 'peer is in Idle state'))
        beep()
    if k == peer2 and v == {'status': {"bgp_peer_state": "Connect", "bgp_sent_err_code": "Hold Timer Expired",
                                       "bgp_sent_err_sub_code": "Unspecific"}}:
        print(site_b, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))
        beep()

########################################################################################################################

#######################################VSA BGP PEER#############################################################
def bgp_block3():
    if k == peer3 and v == {'status': {'bgp_peer_state': 'Established'}}:
        print(vsa, (k), (Back.GREEN + 'peer is in Established state'))
    if k == peer3 and v == {'status': {'bgp_peer_state': 'Open-confirm'}}:
        print(vsa, (k), (Back.YELLOW + 'peer is in OpenConfirm state'))
    if k == peer3 and v == {'status': {'bgp_peer_state': 'OpenSent'}}:
        print(vsa, (k), (Back.CYAN + 'peer is in OpenSent state'))
    if k == peer3 and v == {'status': {'bgp_peer_state': 'Active'}}:
        print(vsa, (k), (Back.BLUE + 'peer is in Active state'))
    if k == peer3 and v == {'status': {'bgp_peer_state': 'Connect'}}:
        print(vsa, (k), (Back.MAGENTA + 'peer is in Connect state'))
    if k == peer3 and v == {'status': {'bgp_peer_state': 'Idle'}}:
        print(vsa, (k), (Back.RED + 'peer is in Idle state'))
        beep()
    if k == peer3 and v == {'status': {"bgp_peer_state": "Connect", "bgp_sent_err_code": "Hold Timer Expired",
                                       "bgp_sent_err_sub_code": "Unspecific"}}:
        print(vsa, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))
        beep()

#########################################################################################################################################

#######################################VSB BGP PEER################################################################################

def bgp_block4():
    if k == peer4 and v == {'status': {'bgp_peer_state': 'Established'}}:
        print(vsb, (k), (Back.GREEN + 'peer is in Established state'))
    if k == peer4 and v == {'status': {'bgp_peer_state': 'Open-confirm'}}:
        print(vsb, (k), (Back.YELLOW + 'peer is in OpenConfirm state'))
    if k == peer4 and v == {'status': {'bgp_peer_state': 'OpenSent'}}:
        print(vsb, (k), (Back.CYAN + 'peer is in OpenSent state'))
    if k == peer4 and v == {'status': {'bgp_peer_state': 'Active'}}:
        print(vsb, (k), (Back.BLUE + 'peer is in Active state'))
    if k == peer4 and v == {'status': {'bgp_peer_state': 'Connect'}}:
        print(vsb, (k), (Back.MAGENTA + 'peer is in Connect state'))
    if k == peer4 and v == {'status': {'bgp_peer_state': 'Idle'}}:
        print(vsb, (k), (Back.RED + 'peer is in Idle state'))
        beep()
    if k == peer4 and v == {'status': {"bgp_peer_state": "Connect", "bgp_sent_err_code": "Hold Timer Expired",
                                       "bgp_sent_err_sub_code": "Unspecific"}}:
        print(vsb, (k), (Back.WHITE + Fore.BLACK + Style.BRIGHT + 'Check Peer Physical Interface and Circuit'))
        beep()

############################################################################################################################################

############################################FS_1 BGP PEER###########################################################################

def bgp_block5():
    if k == peer5 and v == {'status': {'bgp_peer_state': 'Established'}}:
        print(fs_1, (k), (Back.GREEN + 'peer is in Established state'))
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

#####################################################################################################################################

############################################FS_2 BGP PEER####################################################################
def bgp_block6():
    if k == peer6 and v == {'status': {'bgp_peer_state': 'Established'}}:
        print(fs_2, (k), (Back.GREEN + 'peer is in Established state'))
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
       f"https://{sw1}/rest/v10.11/system/vrfs/default/bgp_routers/65001/bgp_neighbors?attributes=status&depth=2&selector=status", verify=False)
    sw_resp = (bgp.json())
    time.sleep(6)
    cls()
    pageheader()


 ####################################MAIN STATUS CHECK DECISION TREE################################################    
    print(Back.BLUE + Fore.WHITE + Style.BRIGHT +  '    DC-SITE \u25ba SWITCH DC-L3-SW1 \u25c4 PEER CHECK    ')
    bottomline()
    for k, v in sw_resp.items():
        bgp_block1()
        bgp_block2()
        bgp_block3()
        bgp_block4()
        bgp_block5()
        bgp_block6()
        splitline()
    topline()
    print(Back.BLUE + Fore.WHITE + Style.BRIGHT + '     DC-SITE \u25ba SWITCH DC-L3-SW2 \u25c4 PEER CHECK    ')
    bottomline()
    bgp = session.get(
        f"https://{sw2}/rest/v10.11/system/vrfs/default/bgp_routers/65001/bgp_neighbors?attributes=status&depth=2&selector=status", verify=False)
    sw_resp = (bgp.json())
    for k, v in sw_resp.items():
        bgp_block1()
        bgp_block2()
        bgp_block3()
        bgp_block4()
        bgp_block5()
        bgp_block6()
        splitline()
    bottomline()
    footer()
 ############################################################################################################################  


###############################################CLEANUP#######################################################################
    # sw_resp.clear()

##############################################END RUN#######################################################################



#########################################EXTRAS##############################################################################

