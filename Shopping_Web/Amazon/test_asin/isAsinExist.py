import re
import pytz
from datetime import datetime,timedelta
from Tools.AMAZON_API.amazon_api.Amazon_api import Amazon_AWS,Amazon_MWS
from multiprocessing import Pool,Lock
from Tools import ALL_CONFIG

def get_product_infos(asins):

    result = amazon_aws.get_product_info(asins)
    print (result)
    # result_dict = result
    if result['result']: # True
        # print result['data']
        pass
    else:
        if 'is not a valid value for ItemId' in str(result['error_message']):
            # asin = re.findall('AWS.InvalidParameterValue: (.*?) is not a valid value for ItemId',str(result['error_message']),re.S)
            asin = str(result['error_message']).split(' ')[1]
            print ('asin: ',asin)
            result_file.write(asin+'\n')
            # result_file.write(''.join(asin) + '\n')
        else:
            ferr.write(asins+'&&'+result['error_message']+'\n')

def start(items_file):
    global result_file, lock, ferr,item_file
    item_file = open(items_file, 'r')

    #调用函数create_titles
    result_file = open(ALL_CONFIG.ISASINEXIT_NOTEXIST_FILE, 'a')
    items_list = item_file.readlines()
    ferr = open(ALL_CONFIG.ISASINEXIT_OTHERERR_FILE, 'a')
    #把获取的url依次传入handle
    items = []
    for item in items_list:
        item = item.split('\n')[0]
        items.append(item)
        # get_info(item)
    # print items

    lock = Lock()
    pool = Pool(5)
    #调用函数把items的url依次传入handle函数中爬虫
    pool.map(get_product_infos, items)
    pool.close()
    pool.join()

    item_file.close()
    result_file.close()
    ferr.close()


if __name__ == "__main__":
    #获取api的response
    to_time = str(datetime.now(pytz.UTC) - timedelta(hours = 2)).split('.')[0].replace(' ','T') + 'Z'
    print ('start:',datetime.now(pytz.UTC))
    from_time = str(datetime.now(pytz.UTC) - timedelta(days = 1)).split('.')[0].replace(' ','T') + 'Z'
    amazon_mws = Amazon_MWS()
    amazon_aws = Amazon_AWS()
    t = datetime.now(pytz.UTC)

    start(ALL_CONFIG.ISASINEXIT_USAMAP_FILE)
