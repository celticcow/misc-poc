#!/usr/bin/python3 -W ignore::DeprecationWarning

import requests
import json
import sys
import time
import argparse
import apifunctions

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
gregory.dunlap / celtic_cow

"""

"""
mgmt_cli -r true -d 146.18.96.25 show objects order.1.ASC "name" in.1 "name" in.2 "FXG-Office-VRF" details-level full --format json
"""

def object_is_locked(ip_addr, name, sid):
    print("in object_is_locked()")

    check_object = {
        "order" : [{"ASC" : "name"}], 
        "in" : ["name", name],
        "details-level" : "full"      
    }
    
    obj_result = apifunctions.api_call(ip_addr, "show-objects", check_object, sid)

    print(json.dumps(obj_result))

    print("\n\n")
    
    if(obj_result['objects'][0]['meta-info']['lock'] == "unlocked"):
        return True
    else:
        return False

"""
main 
"""
def main():
    print("starting main")

    debug = 1

    ip_addr   = "146.18.96.16" #input("enter IP of MDS : ")
    ip_cma    = "146.18.96.25" #input("enter IP of CMA : ")
    user      = "gdunlap" #input("enter P1 user id : ")
    password  = "1qazxsw2" #getpass.getpass('Enter P1 Password : ')

    sid = apifunctions.login(user, password, ip_addr, ip_cma)

    if(debug == 1):
        print("session id : " + sid)

    if(object_is_locked(ip_addr, "dc-test-hot", sid)):
        print("Proceed")
    else:
        print("Object Locked !!!!!")

    ### publish
    print("Start of Publish ... zzzzzz")
    time.sleep(20)
    publish_result = apifunctions.api_call(ip_addr, "publish", {}, sid)
    print("publish results : " + json.dumps(publish_result))

    time.sleep(20)

    ### logout
    logout_result = apifunctions.api_call(ip_addr, "logout", {}, sid)
    if(debug == 1):
        print(logout_result)


#end of main

if __name__ == "__main__":
    main()
#end of program