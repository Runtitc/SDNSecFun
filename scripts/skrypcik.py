from time import sleep
import FLRequester
import json
 
#from modules import mconn
import mconn #the class that makes connections and select form the db

def createflowdelete(ip_src, condition):
    flow = {
        "src-ip": ip_src+"/32", 
        "dst-ip": "any", 
        "nw-proto":"ICMP",
        "tp-src":"5010", 
        "action":condition 
    }
    return flow
 
path = {
    'enableFirewall': '/wm/firewall/module/enable/json',
    'disableFirewall': '/wm/firewall/module/disable/json',
    'firewall': '/wm/staticflowpusher/json',
    'firewall_mgmt_flow': '/wm/firewall/rules/json',
}
flow_allow = {"switchid": "00:00:00:00:00:00:00:01"}



flr = FLRequester.FLRequester("127.0.0.1:8080")
#flr.set('', "GET", "/wm/core/controller/switches/json")
DPIDS = flr.getDPID()



## STATIC ASSUMPTION, H1 (attacker) -- SW -- H2 (Web Serwer)
#                                      |
#                                      H2

#TODO: defining initial flow in SW, forward traffic from port 1 (attacker), to H2 (Web Server) 
#DONE
flr.addBasicFlow(1, 2)
flr.addBasicFlow(2, 1)
print "Flow 1-2, 2-1 added."


# TODO : fetching infomraiton from the snortdb 
# DONE
conn = mconn.Mconn("localhost")

# TODO fetching informaiton regarding created hosts
#print "Fetching hosts: \n"
#flr.fetchHosts()

while True:
    aggressor = conn.shAggressor()
    sleep(3)
    for i in range(len(aggressor['aggressorIP'])):
        print "SRC IP",aggressor['aggressorIP'][i]
        print " Count:",aggressor['aggrCount'][i]

        if aggressor['aggrCount'][i] >= 5:
            # if aggressor IP is an IP of the server itself, then do block the traffic form it
            if aggressor['aggressorIP'][i] != "10.0.0.2":
                flr.redirectToHP(aggressor['aggressorIP'][i])

 
conn.closecnx()
