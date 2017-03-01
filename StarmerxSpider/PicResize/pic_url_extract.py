# coding:utf-8


import time
import os

__author__ = "Tacey Wong"

'''
图片url提取的临时性脚本

工作流中可能会用到的linux命令

[sed -n 10,20p 1.txt > 2.txt]
提取1.txt文件中的第10行到第20行数据并存到2.txt文件

[sed -n "10,$"p 1.txt > 2.txt]
提取1.txt文件中的第10行到最后行数据并存到2.txt文件


[head -100 1.txt > 2.txt]
提取1.txt文件中的前100行数据并存到2.txt文件

[tail -100 1.txt > 2.txt]
提取1.txt文件中的末尾100行数据并存到2.txt文件

[sort -u 1.txt > 2.txt]
将1.txt去重（多行相同只保留一个），并将结果保存在2.txt

[sort 1.txt | uniq -u > 2.txt]
将1.txt去重（多行相同,一个不留），并将结果保存在2.txt

'''


def extract_s(filename):
    """
    功用：提取指定json文件中的图片url并保存到文件
    参数：
        filename:json文件名（该文件须放在当前目录下）
    返回:None
    """
    f = open(filename)
    for line in f:
        try:
            item = eval(line.strip())
        except Exception , e:
            print e
            continue
        tmp_url =[]
        try:
            tmp_url.extend(item['image'])
            if item.has_key('attributes'):
                for attr in item['attributes']:
                    tmp_url.extend(attr['image'])
            tmp_url = list(set(tmp_url))
            with open("image_urls.txt","a") as f:
                f.write("\n".join(tmp_url)+'\n')
        except Exception ,e :
                    print e


def extract(filename,catenames):
    """
    功用：从完整json文件中提取参数列表指定的子品类的json数据及url
         并按照品类名分别保存到不同的文件
    参数：
        catenames:品类名称列表
        filename:json文件名
    返回:None
    """
    all_json= open(filename)
    for line_num , line in enumerate(all_json):
        print 'Have deal %s items' % line_num
        try:
            item = eval(line.strip())
            item_cate = item['cate_url']
        except Exception , e:
            print e
            continue

        for catename in catenames:

            if catename in item_cate:
                try:
                    tmp_url =[]
                    tmp_url.extend(item['image'])
                    if item.has_key('attributes'):
                        for attr in item['attributes']:
                            tmp_url.extend(attr['image'])
                    with open(catename.replace(" ","_").replace("'","_")+"_json.txt" ,"a") as f:
                        f.write(line.strip()+'\n')
                    tmp_url=list(set(tmp_url))
                    with open(catename.replace(" ","_").replace("'","_")+"_url.txt" ,"a") as f:
                        f.write("\n".join(tmp_url)+'\n')
                except Exception , e:
                    print e
                    continue
            else:
                with open("other_json.txt","a") as f:
                    f.write(line.strip()+'\n')
    all_json.close()


def extract_csv(base_path,catenames):
    """
    功用：在一个目录下所有的csv文件中提取指定子品类的json数据
         及图片url，并按照品类名分别保存到不同的文件
    参数：
        base_path:csv文件所在目录地址
        catenames：品类名称列表
    返回:None
    """
    for f in os.listdir(base_path):
        if f.endswith(".csv"):
            extract(f,catenames)






if __name__ == "__main__":
    time_start = time.time()

    catenames = ["Men's Accessories > Ties"]

    # extract(catenames)

    # extract_csv("./",catenames)

    extract_s("../results/ebay/2016/1031/products.txt")

    time_end = time.time()

    print "Cost %s\n" % (time_end-time_start)
    print "\nDone\n"


