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
from Tools.Amazon_Interface.amazom_interface import AmazonReport
# from util.xml_util import get_element_by_tag
from Tools.util.xml_util import get_element_by_tag
from Tools import ALL_CONFIG

def get_account_by_num(n):
    with open(ALL_CONFIG.AMAZON_ACCOUNT_FILE) as amazac:
        amazac_list = amazac.readlines()
        a = amazac_list[n].split('\t')

        STORE_ACCOUNT = {'access_key': a[2].replace('"', '').replace('\n', ''),
                         'secret_key': a[3].replace('"', '').replace('\n', ''),
                         'account_id': a[4].replace('"', '').replace('\n', ''),
                         'mkplace_id': a[5].replace('"', '').replace('\n', ''),
                         'MWSAuthToken': a[6].replace('"', '').replace('\n', '')}
        return [STORE_ACCOUNT, a[1].replace('"', '').replace('\n', '')]


def printPath(level, path):
    # allFileNum = 0
    '''
    打印一个目录下的所有文件夹和文件
    '''
    # 所有文件夹，第一个字段是次目录的级别
    dirList = []
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    # 先添加目录级别
    dirList.append(str(level))
    for f in files:
        if(os.path.isdir(path + '/' + f)):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if(f[0] == '.'):
                pass
            else:
                # 添加非隐藏文件夹
                dirList.append(f)
        if(os.path.isfile(path + '/' + f)):
            # 添加文件
            fileList.append(f)
            # 当一个标志使用，文件夹列表第一个级别不打印
    # i_dl = 0
    # for dl in dirList:
    #     if(i_dl == 0):
    #         i_dl = i_dl + 1
    #     else:
    #     # 打印至控制台，不是第一个的目录
    #         print '-=-=-'
    #         print '-' * (int(dirList[0])), dl
    #         # 打印目录下的所有文件夹和文件，目录级别+1
    #         printPath((int(dirList[0]) + 1), path + '/' + dl)
    # for fl in fileList:
    #     # 打印文件
    #     # print '-'* (int(dirList[0])), fl
    #     print fl
    #     # 随便计算一下有多少个文件
    #     allFileNum = allFileNum + 1
    return fileList

# setp 2: get the group_id_list by the downloaded group.xml
def get_request_id():
    # go through all the file from Result_group
    xml_file_list = printPath(1, ALL_CONFIG.CURRENT_CATALOG)
    # save group_list to './Result_data/groupid_list.txt'
    # print xml_file_list
    with open(ALL_CONFIG.REQUEST_ID_FILE, 'a') as request_id_list:
        for xml_file in xml_file_list:
            # print xml_file
            with open(ALL_CONFIG.REPORT_XML+xml_file, 'r') as request_file:
                # print request_file.read()
                xml = xmltodict.parse(request_file.read(), encoding='utf-8')
                try:
                    request_id = [i['GeneratedReportId'] for i in xml['GetReportRequestListResponse']['GetReportRequestListResult']['ReportRequestInfo']]
                    request_id_list.write(xml_file.strip('.xml')+'\t'+'\t'.join(request_id)+'\n')
                except:
                    pass

# download the request_xml to Report_xml
def get_request_obj(num):
    # current time
    now_time = datetime.now(pytz.UTC) - timedelta(days = 43,hours=datetime.now(pytz.UTC).hour,minutes=datetime.now(pytz.UTC).minute,seconds=datetime.now(pytz.UTC).second)
    from_date = now_time.strftime('%FT%T')
    # print from_date
    to_date = (now_time + timedelta(days = 31)).strftime('%FT%T')
    # print to_date

    # 获取Amazon帐号
    # store_account = amazon_conf.STORE_ACCOUNT
    store_account = get_account_by_num(num)[0]
    print (get_account_by_num(num)[1])
    store_name = get_account_by_num(num)[1]
    amaz = AmazonReport(store_account)
    requestObj = amaz.get_report_request_list(from_date,to_date)

    try:
         is_Ok =requestObj['report_xml']
         requestXml = open(ALL_CONFIG.REPORT_XML+store_name+'.xml', 'w')
         requestXml.write(str(requestObj['report_xml']))
    except:
        print ('Fail: ',store_name)

if __name__ == '__main__':
    if not os.path.exists(ALL_CONFIG.REPORT_XML):
        os.mkdir(ALL_CONFIG.REPORT_XML)

    # for i in range(1,455):
    #     get_request_obj(i)
    #
    get_request_id()