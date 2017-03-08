from multiprocessing import Lock
import re
import requests
from Tools import get_html

def get_list(url):
    list_num =''
    html=get_html.get_html(url)
    list_info =re.search(r"<div class='result-summary-container'>(.*?)</div>",html,re.S)
    if list_info!=None:
        list_info=list_info.group(1)
        list_num=re.search(r'of[\s]([0-9]?\,?[0-9]+)[\s]results', list_info, re.S)
        if list_num:
            list_num = list_num.group(1)
            list_num = list_num.replace(',', '')
            return int(list_num)
        else:
            return 0
    else:
        list_info =re.search(r"<div class=result-summary-container>(.*?)</div>",html,re.S)
        if list_info!=None:
            list_info=list_info.group(1)
            list_num=re.search(r'of[\s]([0-9]?\,?[0-9]+)[\s]results', list_info, re.S)
            if list_num:
                list_num = list_num.group(1)
                list_num = list_num.replace(',', '')
                return int(list_num)
            else:
                return 0
        else:
            return 0
def dichotomy(low,high,list_url):
    print ('.......')
    if high!='':
        mid=(int(low)+int(high))/2
    else:
        mid=low+100
    url=list_url+'&min_price='+str(low)+'&max_price='+str(mid)
    listings_count=get_list(url)
    print (listings_count)
    if listings_count<1000:
        if listings_count!=0:
            lock.acquire()
            list_file.write(str(listings_count)+'\t'+url+'\n')
            list_file.flush()
            lock.release()
    else:
        if int(mid)-int(low)==1:
            lock.acquire()
            list_file.write(str(listings_count)+'\t'+url+'\n')
            list_file.flush()
            lock.release()
        else:
            dichotomy(low,mid,list_url)
    url=list_url+'&min_price='+str(mid)+'&max_price='+str(high)
    listings_count=get_list(url)
    if high!='':
        if listings_count<1000:
            if listings_count!=0:
                lock.acquire()
                list_file.write(str(listings_count)+'\t'+url+'\n')
                list_file.flush()
                lock.release()
        else:
            if int(high)-int(mid)==1:
                lock.acquire()
                list_file.write(str(listings_count)+'\t'+url+'\n')
                list_file.flush()
                lock.release()
            else:
                dichotomy(mid,high,list_url)
    else:
        if listings_count<1000:
            if listings_count!=0:
                lock.acquire()
                list_file.write(str(listings_count)+'\t'+url+'\n')
                list_file.flush()
                lock.release()
        else:
            if int(mid)>=3000:
                lock.acquire()
                list_file.write(str(listings_count)+'\t'+url+'\n')
                list_file.flush()
                lock.release()
            else:
                dichotomy(mid,high,list_url)

def get_list_info():
    global list_file,lock
    lock=Lock()
    list_file=open('./result/list.txt','w')
    #url='http://www.walmart.com/browse/electronics/laptop-accessories/3944_3951_1089430_1230184?facet=condition:New'
    # url='https://www.walmart.com/browse/ipad-tablets/tablet-pcs/3944_1078524_1078084/?cat_id=3944_1078524_1078084&facet=operating_system:Microsoft%20Windows||condition:New'
    # url = 'https://www.walmart.com/browse/ipad-tablets/tablet-pcs/3944_1078524_1078084/?cat_id=3944_1078524_1078084&facet=condition:New||operating_system:Android'
    # url = '''https://www.walmart.com/browse/electronics/monitors/3944_3951_1089430_1230184_1230252_110915?cat_id=3944_3951_1089430_1230184_1230252_110915&facet=condition:New'''
    # url = '''https://www.walmart.com/browse/speakers/sound-bars/3944_77622_1230415_1107398?cat_id=3944_77622_1230415_1107398&facet=condition:New'''
    url = '''https://www.walmart.com/browse/soccer/soccer-shinguards/4125_4161_432196_1075749?cat_id=4125_4161_432196_1075749&facet=condition:New'''
    low=50
    high=''
    dichotomy(low,high,url)
    list_file.close()
if __name__=="__main__":
    get_list_info()
