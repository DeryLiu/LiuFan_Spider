import re

'''
    获取品类并转成字典返回
'''
def get_cate():
    with open('./result/cate_url.txt') as f:
        lines=f.readlines()
    cate_list={}
    for line in lines:
        split=line.replace('\n','').split('|')
        cate_list[split[1]]=split[0]
    return cate_list



'''
    选择抓取品类
'''
def judge(input_num,lenth):
    if input_num=='':
        exit()
    input_num=int(input_num)
    if input_num in range(1,lenth+1):
        return 1
    else:
        return 0

def select_category():
    category=get_cate()
    length=len(category)
    for i in range(length):
        print (i,category.keys()[i])
    num_cate=input('Select category:')
    if judge(num_cate,length):
        cate=category.keys()[int(num_cate)]
        url=category.values()[int(num_cate)]
    else:
        print ('Input number is not legal, please re-enter.')
        select_category()
    return cate,url

'''
   截取解析url的部分
'''
def input_num():
   begin_num = input("please input begin number: ")
   while "y" != input("Sure(y/n)?"):
       begin_num = input("please input begin number: ")
   end_num = input("please input end number: ")
   while "y" != input("Sure(y/n)?"):
       end_num = input("please input end number: ")
   return str(begin_num),str(end_num)


