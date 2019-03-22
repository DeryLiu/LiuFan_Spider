# Create your models here.
# import json
import os
from datetime import datetime, timedelta
from xml.dom.minidom import parseString
import pytz
from Tools.Amazon_Interface.amazom_interface import AmazonFinancial
from Tools.util.xml_util import get_element_by_tag
import xmltodict
from Tools import ALL_CONFIG

# find amazon_account by store_name
def get_account(n):
    with open(ALL_CONFIG.AMAZON_ACCOUNT_FILE) as amazac:
        amazac_list = amazac.readlines()
        a  = amazac_list[n].split('\t')

        STORE_ACCOUNT = {'access_key': a[2].replace('"','').replace('\n',''),
                         'secret_key': a[3].replace('"','').replace('\n',''),
                         'account_id': a[4].replace('"','').replace('\n',''),
                         'mkplace_id': a[5].replace('"','').replace('\n',''),
                         'MWSAuthToken': a[6].replace('"','').replace('\n','')}
        return [STORE_ACCOUNT,a[1].replace('"','').replace('\n','')]

# print the path
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

# step 1: download the group.xml by date time and account
def get_group_obj(num):

    # current time
    now_time = datetime.now(pytz.UTC) - timedelta(days = 35,hours=datetime.now(pytz.UTC).hour,minutes=datetime.now(pytz.UTC).minute,seconds=datetime.now(pytz.UTC).second)
    from_date = now_time.strftime('%FT%T')
    # print from_date
    to_date = (now_time + timedelta(days = 31)).strftime('%FT%T')
    # print to_date

    # 获取Amazon帐号
    # store_account = amazon_conf.STORE_ACCOUNT
    store_account = get_account(num)[0]
    print (get_account(num)[1])
    amaz = AmazonFinancial(store_account)
    groupObj = amaz.list_finace_eventgroup(from_date,to_date)

    try:
         is_Ok =groupObj['group_xml']
         groupxml = open(ALL_CONFIG.RESULT_GROUP+get_account(num)[1]+'.xml', 'w')
         groupxml.write(str(groupObj['group_xml']))
    except:
        print ('Fail: ',get_account(num)[1])

# setp 2: get the group_id_list by the downloaded group.xml
def get_groupId_list():
    # go through all the file from Result_group
    xml_file_list = printPath(1, ALL_CONFIG.CURRENT_CATALOG)
    # save group_list to './Result_data/groupid_list.txt'
    with open(ALL_CONFIG.GROUP_LIST_FILE, 'a') as group_id_list:
        for xml_file in xml_file_list:
            file_type = str(xml_file).split('.')[1]
            file_name = str(xml_file).split('.')[0]
            # avoid to trans other files
            if file_type == 'xml':
                group_xml_file = open(ALL_CONFIG.RESULT_GROUP+xml_file,'r').read()
                # transfer_file = open(amazon_conf.TRANSFER_FILE,'aw')
                try:
                    group = xmltodict.parse(group_xml_file,encoding='utf-8')
                    try:
                        eventGroupList = group['ListFinancialEventGroupsResponse']['ListFinancialEventGroupsResult']['FinancialEventGroupList']['FinancialEventGroup']
                        # print eventGroupList
                        group_id_list.write(file_name + '\t')
                        if isinstance(eventGroupList,list):
                            for eventGroup in eventGroupList:
                                groupid = eventGroup['FinancialEventGroupId']
                                group_id_list.write(groupid+'\t')
                            group_id_list.write('\n')
                        else:
                            groupid = group['ListFinancialEventGroupsResponse']['ListFinancialEventGroupsResult']['FinancialEventGroupList']['FinancialEventGroup']['FinancialEventGroupId']
                            group_id_list.write(groupid + '\t')
                            group_id_list.write('\n')

                    except Exception as e:
                        print (file_name,': ',e)
                            # group_id_list.write('"'+str(groupid)+'"'+',')

                except Exception as e:
                    print (file_name,': ',e)


if __name__ == '__main__':
    # get_group_obj(1)
    if not os.path.exists(ALL_CONFIG.RESULT_GROUP):
        os.mkdir(ALL_CONFIG.RESULT_GROUP)
    # step 1: get the group.xml
    # before u use this func,please set the date of u need
    for i in range(1,455):
        get_group_obj(i)

    # step 2: get the list of group_id_list from group.xml
    get_groupId_list()

