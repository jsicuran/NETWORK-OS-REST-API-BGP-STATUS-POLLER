A DevOps application for a client to track the BGP peering status of critical financial services vendor partner peer links. Utilizes RESTful API BGP calls to the devices for peering status. 

Complements current NMS systems and provides improved observability on NOC dashboard. 

This application provides a “DEFCON” level/color type indicator peer BGP peering state

Provides NOC staff ability to quickly validate that the peer is experiencing an issue while the physical link to the BGP peer is may still indicate a “Green UP” displayed other NMS systems portals.

The application is Python based utilizing various RESTful API and JSON libraries for the for formatting prior presenting to the NOC user. It was porotype and tested using Swagger for ArubaOS-CX as well as Postman for returned data set validation. 

This is small and simple version of the application that is a hard coded to point to specific BGP devices. There is limited error correction and it is a non-HTTPS cookie version using single SSH based single login.  

Code is included for DELL OS10 switch REST API as well that utilizes differnt URL and schema to traverse.

A GUI version will be available soon that utilizes improved error correction, adding additional peers and REST cookie use for secure single sign on use. 
Both GUI/Text versions can be “complied” for use as a single executable file. 
Can be used as part of an automation tool or code can be integrated into other automation tools/code. 
I may add a Python send mail module to send an email when the status changes to Idle.
