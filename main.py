# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os
from os import listdir
from os.path import isfile, join
import urllib3

import requests
import http.client



def getTokenClient(tentnid,appid,clientsecret):

    try:

        url = f"https://login.microsoftonline.com/{tentnid}/oauth2/token"

        payload = f'grant_type=client_credentials&client_id={appid}&client_secret={clientsecret}&resource=https%3A%2F%2Fmanagement.azure.com%2F'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        res = json.loads(response.text)

    except Exception as e:
         print(e)
    return res["access_token"]


def gettokenclient(tentnid,appid,clientsecret):

    try:
        conn = http.client.HTTPSConnection("login.microsoftonline.com")
        payload = f"grant_type=client_credentials&client_id={appid}&client_secret={clientsecret}&resource=https%3A%2F%2Fmanagement.azure.com%2F"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',

        }
        conn.request("POST", f"/{tentnid}/oauth2/token", payload, headers)
        res = conn.getresponse()
        data = res.read()
        resposnesTxt=data.decode("utf-8")
        res = json.loads(resposnesTxt)
        print(res)
        print(res["access_token"])
    except Exception as e:
        print(e)
    return res["access_token"]

# Press the green button in the gutter to run the script.

def getlistoffiles(mypath,objectType,bearer,subscriptionid):
    folders = [f for f in listdir(mypath) if  os.path.isdir(join(mypath, f)) and f==objectType  ]
    for folder in folders :
        print(folder)
        print('---')
        files=listdir(join(mypath, folder))
        for file in files:
          print(file)
          f = open( join(join(mypath, folder),file), "r")
          res = json.loads(f.read())
          listofdicts=res["value"]
          for dict in   listofdicts:
              objcetName=dict["name"]
              print(objcetName)
              if "properties" in dict:
                  if "connectVia" in dict["properties"]:
                      print(f'remove key connectVia:{dict["properties"]["connectVia"]}')
                      dict["properties"].pop('connectVia', None)

              publishobjectClinet(subscriptionid, resourceGroup, factoryname, folder, objcetName, dict, bearer)




def publishobjectClinet(subscriptionid,resourceGroup,factory,objectType,objectName,dict,bearer):


    conn = http.client.HTTPSConnection("management.azure.com")
    payload = json.dumps(dict)
    headers = {
        'Authorization': 'Bearer  '  +bearer,
        'Content-Type': 'application/json'
    }
    conn.request("PUT",
                 f"/subscriptions/{subscriptionid}/resourceGroups/{resourceGroup}/providers/Microsoft.DataFactory/factories/{factory}/{objectType}/{objectName}?api-version=2018-06-01"
                 .replace(" ","%20"),
                 payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))



tenantid="fbb6a85c-fb76-4fe5-9893-abd1eace5774"
appid="33fb8409-1e84-4aa1-b322-771fb96b4ded"
clientsecret="QkT8Q~rhbaTKDYwuCJAXnkLJqOsOwmeiO7v8tb51"
resourceGroup="octopaidevops"
factoryname="Waves"
subscriptionid="772a05fa-8add-4975-84a3-96ce16f81016"


bearer= getTokenClient(tenantid,appid,clientsecret)

listoftype=['LinkedServices','DataFlows','DataSets','pipelines']


for objecttype in listoftype:
    try:
        getlistoffiles("E:\\tmp\\BW\\ADF_106_DFCloudiaX-test_2023-4-25-13-54-4\\ADF\\DFCloudiaX-test\\rg-data-factories",objecttype,bearer,subscriptionid)
    except Exception as e:
        print(e)



