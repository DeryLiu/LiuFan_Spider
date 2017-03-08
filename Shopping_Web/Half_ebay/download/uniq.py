import re
import os
import glob
'''
    获取文件夹内所有解析结果列表
'''
def get_list():     
    filenames = glob.glob('*.csv')
    ids=[i for i in xrange(1,len(filenames)+1)]
    list=dict(zip(ids,filenames))
    return list
'''
    输入校验
'''
def judge(input_num,lenth):
    if input_num=='':
        exit()
    input_num=int(input_num)
    if input_num in range(1,lenth+1):
        return 1
    else:
        return 0
'''
    选择要去重的文件
'''
def select_category():
    category=get_list()
    for key in category:
        print (key,category[key],'\n')
    num_uniq=raw_input('Select file want to be unique:')
    if judge(num_uniq,len(category)):
        filename=category[int(num_uniq)]
        filelike=filename[:len(filename)-10]
    else:
        print ('Input number is not legal, please re-enter.')
        select_category()
    return filename,filelike
'''
    对文件进行去重处理
'''
def handle(files):
    file1=str(files[0])
    filelike=str(files[1])     
    filenames = glob.glob(filelike+'*.csv')
    for filename in filenames:
        if filename!=file1:
            print ('with file:',filename)
            with open(file1,'r+') as f1:
                lines1=f1.readlines()
                lines11=[i[:10] for i in lines1]
                with open(filename) as f2:
                    lines2=f2.readlines()
                lines22=[i[:10] for i in lines2]
                lines=[]
                for i in xrange(len(lines11)):
                    if lines11[i] not in lines22:
                        lines.append(lines1[i])
                f1.seek(0)
                f1.truncate(0)
                f1.writelines(lines)
            print ('result amount:',len(lines))


if __name__ == '__main__':
    while True:
        files= select_category()
        handle(files)
        choice=raw_input('Continue(y/n)? ')
        if choice!='y':
            break


