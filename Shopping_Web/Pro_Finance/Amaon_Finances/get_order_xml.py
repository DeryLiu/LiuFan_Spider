import json
from datetime import datetime, timedelta
from xml.dom.minidom import parseString
import os
import pytz
from multiprocessing import Lock, Pool
# from Interface.amazom_interface import AmazonFinancial
import xmltodict
import string
import random
from Tools.Amazon_Interface.amazom_interface import AmazonFinancial
# from util.xml_util import get_element_by_tag
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

def get_obj_by_group_id(num):
    # deal_groupid eg:Phoenix-C	2016361iP4KpTBlSUKfzp3fDnYijQ	2016361Pm1NWtsgQcmrgGJTKoL3KA	2016347nkA5WXFCSVKfCd0E1lwgZw	2016347i4O6LtozTaecjTuXRiD30w	20163330PLSUJNTQBqhZxO7avUlcw	2016333cJ9i-NBvTNGi9H29710y6g
    # get the store_name
    store_name = deal_groupid(num)[0]
    # get the list of group_id
    group_id = deal_groupid(num)[1:-1]

    store_account = get_account(store_name)
    amaz = AmazonFinancial(store_account)
    # print store_account
    # print group_id
    for group in group_id:
        print (group)
        try:
            xls = amaz.list_finace_event(group)
            with open(ALL_CONFIG.RESULT_XML_FILE+store_name+'/'+ store_name + ': ' + group + '.xml', 'w') as groupxml:
                groupxml.write(str(xls['finance_event_group_obj']))

            try:
                nextToken = xls['NextToken']
                print ('newxtoken: ',nextToken)
                # isNext = True
                get_obj_by_next_token(nextToken,num)

            except Exception as e:
                print ('None of NextToken: ',e)

        except Exception as e:
            print ('cant amaz.list_finace_event: ',e)


def get_obj_by_next_token(next_token,num):

    store_name = deal_groupid(num)[0]
    # store_account = amazon_conf.STORE_ACCOUNT
    store_account = get_account(store_name)
    amaz = AmazonFinancial(store_account)
    try:
        finance_event_group_obj = amaz.list_finace_event_by_nextToken(next_token)['finance_event_group_obj']

        next_token_name = ''.join([random.choice(string.digits + string.letters) for i in range(0, 45)])
        with open(ALL_CONFIG.RESULT_XML_FILE+store_name+'/'+next_token_name+'.xml','aw') as nexttokenxml:
            nexttokenxml.write(finance_event_group_obj)
            nexttokenxml.flush()
        nexttokenxml.close()

        dom = parseString(finance_event_group_obj)
        try:
            nextToken = get_element_by_tag(dom, "NextToken")
            print ('nextToken ',nextToken)
            if nextToken:
                get_obj_by_next_token(nextToken,num)
            # else:
            #     return 'nextToken is empty'

        except Exception as e:
            print (e)
            return 0

    # can't get the finance_event_group_obj
    except:
        print ("there is no nextToken")
        # return 0

# read group_id.txt,and return the list of group_id_info
def deal_groupid(num):
    # global error_info
    # # lock = Lock()
    # error_info = open(amazon_conf.ERROR_LOG_FILE,'w')
    # error_info.close()

    groupID_list = open(ALL_CONFIG.GROUP_LIST_FILE, 'r').readlines()
    group_group = groupID_list[num].split('\t')
    group_name = group_group[0]
    # /home/ytroot/桌面/WorkSpaceLHW/ShoppingWebSpider/Pro_Finance/Amaon_Order_Report
    if not os.path.exists('./Result_xml/'+group_name+'/'):
        os.mkdir('./Result_xml/'+group_name+'/')
    return group_group


if __name__ == '__main__':
    # deal_groupid(2)
    if not os.path.exists('./Result_xml/'):
        os.mkdir('Result_xml')
    # num = 0
    # get_obj_by_group_id(num)
    for i in range(0,354):
        get_obj_by_group_id(i)

    # get_obj_by_next_token('e21hcmtldHBsYWNlSWQ6bnVsbCxtYXhSZXN1bHRzUGVyUGFnZTowLHNlYXJjaFF1ZXJ5Q2hlY2tzdW06bnVsbCxxdWVyeVBhZ2luYXRpb25Ub2tlbjoiVUQwelVqY1hXRU5ENHZhZERCWTdDUlBMeHd4X1lMaHVtX2pRUXZkbE9vTllkdmxDYlNMUlZNLUgyTnJUWHJ3UXFjQkxnU0ZPOTd5RUlyaTJhZDQyREg1QVNKSmE5dkpRejRJU09oaTJnQWJOQkxsZEtMTE03aFpzWkQ2R0tuNy0zTkN5RkpOLW9IM2VpS3JBY3pESU5xeUJVSnNnS2tmLUY0ZVZKVm9MOWE4WHpGc1pKMkZ3N2hNeFVXRFY0Wk9Kbnk3UjVRVUJfMy1DaHliWE9tUVVDaFFpZmt5VHR1dmtBTGZIdG9vS0QwclEyMWRvdVhmTlRqQ050V2ZDdDVzUCIsc2VhcmNoUXVlcnk6bnVsbCx0b2tlbkNyZWF0aW9uRGF0ZToxNDgyOTEzOTE4NzgyLHNlbGxlcklkOiJBM042VjYzOTk1MDhGUSJ9')
