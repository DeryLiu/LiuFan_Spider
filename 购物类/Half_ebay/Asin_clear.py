from multiprocessing import Lock,Pool
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import time
from Tools import ALL_CONFIG,get_html

#保存cate的id
def categorys_id_save():
    #获取cateid
    categories_file = open('./Data/categorys.txt')
    lines = categories_file.readlines()
    cate_ids = []
    categorys_id = open('./Data/categorys_id.txt','aw')
    for line in lines:
        split = line.replace("\n", "").split("|")
        if -1 != split[1].find("True"):
            cate_ids.append(split[0])

    for cate_id in cate_ids:
        categorys_id.write(cate_id+'\n')

#把每一个文件内的asin去重
def cleaned_single():

    cate_ids_file = open('./Data/categorys_id.txt','r')
    cate_id_file = cate_ids_file.readlines()
    for cate_id in cate_id_file:
        cate_id = cate_id.split("\n")[0]

        # 去重后文件
        # handle = open('./Data/asin_clean/'+cate_id+'_cleaned.txt')

        #读取去重前文件
        try:
            cate_isbn_file = open('./Data/asin_result/'+cate_id+'/asins_more.txt','r')

            os.system('sort -u ' + './Data/asin_result/'+cate_id+'/asins_more.txt' + '>' + './Data/asin_clean/'+cate_id+'_cleaned.txt')

        except Exception as e:
            print (e)

#把所有文件内的asin去重
def cleaned_all():
    cate_ids_file = open('./Data/categorys_id.txt', 'r')
    cate_id_file = cate_ids_file.readlines()

    total_asin_prime = open('./Data/total_asin_prinme.txt','aw')

    cate_id_list = []
    for cate_id in cate_id_file:
        cate_id = cate_id.split("\n")[0]
        cate_id_list.append(cate_id)

    for cate_id_item in cate_id_list:
        try:
            cate_isbn_file = open('./Data/asin_result/' + cate_id_item + '/asins_more.txt', 'r').read()

            for cate_isbn in cate_isbn_file:
                total_asin_prime.write(cate_isbn)
                continue
        except Exception as e:
            print (e)

    os.system('sort -u ' + './Data/total_asin_prinme.txt' + '>' + './Data/total_asin.txt')

#去掉已上架的
def onShelf_clean():
    #去掉已上架的总asin
    total_asin_file = open("./Data/total_asin_offshelf.txt",'aw')

    #去重总Asin
    total_asin = []
    for total_asin_item in open("./Data/total_asin.txt",'r').readlines():
        total_asin_item = total_asin_item.split("\n")[0]
        total_asin.append(total_asin_item)

    onshelf_file_list = ['./Data/OnShelves/Ca_even.csv','./Data/OnShelves/USA_even.csv','./Data/OnShelves/USA_stanford1.csv',
                         './Data/OnShelves/USA_stanford2.csv','./Data/OnShelves/USA_stanford3.csv','./Data/OnShelves/USA_stanford4.csv',
                         './Data/OnShelves/USA_stanford5.csv','./Data/OnShelves/USA_sun.csv','./Data/OnShelves/USA_union.csv']

    onshelf_file_asin = []
    for onshelf_file in onshelf_file_list:
        onshelf_asin_file = open(onshelf_file,'r').readlines()
        for onshelf_asin_item in onshelf_asin_file:
            onshelf_asin_item = onshelf_asin_item.split('\n')[0]
            onshelf_file_asin.append(onshelf_asin_item)



    result_list = list(set(total_asin) - set(onshelf_file_asin))
    for result in result_list:
        total_asin_file.write(result+'\n')

    # for item in onshelf_file_asin:
    #     if item in total_asin:
    #         continue
    #     total_asin_file.writelines(item)

# 截取前20w
def asin_everyday():
    asin_file = open('./Data/total_asin_offshelf.txt','r').readlines()
    asin_now_file = open('./Data/total_asin_offshelf_0-20.txt','aw')
    # print len(asin_file)
    for asin in asin_file[:200000]:
        asin = asin.split('\n')[0]
        asin_now_file.write(asin+'\n')


#发送文件
def send_email(infofile):
    #创建一个带附件的实例
    msg = MIMEMultipart()
    #构造附件1
    att1 = MIMEText(open(infofile, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="update_info_part.zip"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
    msg.attach(att1)
    #加邮件头
    #to_list=['liz0505@starmerx.com','lujuan@starmerx.com','lily@starmerx.com','jiping@starmerx.com']#发送给相关人员
    to_list=['hengwei@starmerx.com']
#     to_list=['3394722605@qq.com']
    msg['to'] = ';'.join(to_list)
    msg['from'] = 'hengwei@starmerx.com'
    msg['subject'] = 'test'
    #发送邮件
    try:
        server = smtplib.SMTP()
        server.connect('smtp.exmail.qq.com')
        server.login('hengwei@starmerx.com','Lianyu2016')#XXX为用户名，XXXXX为密码
        server.sendmail(msg['from'], to_list,msg.as_string())
        print ('发送成功',infofile)
    except Exception as e:
        print ('发送失败',e)
        #server.quit()
        send_email(infofile)
    finally:
        server.quit()

if __name__ == '__main__':

    # cleaned_all()
    # cleaned_single()
    # categorys_id_save()
    # onShelf_clean()
    asin_everyday()

    # send_email('./Data/total_asin.txt')


