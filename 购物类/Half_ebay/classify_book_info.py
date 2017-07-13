'''
Created on 2016年06月15日

@author: yonghuan
'''
import re 
import os
from multiprocessing import Lock, Pool
from Tools.util import httptools
import logging
import logging.config

import select
import config

logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1")   
logger2 = logging.getLogger("logger2") 



def create_titles(filename,titles):
    f = open(filename,"w")
    f.write("\t".join(titles)+"\n")
    f.flush()
    f.close()

'''
   获取亚马逊的书籍信息
'''
def amazon_book_info(html,mdir,buybox_url,abook_url,condition,weight,isbn,isbn13,hbook_url):
    print ('---------------------amazon_book_info begin----------------------')
    try:
        atool=httptools.httptools(mdir.split('/')[1])
        with open(mdir+'follow.csv','aw') as f:
            #print 'exist'
            asin=re.findall('data-asin="(.*?)"',html,re.S)[0]
            buybox_url=buybox_url.replace('[asin]',asin)
            print (buybox_url)
            buybox_html=atool.gethtmlproxy(buybox_url)
            if buybox_html:
                buybox=re.findall('<span class="a-size-medium a-color-price .*?>(.*?)</span>',buybox_html,re.S)
                if buybox:
                    buybox_price=buybox[0].replace('\t','').replace('\n','')
                else:
                    buybox_price=re.findall('from.*?<span class=\'a-color-price\'>(.*?)</span>',buybox_html,re.S)[0].replace('\t','').replace('\n','')
                    #if buybox:
                    #buybox_price=buybox[0]
               # print isbn,buybox#,buybox_price

            abook_url=abook_url.replace('[asin]',asin)
            print (abook_url)
            abook_html = atool.gethtmlproxy(abook_url)
            #abook_html = self.get_html(abook_url)
            if abook_html:
                #with open('xx.html','w') as xx:
                    #xx.write(abook_html)
                if 'There are currently no listings' in abook_html:
                    flag='no'
                else:
                    flag='yes'
            amazon_condition={'Brand New':'f_new=true','Like New':'f_usedLikeNew=true','Very Good':'f_usedVeryGood=true','Good':'f_usedGood=true','Acceptable':'f_usedAcceptable=true'}
            forward='f_primeEligible=true'
            for i in range(len(condition)):
                abook_url=abook_url.replace(forward,amazon_condition[condition[i][0]])
                forward=amazon_condition[condition[i][0]]
                print (abook_url)
                aabook_html = atool.gethtmlproxy(abook_url)
                if aabook_html:
                    prices=re.findall('<span class=.*?price.*?">(.*?)</span>',aabook_html)
                    if prices:
                        amazon_condition[condition[i][0]]=prices[0].replace(' ','')
                    else:
                        amazon_condition[condition[i][0]]=''
            #print amazon_condition
            for i in range(len(condition)):
                bookinfo=[]
                bookinfo.append(asin)
                bookinfo.append(isbn)
                bookinfo.append(isbn13)
                bookinfo.append(condition[i][0])
                bookinfo.append(condition[i][1])
                bookinfo.append(condition[i][2])
                bookinfo.append(weight)
                bookinfo.append(buybox_price)
                bookinfo.append(flag)
                bookinfo.append(amazon_condition[condition[i][0]])
                bookinfo.append(hbook_url)
                print (bookinfo)
                f.write("\t".join(bookinfo)+"\n")
    except Exception as e:
        print (e)
        logger2.exception(e)
    print ('---------------------amazon_book_info end----------------------')


def book_info(line):
    print ('---------------------book_info begin----------------------')
    try:
        book_info=eval(line.replace('\n',''))
        #print book_info
        for i in range(2):
            if i==0:
                mdir='./result/'+opt[0]+'/com/'
                aurl="https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dstripbooks&field-keywords=[isbn]"
                buybox_url="https://www.amazon.com/gp/product/[asin]"
                abook_url="https://www.amazon.com/gp/offer-listing/[asin]/ref=olp_f_primeEligible?ie=UTF8&f_primeEligible=true"   
                tool = httptools.httptools('com')
            else:
                mdir='./result/'+opt[0]+'/ca/'
                buybox_url="https://www.amazon.ca/gp/product/[asin]"
                abook_url="https://www.amazon.ca/gp/offer-listing/[asin]/ref=olp_f_primeEligible?ie=UTF8&f_primeEligible=true"   
                tool = httptools.httptools('ca')
            isbn=book_info['ISBN']
            isbn13=book_info['ISBN-13']
            weight=book_info['weight']
            condition=book_info['condition']
            hbook_url=book_info['url']
            if condition:
                ourl=aurl.replace('[isbn]',isbn13)
                print (ourl)
                ohtml = tool.gethtmlproxy(ourl)
                if ohtml:
                #with open('m.html','w') as mm:
                    #mm.write(ohtml)
                    if 'result for' in ohtml or 'results for' in ohtml:
                        amazon_book_info(ohtml,mdir,buybox_url,abook_url,condition,weight,isbn,isbn13,hbook_url)
                    else:
                        #with open('m.html','w') as mm:
                        #mm.write(ohtml)
                        turl=aurl.replace('[isbn]',isbn)
                        print (turl)
                        thtml = tool.gethtmlproxy(turl)
                        if thtml:
                            if 'result for' in ohtml or 'results for' in ohtml:
                                amazon_book_info(thtml,mdir,buybox_url,abook_url,condition,weight,isbn,isbn13)
                            else:
                                mformat=book_info['format']
                                language=book_info['language']
                                publisher=book_info['publisher']
                                author=book_info['author']
                                publish_time=book_info['publish time']
                                details=book_info['details']
                                title=book_info['title']
                                with open(mdir+'establish.csv','aw') as f:
                                    for i in range(len(condition)):
                                        bookinfo=[]
                                        bookinfo.append(isbn)
                                        bookinfo.append(isbn13)
                                        bookinfo.append(condition[i][0])
                                        bookinfo.append(condition[i][1])
                                        bookinfo.append(condition[i][2])
                                        bookinfo.append(weight)
                                        bookinfo.append(mformat)
                                        bookinfo.append(language)
                                        bookinfo.append(publisher)
                                        bookinfo.append(author)
                                        bookinfo.append(publish_time)
                                        bookinfo.append(details)
                                        bookinfo.append(title)
                                        bookinfo.append(hbook_url)
                                        print (bookinfo)
                                        f.write("\t".join(bookinfo)+"\n")
                        else:
                            with open('./result/'+opt[0]+'/classify_fail.txt','aw') as rr:
                                rr.write(line)
                else:
                    with open('./result/'+opt[0]+'/classify_fail.txt','aw') as rr:
                        rr.write(line)
    except Exception as e:
        print (e)
        logger2.exception(e)
    print ('---------------------book_info end----------------------')

if __name__ == '__main__':
    global opt
    opt=config.opt.split('|')
    logger1.info(opt[0]+'classify book info begin')
    if os.path.exists('./result/'+opt[0]+'/com')==0:
        os.mkdir('./result/'+opt[0]+'/com')
    if os.path.exists('./result/'+opt[0]+'/ca')==0:
        os.mkdir('./result/'+opt[0]+'/ca')
    follow_filename={'com':'./result/'+opt[0]+'/com/follow.csv','ca':'./result/'+opt[0]+'/ca/follow.csv'}
    establish_filename={'com':'./result/'+opt[0]+'/com/establish.csv','ca':'./result/'+opt[0]+'/ca/establish.csv'}
    follow_titles=['asin','ISBN','ISBN-13','condition','half.ebay price','secondary price','weight','amazon-buybox','self-support','amazon-price','url'] 
    establish_titles=['ISBN','ISBN-13','condition','half.ebay price','secondary price','weight','formart','language','publisher','author','publish time','detail','title','url'] 
    for key in follow_filename:
        create_titles(follow_filename[key],follow_titles)
    for key in establish_filename:
        create_titles(establish_filename[key],establish_titles)
    with open('./result/'+opt[0]+'/book_info.txt') as hh:
    #with open('./result/url/book_info.txt') as hh:
        lines = hh.readlines()
    #lines=lines[:1]
    #book_info(line)
    pool = Pool(2)
    pool.map(book_info,lines)
    pool.close()
    pool.join()
    logger1.info(opt[0]+'classify book info end')
