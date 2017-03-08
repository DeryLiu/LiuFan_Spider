import xmltodict
from Pro_Finance.Amaon_Finances.get_info_save import get_data_to_save_db
import re
import os
import zipfile
from Tools import ALL_CONFIG

# trans xxx.xml to 1.xml
def rename():
    path = ALL_CONFIG.RESULT_XML_FILE
    with open(ALL_CONFIG.GROUP_LIST_FILE) as group_file:
        group_list = group_file.readlines()
        for group in group_list:
            group_name = group.split('\t')[0]
            try:
                i =1
                for file in os.listdir(path+group_name+'/'):
                    # if os.path.isfile(os.path.join(path,file))==True:
                        # if file.find('.')<0:
                    # print file
                    if file.split('.')[1] == 'xml':
                        newname= str(i)+'.xml'
                        os.rename(os.path.join(path+group_name+'/',file),os.path.join(path+group_name+'/',newname))
                        i+=1
                        print (file,'ok')
            except Exception as e:
                pass
                # print e

def get_financialEvent():
    if not os.path.exists(ALL_CONFIG.CSV_DATA_FILE):
        os.mkdir(ALL_CONFIG.CSV_DATA_FILE)

    for group_xmls in os.listdir(ALL_CONFIG.RESULT_GROUP):
        groupxml_orange = open(ALL_CONFIG.RESULT_GROUP + group_xmls, 'r').read()
        store_name = str(group_xmls).split('.')[0]
        with open(ALL_CONFIG.CSV_DATA_FILE + store_name + '.csv', 'a') as groupxml_info:
            group = xmltodict.parse(groupxml_orange, encoding='utf-8')

            # get the account_id
            account_id_list = [i.split('\t')[0] for i in open(ALL_CONFIG.AMAZON_ACCOUNT_FILE,'r').readlines() if str(i).split('\t')[1].replace('"','') == store_name]
            account_id = ''.join(account_id_list)

            try:
                eventGroupList = group['ListFinancialEventGroupsResponse']['ListFinancialEventGroupsResult']['FinancialEventGroupList']['FinancialEventGroup']
                trans_list = []
                try:
                    for eventGroup in eventGroupList:
                        trans_fee = eventGroup['OriginalTotal']['CurrencyAmount']
                        trans_time = eventGroup['FinancialEventGroupStart']
                        trans_time = str(trans_time).replace('T',' ').replace('Z','')
                        info_list = [trans_time, '', 'Transfer', account_id, '', '', '', '', '','Amazon', '', '','', '', '', '', '', '', '', trans_fee, trans_fee]
                        trans_list.append(info_list)
                        # trans_list.append('\n')
                except:
                    trans_fee = eventGroupList['OriginalTotal']['CurrencyAmount']
                    trans_time = eventGroupList['FinancialEventGroupStart']
                    trans_time = str(trans_time).replace('T',' ').replace('Z','')
                    info_list = [trans_time, '', 'Transfer', account_id, '', '', '', '', '', 'Amazon','', '', '','', '', '', '', '', '', trans_fee, trans_fee]
                    trans_list.append(info_list)
                    # trans_list.append('\n')
                # print trans_list
                for sub_list in trans_list:
                    # print sub_list
                    groupxml_info.write('\t'.join(str(s) for s in sub_list if isinstance(sub_list,list))+'\n')
                # groupxml_info.write('\t'.join(str(s) for sub_list in trans_list for s in sub_list if isinstance(sub_list,list)))

            except:
                print (store_name+' is None')

def xml2csv():
    # the catalog of csv_data
    path = ALL_CONFIG.RESULT_XML_FILE
    # file_list_len = os.listdir(path)

    # open the groupid_list.txt
    with open(ALL_CONFIG.GROUP_LIST_FILE) as group_file:
        # find the store_name
        group_list = group_file.readlines()
        for group in group_list:
            group_name = group.split('\t')[0]
            # print group_name
            # find account id

            account_id_list = [ str(i).split('\t')[0] for i in open(ALL_CONFIG.AMAZON_ACCOUNT_FILE,'r').readlines() if group_name == i.split('\t')[1].replace('"','')]
            account_id = ''.join(account_id_list)
            # print account_id
            # group_name = 'Phoenix-C'
            try:
                # ./Result_data/CSV_data/ + group_name + .csv
                with open(ALL_CONFIG.CSV_DATA_FILE + group_name+ '.csv', 'aw') as info_file:
                    try:
                        # gp through the list of ./Result_xml/
                        for file in os.listdir(path + group_name + '/'):
                            print (file)
                            zyx_xml = open(path + group_name + '/' + file, 'r').read()
                            try:
                                fee_group_data = xmltodict.parse(zyx_xml, encoding='utf-8')
                                # file_name = path + group_name + '/'+ file.split('.')[0] + '.csv'
                                info = get_data_to_save_db(fee_group_data, account_id)
                                # info = get_data_to_save_text(fee_group_data)
                                info_file.write('\n')
                                for fee_dict in info:
                                    for t in ALL_CONFIG.TITLE:
                                        fee_dict[t] = str(fee_dict[t])+'\t'

                                        info_file.write(fee_dict[t])

                                        # print '=-=-='
                                        # # response.write('\t'.join(amazon[key]))
                                    info_file.write('\n')
                                info_file.flush()
                                print ('Success: '+group_name)

                            except Exception as e:
                                # print '1',e
                                print ('None of type: '+ group_name)
                                # print path + group_name + '/' + file
                    except Exception as e:
                        print (e)
            except:
                pass

def zip_csv():
    path = ALL_CONFIG.RESULT_XML_FILE
    try:
        import zlib
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED

    z = zipfile.ZipFile('./amazon_fee.zip', mode='a', compression=compression)

    with open(ALL_CONFIG.GROUP_LIST_FILE) as group_file:
        group_list = group_file.readlines()
        # zip_file = []
        for group in group_list:
            group_name = group.split('\t')[0]
            try:
                # zip_file.append(path + group_name + '/' + group_name + '.csv')
                z.write(path + group_name + '/' + group_name + '.csv')
            except:
                pass
        z.close()

# collect all csv file to one,info.csv
def collect_csv():
    path = ALL_CONFIG.CSV_DATA_FILE
    with open('./info.csv','a') as all_info_file:
        # open the groupid_list.txt
        try:
            # go through the group_list.txt
            with open(ALL_CONFIG.GROUP_LIST_FILE) as group_file:
                group_list = group_file.readlines()
                for group in group_list:
                    # find the store_name
                    group_name = group.split('\t')[0]
                    # group_name = 'Phoenix-C'
                    try:
                        with open(path + group_name + '.csv', 'r') as info_file:
                            # clear the '\n'
                            for clear_n in info_file.readlines():
                                if clear_n == '\n':
                                    pass
                                else:
                                    # print clear_n
                                    all_info_file.write(clear_n)
                                    # all_info_file.write(info_file.read())
                            all_info_file.write('\n')
                    except:
                        pass
        except:
            pass

# delete store_name.csv from Result_xml/store_name/store_name.csv
def rome():
    import sys, csv, operator
    import os
    import glob

    path = ALL_CONFIG.RESULT_XML_FILE

    with open(ALL_CONFIG.GROUP_LIST_FILE) as group_file:
        # find the store_name
        group_list = group_file.readlines()
        for group in group_list:
            group_name = group.split('\t')[0]
            print (group_name)
            # find account id
            # print account_id
            # group_name = 'Phoenix-C'
            try:
                os.remove(path + group_name + '/' + group_name + '.csv')
            except:
                pass


if __name__ == '__main__':

    # trans xxx.xml to 1.xml
    # rename()

    # get_financialEvent info to save the csv.file
    get_financialEvent()

    xml2csv()

    # zip_csv()

    # collect all csv file to one,info.csv
    collect_csv()

    # delete store_name.csv from Result_xml/store_name/store_name.csv
    # rome()