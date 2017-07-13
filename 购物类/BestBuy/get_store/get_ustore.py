import re
import random
import requests

def create_titles(filename, titles):
    f = open(filename, "w")
    f.write("\t".join(titles) + "\n")
    #清除内部缓冲区
    f.flush()
    #关闭文件
    f.close()

def get_info(file_name):
    global false, true, null
    false = False
    true = True
    null = None

    file_id = open("./test.json", "r")
    titles = ['skuid','store1','sit','store2','sit','store3','sit','store4','sit','have']

    # 调用函数create_titles
    create_titles(file_name, titles)

    Ids = file_id.readlines()
    print (len(Ids))
    # result_file = open(result_file, "aw")
    # with open('./Result/items.xls','aw') as f:
    a=Ids[0]
    b=eval(a)
    situlist = []
    c=b['storeAvailabilities'][0:4]
    skuId=c[0]['skuAvailabilities'][0]['sku']
    print  (skuId)
    situlist.append(str(skuId))
    store1=c[0]['store']['name']
    have=[]
    for i in range(4):
        situlist.append(c[i]['store']['name'])
        if c[i]['skuAvailabilities'][0]['availabilityType']=='InStore':
            situlist.append('2')
            have.append(c[i]['store']['name'])

    situlist.append(have[0])
    result_file.write("\t".join(situlist) + "\n")


    #result_file.write("\t".join(goods_info) + "\n")




if __name__ == "__main__":
    global result_file,file_name
    file_name = './Result/Audio/Car_Audio_Stereo5.csv'

    result_file = open(file_name,'aw')

    get_info(file_name)
