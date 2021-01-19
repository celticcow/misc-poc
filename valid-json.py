#!/usr/bin/python3

import json

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except json.decoder.JSONDecodeError as err:
        print(err)
        return(False)
    
    return(True)


def main():
    json1 = {
        "name" : "jane doe",
        "salary" : 9000,
        "email" : "jane@doe",
    } 

    json2 = {
        "name" : "john doe",
        "salary" : 8500,
        "email" : "john@doe"
    }

    print(validateJSON(str(json1)))
    print(validateJSON(str(json2)))

if __name__ == "__main__":
    main()