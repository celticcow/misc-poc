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
def main():
    #
    debug = 0

    print("Push Policy")

    ip_addr  = "146.18.96.16" #args.m
    ip_cma   = "146.18.96.25" #args.c
    user     = "user_id" #needs actual user
    password = "leftblank"

    sid = apifunctions.login(user,password, ip_addr, ip_cma)

    if(debug == 1):
        print("session id : " + sid)

    # mgmt_cli -r true -d 146.18.96.25 install-policy 
    #     policy-package "HubLab" access true targets.1 "hublab-bd70" --format json

    policy_json = {
        "policy-package" : "HubLab",
        "access" : "true",
        "targets" : [ "hublab-bd70" ]
    }

    push_result = apifunctions.api_call(ip_addr, "install-policy", policy_json, sid)

    #get task ID
    task_id = push_result['task-id']

    #get task info ... lot of stuff in here
    task_info = apifunctions.api_call(ip_addr, "show-task", {"task-id" : task_id, "details-level" : "full"}, sid)

    #better measure if done or not.   will be int from 0 - 100
    percent = task_info['tasks'][0]['progress-percentage']
    print(percent)
    
    while(percent != 100):
        print("--In progress--")

        time.sleep(1)
        
        task_info = apifunctions.api_call(ip_addr, "show-task", {"task-id" : task_id, "details-level" : "full"}, sid)  #, "details-level" : "full"
        status = task_info['tasks'][0]['status']
        percent = task_info['tasks'][0]['progress-percentage']

        print(status)
        if(debug == 1):
            print(json.dumps(task_info))
        print(percent)
        print("/////////////////////////////////////")
    #end of while loop

    if(debug == 1):
        print(json.dumps(task_info))

    task_len = len(task_info['tasks'][0]['task-details'])
    
    if(debug == 1):
        print(task_len)

    for x in range(task_len):
        if(task_info['tasks'][0]['task-details'][x]['cluster'] == True):
            print("*^*^*^*^*^")
            print(task_info['tasks'][0]['task-details'][x]['stagesInfo'])


    # don't need to publish
    time.sleep(20)

    ### logout
    logout_result = apifunctions.api_call(ip_addr, "logout", {}, sid)
    if(debug == 1):
        print(logout_result)
#end of main()

if __name__ == "__main__":
    main()