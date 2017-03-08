#coding:utf8
'''
Created on 2016年1月4日

@author: tianhu
'''
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    with open('./result.txt') as f:
        lines = f.readlines()
    titles = ['asin','reviews','brand','price','shipping_price','fba_lowest_price','fba_status','title','img_list']   
    with open('buybox_de_2016-03-28.csv','aw') as ff:
        ff.write('\t'.join(titles) + '\n')
        for line in lines:
            pro = eval(line)
            info = [pro['asin'],'',pro['brand'],'','','','',pro['title'],str(pro['image_list'])]
            print (str(info))
            ff.write('\t'.join(info) + '\n')
