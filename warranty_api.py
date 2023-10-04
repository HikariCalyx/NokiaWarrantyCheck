#!/usr/bin/python3
# HCTSW Care OSTRemote 2 Warranty Program for Python 3.x
# 2015-2023 (C) Hikari Calyx Tech. All Rights Reserved.
from flask import request, Blueprint
import json
import time
import requests
from datetime import datetime as zdt
import pycountry

# Configuration
upstream_api_url = 'https://replace_it_with.actualdomain_of_triple_color_company.com/api/Program/validateImeiForProgram'
upstream_api_url2 = 'https://www.nokia.com/phones/en_int/support/api/imei'
referer_url = 'https://www.nokia.com/phones/en_int/support/topics/imei-checker'
x_api_key = 'replace_it_with_actual_x_api_key_you_have_found'
redirect_tccserver_hdr = {
    'Content-Type': 'application/json', 'x-api-key': x_api_key}
redirect_tccserver_hdr2 = {
    'Content-Type': 'application/json', 'referer': referer_url, 'User-Agent': 'OSTRemote2-00001111/1.0'}

exampleData = {"data": {"product": "0000000000000","productName": "Example","serial": "0000000","status": "SH","IMEI": "000000000000000","countryCode": "US","countryDesc": "USA","sdfDesc": "Standard warranty code","shipDate": "2017-07-30","warstart": "2017-07-30","wed": "2018-10-29"}}
invalidData = {"data": {"productName": None}}
cooldownData = {"data": {"productName": 'isCoolDown'}}

invalidImeiValue = ['004400152020002', '123456789012347', '000000000000000', '135790246811220']

warranty = Blueprint('warranty', __name__)


def currenttime():
    return(zdt.now().strftime('%Y-%m-%d %H:%M:%S'))

def ctime():
    return(zdt.now())

def timedelta(a, b):
    return((b - a).seconds)

def isCooldown(xSrcIP):
    if timedelta(xSrcIP, ctime()) <= 30:
        return(True)
    else:
        del(xSrcIP)
        return(False)

def cut(obj, sec):
    return [obj[i:i+sec] for i in range(0, len(obj), sec)]

def transfer_to_dict(self, data):
    listdata = data.split("&")
    properties = {}
    for line in listdata:
        if line.find("=") > 0:
            strs = line.replace("\n", "").replace("\t|\n", "").split("=")
            properties[strs[0]] = strs[1]
    return properties

def isImeiValid(imei):
    imei_number = cut(imei, 1)
    imei_n2_x2 = int(imei_number[1]) * 2
    imei_n4_x2 = int(imei_number[3]) * 2
    imei_n6_x2 = int(imei_number[5]) * 2
    imei_n8_x2 = int(imei_number[7]) * 2
    imei_n10_x2 = int(imei_number[9]) * 2
    imei_n12_x2 = int(imei_number[11]) * 2
    imei_n14_x2 = int(imei_number[13]) * 2
    imei_n2 = sum([int(i) for i in cut(str(imei_n2_x2), 1)])
    imei_n4 = sum([int(i) for i in cut(str(imei_n4_x2), 1)])
    imei_n6 = sum([int(i) for i in cut(str(imei_n6_x2), 1)])
    imei_n8 = sum([int(i) for i in cut(str(imei_n8_x2), 1)])
    imei_n10 = sum([int(i) for i in cut(str(imei_n10_x2), 1)])
    imei_n12 = sum([int(i) for i in cut(str(imei_n12_x2), 1)])
    imei_n14 = sum([int(i) for i in cut(str(imei_n14_x2), 1)])
    imei_sum = int(imei_number[0]) + int(imei_number[2]) + int(imei_number[4]) + int(
        imei_number[6]) + int(imei_number[8]) + int(imei_number[10]) + int(imei_number[12]) + imei_n2 + imei_n4 + imei_n6 + imei_n8 + imei_n10 + imei_n12 + imei_n14
    if str(imei_sum)[-1] != '0':
        imei_checkval = 10 - int(str(imei_sum)[-1])
    else:
        imei_checkval = 0
    if imei_checkval != int(imei_number[14]):
        return(False)
    else:
        return(True)

def convCountry(country, target):
    if country is None:
        return(None)
    elif country is not None and len(country) == 2:
        countryStorage = pycountry.countries.get(alpha_2=country)
    else:
        countryStorage = pycountry.countries.get(official_name=country)
        if countryStorage is None:
            countryStorage = pycountry.countries.get(name=country)
    if target == 'a2':
        return(countryStorage.alpha_2)
    elif target == 'name':
        countryName = countryStorage.official_name
        if countryName is None:
            countryName = countryStorage.name
        return(countryName)

def getWarrantyStatus(imei, code):
    submitData = {'country': code, 'imei': imei, 'url': '/phones/en_int/support/api/imei'}
    while True:
        try:
            print(currenttime(), "Looking up...")
            warrantyresponse = requests.post(upstream_api_url2, data=json.dumps(
                submitData), headers=redirect_tccserver_hdr2).text
            break
        except requests.exceptions.ConnectionError:
            print(currenttime(), "Connection Error - waiting 5 seconds...")
            time.sleep(5)
        except requests.exceptions.ChunkedEncodingError:
            print(currenttime(), "Connection Error - waiting 5 seconds...")
            time.sleep(5)
        except:
            print(currenttime(), "Connection Error - waiting 5 seconds...")
            time.sleep(5)
    if warrantyresponse['code'] == 200:
        return(warrantyresponse['valid'])
    else:
        return(False)

def getActivationInfo(imei):
    submitData = {'programName': 'nokia8-upgrade', 'imei': imei}
    while True:
        try:
            print(currenttime(), "Looking up...")
            warrantyresponse = requests.post(upstream_api_url, data=json.dumps(
                submitData), headers=redirect_tccserver_hdr).text
            break
        except requests.exceptions.ConnectionError:
            print(currenttime(), "Connection Error - waiting 5 seconds...")
            time.sleep(5)
        except requests.exceptions.ChunkedEncodingError:
            print(currenttime(), "Connection Error - waiting 5 seconds...")
            time.sleep(5)
        except:
            print(currenttime(), "Connection Error - waiting 5 seconds...")
            time.sleep(5)
    if 'not found' in warrantyresponse:
        return(invalidData)
    else:
        response_dict = json.loads(warrantyresponse)
        imei_r = response_dict.setdefault('imei', None)
        imei2_r = response_dict.setdefault('imei2', None)
        serial = response_dict.setdefault('psn', None)
        product = response_dict.setdefault('model', None)
        productName = response_dict.setdefault('marketName', None)
        countryCode = response_dict.setdefault('activationCountry', None)
        soldCountryCode = response_dict.setdefault('shipToCountry', None)
        warstart = response_dict.setdefault('activationDate', None)
        shipToCustomer = response_dict.setdefault('shipToCustomer', None)
        countryCode = convCountry(countryCode, 'a2')
        countryDesc = convCountry(countryCode, 'name')
        soldCountryCode = convCountry(soldCountryCode, 'a2')
        soldCountryDesc = convCountry(soldCountryCode, 'name')
    actWarrantyExp = None
    targetWarrantyExp = None
    if imei2_r == None:
        imei_merge = imei_r
    else:
        imei_merge = imei_r + '|' + imei2_r
    resultData = {'data': {'product': serial, 
                        'productName': productName, 
                        'serial': product, 
                        'status': 'SH', 
                        'IMEI': imei_merge,
                        'countryCode': countryCode, 
                        'countryDesc': countryDesc, 
                        'soldCountryCode': soldCountryCode, 
                        'soldCountryDesc': soldCountryDesc, 
                        'sdfDesc': shipToCustomer, 
                        'warstart': warstart, 
                        'actWarrantyExp': actWarrantyExp,
                        'targetWarrantyExp': targetWarrantyExp}}
    return(resultData)


@warranty.route('/WarrantyLookup', methods=['POST'])
def lookup():
    print(currenttime(),"=== Warranty Lookup Request Detected ===")
    srcIP = request.environ.get('HTTP_X_REAL_IP')
    print(currenttime(), 'Source IP: ' + srcIP)
    xsrcIP = srcIP.replace('.', '_')
    if ('xSrc_' + xsrcIP) not in globals().keys():
        globals()['xSrc_' + xsrcIP] = None
    if globals()['xSrc_' + xsrcIP] is not None and isCooldown(globals()['xSrc_' + xsrcIP]):
        print(currenttime(), 'Request from', srcIP, 'is under Cooldown')
        return(cooldownData)
    else:
        globals()['xSrc_' + xsrcIP] = ctime()
        imei = request.get_data(as_text=True)
        imei = transfer_to_dict(imei, imei)['imei']
        imei = (''.join(list(filter(str.isalnum, imei.upper()))))
        print(currenttime(), 'IMEI:', imei)
        if(len(imei)) == 15:
            if isImeiValid(imei):
                if imei in invalidImeiValue:
                    print(currenttime(), 'Invalid IMEI')
                    return(invalidData)
                else:
                    print(currenttime(), 'Valid IMEI')
                    resultDataEx = getActivationInfo(imei)
                    print(currenttime(), resultDataEx)
                    return(resultDataEx)
            else:
                print(currenttime(), 'Invalid IMEI')
                return(invalidData)
        elif(len(imei)) == 18:
            print(currenttime(), 'PSN:', imei)
            resultDataEx = getActivationInfo(imei)
            print(currenttime(), resultDataEx)
            return(resultDataEx)
        else:
            print(currenttime(), 'Invalid IMEI')
            return(invalidData)
