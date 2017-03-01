# coding:utf-8

__author__ = 'Tacey Wong'

"""

过滤掉已经处理的图片url的临时脚本
(须配置URL_FILE为当前处理处理的图片url文件)
(由于使用的是相对路径，须放在图片处理程序的同级目录运行)

"""

import os

URL_FILE = "./xab"

image_list = open("./image_list.txt")

for line in image_list:
    try:
        url = eval(line)
        # print cate_url['source_url']
        with open(URL_FILE, "a") as url_file:
            url_file.write(url['source_url'].strip() + '\n')
    except Exception, e:
        print e

cmd1 = "cat ./error/error.txt >> %s" % URL_FILE
cmd2 = "sort %s | uniq -u > ./url_tmp" % URL_FILE
cmd3 = "cat ./image_list.txt >> ./bak/image_list.txt"
cmd4 = "cat ./s3_list.txt >> ./bak/s3_list.txt"
cmd5 = "cat ./error/error.txt >> ./bak/error_list.txt"
cmd6 = "rm ./*.txt"
cmd7 = "rm ./nohup.out"
cmd8 = "rm ./error/error.txt"
cmd9 = "rm %s" % URL_FILE
cmd10 = "mv ./url_tmp %s" % URL_FILE

if not os.path.exists("./bak"):
    os.mkdir("./bak")

try:
    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
    os.system(cmd4)
    os.system(cmd5)
    os.system(cmd6)
    os.system(cmd7)
    os.system(cmd8)
    os.system(cmd9)
    os.system(cmd10)
except Exception, e:
    print e

print "\nDone!\n"
