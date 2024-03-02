###########################################################################
### SOME REST API QUERIES VIS HP ARUBAOS-CX SWAGGAR TOOL AND POSTMAN      #
### USED TO WHITTLE DOWN BGP STATUS                                       #
###########################################################################


*#**************************PERFECT***************************
https://192.168.1.254/rest/v10.13/system/vrfs/default/bgp_routers/65001/bgp_neighbors?attributes=status&depth=2&selector=status
{
  "192.168.1.253": {
    "status": {
      "bgp_peer_state": "Idle"
    }
  }
}


{
  "192.168.1.254": {
    "status": {
      "bgp_peer_state": "Established"
    }
  }
}






https://192.168.1.254/rest/v10.04/system/vrfs/default/bgp_routers/65001/bgp ------> just returns single line neighbors
https://192.168.1.254/rest/v10.04/system/vrfs/default/bgp_routers/65001/bgp_neighbors?depth=2&selector=status

**********good detailed quiery*********************************************************************
https://192.168.1.254/rest/v10.04/system/vrfs/default/bgp_routers/*/bgp_neighbors/*?attributes=status
Returns 
{
    "default": {
        "65001": {
            "1.1.1.1": {
                "status": {
                    "bgp_peer_state": "Idle"
                }
            }
        }
    }
}

*********************************************************************************EXCELLENT**********************************************
https://192.168.1.210/rest/v10.11/system/vrfs/default/bgp_routers/65001/bgp_neighbors?attributes=status&depth=2&selector=status

{
  "192.168.1.211": {
    "status": {
      "bgp_peer_state": "Established"
    }
  }
}
********************************************************************************************************************************************

*******************************************************************************************



https://192.168.1.254/rest/v10.04/system/vrfs/default/bgp_routers/*/bgp_neighbors/*?attributes=status"                                                



***********************Try at bank on rest v10.11***************************************************************
https://192.168.1.254/rest/v10.04/system/vrfs/default/bgp_routers/65001/bgp_neighbors?depth=2&filter=bgp_peer_state:Idle
https://192.168.1.254/rest/v10.04/system/vrfs/default/bgp_routers/65001/bgp_neighbors?depth=2&filter=status:Idle
https://192.168.1.254/rest/v10.04/system/vrfs/default/bgp_routers/65001/bgp_neighbors?depth=2&attributes=status,bgp_peer_state
https://192.168.1.254/rest/v10.04/system/vrfs/default/bgp_routers/65001/bgp_neighbors/*?depth=2&attributes=status
https://192.168.1.254/rest/v10.04/system/vrfs/default/bgp_routers/65001/bgp_neighbors/*?depth=2&attributes=bgp_peer_state:

****************************************************************************************************************************

##############FULL JSON CONVERTED RETRUNED DICTIONARY ###############################



1.1.1.1": {
        "ORF_capability": {},
        "ORF_prefix_list": {},
        "ORF_received_prefix_list": {},
        "activate": {
            "ipv4-unicast": false,
            "ipv6-unicast": false,
            "l2vpn-evpn": false
        },
        "add_paths": {
            "ipv4-unicast": "disable",
            "ipv6-unicast": "disable"
        },
        "add_paths_adv_best_n": {
            "ipv4-unicast": 1,
            "ipv6-unicast": 1
        },
        "advertisement_interval": {},
        "af_status": {},
        "allow_as_in": {},
        "aspath_filters": {},
        "bfd_enable": false,
        "bgp_peer_group": null,
        "capabilites_recevied": [],
        "capabilites_sent": [],
        "default_originate": {
            "ipv4-unicast": false,
            "ipv6-unicast": false
        },
        "default_originate_route_map": {},
        "description": null,
        "ebgp_hop_count": 1,
        "fall_over": false,
        "gshut": {
            "local_pref": 0,
            "timer": 180
        },
        "gshut_status": null,
        "inbound_soft_reconfiguration": {
            "ipv4-unicast": false,
            "ipv6-unicast": false
        },
        "is_peer_group": false,
        "last_shutdown_time": null,
        "local_as": null,
        "local_as_mode": "none",
        "local_interface": null,
        "max_prefix_options": {},
        "negotiated_add_paths": {
            "ipv4-unicast": "disable",
            "ipv6-unicast": "disable"
        },
        "negotiated_holdtime": 0,
        "negotiated_keepalive": 0,
        "next_hop_self": {
            "ipv4-unicast": false,
            "ipv6-unicast": false
        },
        "next_hop_unchanged": {
            "l2vpn-evpn": false
        },
        "passive": false,
        "password": null,
        "peer_rtrid": "0.0.0.0",
        "prefix_lists": {},
        "remote_as": 65002,
        "remove_private_as": false,
        "route_maps": {},
        "route_reflector_client": {
            "ipv4-unicast": false,
            "ipv6-unicast": false,
            "l2vpn-evpn": false
        },
        "sel_local_port": 0,
        "sel_remote_port": 0,
        "send_community": {
            "ipv4-unicast": "none",
            "ipv6-unicast": "none",
            "l2vpn-evpn": "none"
        },
        "shutdown": false,
        "statistics": {
            "bgp_peer_dropped_count": 0,
            "bgp_peer_established_count": 0,
            "bgp_peer_keepalive_in_count": 0,
            "bgp_peer_keepalive_out_count": 0,
            "bgp_peer_notify_in_count": 0,
            "bgp_peer_notify_out_count": 0,
            "bgp_peer_open_in_count": 0,
            "bgp_peer_open_out_count": 0,
            "bgp_peer_refresh_in_count": 0,
            "bgp_peer_refresh_out_count": 0,
            "bgp_peer_update_in_count": 0,
            "bgp_peer_update_out_count": 0,
            "bgp_peer_uptime": 0
        },
        "status": {
            "bgp_peer_state": "Idle"
        },
        "tcp_port_number": null,
        "timers": {
            "connect-retry": 120,
            "holdtime": 180,
            "keepalive": 60
        },
        "ttl_security_hops": null,
        "update_source": null,
        "vsx_sync_exclude": null,
        "weight": 0
    }
}