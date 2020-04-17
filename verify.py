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

def get_policies(ip_addr,sid):
    get_package_result = apifunctions.api_call(ip_addr,"show-packages", {"details-level" : "full"}, sid)

    policy_select = {}
    policy_index = 0 # things should start 0

    for i in range(get_package_result['total']):
        size_of_package = len(get_package_result['packages'][i]['access-layers'])
        for j in range(size_of_package):
            current_name = get_package_result['packages'][i]['access-layers'][j]['name']
            if((current_name == "FDX_Services Security") or ("Application" in current_name) or (current_name == "Network")):
                pass
            else:
                #print(current_name)
                policy_select[policy_index] = current_name
                policy_index = policy_index + 1

    print(policy_select)
    return(policy_select)
#end of get_policies

def main():
    #
    debug = 1

    print("Verify Me")

    ip_addr  = "146.18.96.16" #args.m
    ip_cma   = "146.18.96.25" #args.c
    user     = "roapi"
    password = "1qazxsw2"

    policies_dic = {}

    sid = apifunctions.login(user,password, ip_addr, ip_cma)

    if(debug == 1):
        print("session id : " + sid)

    policies_dic = get_policies(ip_addr, sid)

    if(debug == 1):
        print("**************")
        print(policies_dic)
        print("**************")
    
    ### Json to Verify a Policy ###
    verify_policy = {
        "policy-package" : "SearchTest"   #SearchTest
    }

    ## result will be a task ID
    verify_result = apifunctions.api_call(ip_addr, "verify-policy", verify_policy, sid)

    print(json.dumps(verify_result))

    #get task ID
    task_id = verify_result['task-id']

    #get task info ... lot of stuff in here
    task_info = apifunctions.api_call(ip_addr, "show-task", {"task-id" : task_id}, sid)

    #status is deceptive can be 
    # "status": "succeeded"
    # "status": "failed"
    # "status": "in progress"
    status = task_info['tasks'][0]['status']

    #better measure if done or not.   will be int from 0 - 100
    percent = task_info['tasks'][0]['progress-percentage']
    print(percent)
    
    while(percent != 100):
        print("In progress")

        time.sleep(1)
        
        task_info = apifunctions.api_call(ip_addr, "show-task", {"task-id" : task_id}, sid)  #, "details-level" : "full"
        status = task_info['tasks'][0]['status']
        percent = task_info['tasks'][0]['progress-percentage']

        print(status)
        print(json.dumps(task_info))
        print(percent)
        print("/////////////////////////////////////")
    #end of while loop

    print(json.dumps(task_info))

    
    # don't need to publish
    time.sleep(20)

    ### logout
    logout_result = apifunctions.api_call(ip_addr, "logout", {}, sid)
    if(debug == 1):
        print(logout_result)
#endof main()

if __name__ == "__main__":
    main()
