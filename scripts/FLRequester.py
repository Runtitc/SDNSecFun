'''
This class describes the communication between main script and Floodlight REST API
'''

#import httplib
import requests # because it seems to better understand JSON response body
import json
import ast
import os

class FLRequester:
    def __init__(self, server):
        #definition of the controller address
        self.server = server


    def set(self, data, mode, path):
        if mode=="GET":
            ret = self.rest_call_get(data, mode, path )
        elif mode=="POST":
            pass
        #print ret
        return ret

    def rest_call_get(self, data, action, path):
    
        if data!="":
            headers ={
                'Content-type': 'application/json',
                'Accept': 'application/json',
            }
            print "naglowki JSON ustawione.."
            body = json.dumps(data)
        
        else:
            print "naglowki zwykle ustawione.. "
            body =""
            #headers = {
            #    'Content-type': 'text/plain',
            #}

        URI = "http://"+self.server+path
        print URI
        r = requests.get("http://"+self.server+path)
    

        if r.status_code == 200:
            # good, let's have a fun
            
            if "application/json" in r.headers['Content-Type']:
                print "INFO: APP/JSON detected"
                jsonResp = r.json()
                print len(r.json())
                print r.json()[0]
                print r.json()[0]["switchDPID"]
            else:
                print "appjson not detected"
        else:
            return 0
            print "ERROR:Response code - "+str(r.status_code)

    def getDPID(self):
        URL = "http://" + self.server + "/wm/core/controller/switches/json"
        r = requests.get(URL)
        if r.status_code==200:
            #print r.json()
            dpids = []
            for dpid in r.json():
                dpids.append( dpid["switchDPID"] )
                #print dpid.json()[0]["switchDPID"]
                #dpids.append(dpid[0]["switchDPID"]) 
            return dpids
        else:
            return "0"

    def addBasicFlow(self, inport, outport):
        URL = "http://" + self.server + "/wm/staticflowpusher/json"
        dpid = self.getDPID()
        flow = {
            "switch": dpid[0],      
            "name":"normal-drain"+str(inport)+str(outport), 
            "priority":"10",
            "active":"true", 
            "in_port":str(inport),
            "actions":"output="+ str(outport)}

        #print "Flow <" + str(inport) +", " + str(outport) + "> added. \n"
        r = requests.post(URL, json=flow)
        #return r
        #os.system("ovs-ofctl add-flow S0 priority=10,action=normal")


    def redirectToHP(self, sourceIP):
        URL = "http://" + self.server + "/wm/staticflowpusher/json"
        dpid=self.getDPID()
        flow = {
        "switch": dpid[0],
        "name":"flow-"+str(sourceIP[-1:]),
        "priority":"32768",
        "in_port":"1",
        "active":"true",
        #"eth_dst":"6a:5a:f7:63:c8:ac", 
        "ipv4_src":sourceIP, 
        "ipv4_dst":"10.0.0.2", 
        "actions":"drop"}

        print "DENY flow <from IP>:" + str(sourceIP)
        #r = requests.post(URL, json=flow)
        os.system("ovs-ofctl add-flow S0 priority=11,dl_type=0x0800,nw_src="+sourceIP+",action=3")
        #print r.status_code
        #return r
'''
    def fetchHosts(self):
        r = requests.get(URL)
        if r.status_code==200:

            hIpV4 = []
            hToSwPort = []
            mac = []

            dictHosts = {
                "hip4":hIpV4,
                "h2swp":hToSwPort,
                "mac":mac,
                }
            for host in r.json():
                try:
                    print host["ipv4"][0]
                except IndexError:
                    print "unassigned"+str(host)
                
                print host["mac"][0]
                #print host["attachmentPoint"][0]["port"]
                dictHosts["mac"].append(host["mac"][0])
                #dictHosts["hip4"].append(host["ipv4"][0])
                dictHosts["h2swp"].append(host["attachmentPoint"][0]["port"])
                
#flr = FLRequester("127.0.0.1:8080")
#flr.set('', "GET", "/wm/core/controller/switches/json")
'''