import json
from datetime import datetime, timedelta
from xml.dom.minidom import parseString
import os
import pytz
from multiprocessing import Lock, Pool
import xmltodict
import string
import random
from Tools.Amazon_Interface.amazom_interface import AmazonReport
from Tools.util.xml_util import get_element_by_tag
from Tools import ALL_CONFIG

# find amazon_account by store_name
def get_account(name):
    with open(ALL_CONFIG.AMAZON_ACCOUNT_FILE) as amazac:
        amazac_list = amazac.readlines()
        for ama in amazac_list:
            a  = ama.split('\t')
            if a[1].replace('"','').replace('\n','') == name:
                STORE_ACCOUNT = {
                    'access_key': a[2].replace('"','').replace('\n',''),
                    'secret_key': a[3].replace('"','').replace('\n',''),
                    'account_id': a[4].replace('"','').replace('\n',''),
                    'mkplace_id': a[5].replace('"','').replace('\n',''),
                    'MWSAuthToken': a[6].replace('"','').replace('\n','')}
                return STORE_ACCOUNT
            else:
                pass

def download_request_file(num):
    # get the store_name
    # store_account = amazon_conf.STORE_ACCOUNT
    with open(ALL_CONFIG.REQUEST_ID_FILE,'r') as request_id_file:
        try:
            report_id_list = request_id_file.readlines()[num].split('\t')
            store_name = report_id_list[0]
            store_account = get_account(store_name)
            try:
                amaz = AmazonReport(store_account)
                for report_id in report_id_list[1:]:
                    try:
                        xls = amaz.get_report(report_id.strip('\n'))
                        # print xls
                        request_response = xls['report_request_info']

                        if not os.path.exists(ALL_CONFIG.REPORT_FILE+store_name + '/'):
                            os.mkdir(ALL_CONFIG.REPORT_FILE+store_name + '/')

                        with open(ALL_CONFIG.REPORT_FILE+store_name+'/'+store_name+'.txt', 'a') as report_file:
                            report_file.write(request_response)

                    except Exception as e:
                        print ('sss', e)
            except Exception as e:
                print (store_account,': ',e)

        except Exception as e:
            print ('list index out of range? ',e)


def cut_market_file(info):
    pass


def cut_report_file(info,store_name):
    if info == []:
        pass
    try:
        start_time = info[1][1].split(' ')[0]
        if info[2][11] == 'Amazon.com':
            with open(ALL_CONFIG.REPORT_FILE+store_name+'/'+store_name+'_'+start_time+'_'+'us'+'.csv','a') as usa_file:
                for i in info:
                    usa_file.write('\t'.join(i))
                # usa_file.write('\t'.join(str(usadata) for usadata in info))
        elif info[2][11] == 'Amazon.ca':
            with open(ALL_CONFIG.REPORT_FILE+store_name+'/'+store_name+'_'+start_time+'_'+'ca'+'.csv','a') as ca_file:
                for c in info:
                    ca_file.write('\t'.join(c))
                # ca_file.write('\t'.join(str(cadata) for cadata in info)+'\n')
        else:
            print ('nonono')

    except Exception as e:
        print (e)


def spilt_report_file():
    cut_list = []
    send_list = []
    all_report_filelist = os.listdir(ALL_CONFIG.REPORT_FILE)
    for report_file in all_report_filelist:
        try:
            with open(ALL_CONFIG.REPORT_FILE+report_file+'/'+report_file+'.txt','r') as wait_to_cut_file:
                for data in wait_to_cut_file.readlines():
                    data_info = data.split('\t')
                    cut_list.append(data_info)

                    if data_info[0] == 'settlement-id':
                        cut_report_file(send_list,report_file)
                        send_list = [data_info]
                    else:
                        send_list.append(data_info)
                cut_report_file(send_list,report_file)
        except Exception as e:
            print (e)

def delet_file():
    for filename in os.listdir(ALL_CONFIG.REPORT_FILE):
        os.remove(ALL_CONFIG.REPORT_FILE+filename+'/'+filename+'.txt')

if __name__ == '__main__':

    if not os.path.exists(ALL_CONFIG.REPORT_FILE):
        os.mkdir(ALL_CONFIG.REPORT_FILE)

    # download the file
    # for i in range(1,335):
    #     download_request_file(i)

    spilt_report_file()

    # delet_file()
