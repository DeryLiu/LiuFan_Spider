import os

# 111111111111111111111111111111111111111111111111111111111111111111111111

'''把所有的sun_sku文件合成一个文件 -- sun_compare.txt'''
def zip_sun_sku():
    sun = []
    for sun1 in open('/home/ytroot/桌面/Update_file/sun的SKU 1.txt','r').readlines():
        sun.append(sun1)
    for sun2 in open('/home/ytroot/桌面/Update_file/sun的SKU 2.txt','r').readlines():
        sun.append(sun2)
    for sun3 in open('/home/ytroot/桌面/Update_file/sun的SKU 3.txt', 'r').readlines():
        sun.append(sun3)
    for sun4 in open('/home/ytroot/桌面/Update_file/sun的SKU 4.txt', 'r').readlines():
        sun.append(sun4)

    for skus in sun:
        with open('/home/ytroot/桌面/Update_file/sun_compare_f.txt','aw') as sun_f:
            sun_f.write(skus)

    os.system('sort -u ' + '/home/ytroot/桌面/Update_file/sun_compare_f.txt' + ' > ' + '/home/ytroot/桌面/Update_file/sun_compare.txt')

'''把所有的even_isbn文件合成一个文件 -- sun_isbn.csv'''
def zip_sun_isbn():
    sun = []
    total_sun = open('/home/ytroot/桌面/Update_file/sun.csv', 'w')

    for sun_1 in open('/home/ytroot/桌面/Update_file/sun的ISBN 1.txt','r').readlines():
        sun_1 = sun_1.split('\n')[0]
        sun.append(sun_1)
    for sun_2 in open('/home/ytroot/桌面/Update_file/sun的ISBN 2.txt','r').readlines():
        sun_2 = sun_2.split('\n')[0]
        sun.append(sun_2)
    for sun_3 in open('/home/ytroot/桌面/Update_file/sun的ISBN 3.txt','r').readlines():
        sun_3 = sun_3.split('\n')[0]
        sun.append(sun_3)
    for sun_4 in open('/home/ytroot/桌面/Update_file/sun的ISBN 4.txt','r').readlines():
        sun_4 = sun_4.split('\n')[0]
        sun.append(sun_4)
    # for sun_5 in open('/home/ytroot/桌面/Update_file/sun5.csv','r').readlines():
    #     sun_5 = sun_5.split('\n')[0]
    #     sun.append(sun_5)

    for sun_t in sun:
        total_sun.write(sun_t+'\n')

    os.system('sort -u ' + '/home/ytroot/桌面/Update_file/sun.csv' + ' > ' + '/home/ytroot/桌面/Update_file/sun_isbn.txt')

'''把所有的even_asin文件合成一个文件 -- sun.csv'''
def zip_sun_asin():
    sun = []
    total_sun = open('/home/ytroot/桌面/Update_file/sun_a.csv', 'w')

    for sun_1 in open('/home/ytroot/桌面/Update_file/sun的ASIN 1.txt','r').readlines():
        sun_1 = sun_1.split('\n')[0]
        sun.append(sun_1)
    for sun_2 in open('/home/ytroot/桌面/Update_file/sun的ASIN 2.txt','r').readlines():
        sun_2 = sun_2.split('\n')[0]
        sun.append(sun_2)
    for sun_3 in open('/home/ytroot/桌面/Update_file/sun的ASIN 3.txt','r').readlines():
        sun_3 = sun_3.split('\n')[0]
        sun.append(sun_3)
    for sun_4 in open('/home/ytroot/桌面/Update_file/sun的ASIN 4.txt','r').readlines():
        sun_4 = sun_4.split('\n')[0]
        sun.append(sun_4)
    # for sun_5 in open('/home/ytroot/桌面/Update_file/sun_a5.csv','r').readlines():
    #     sun_5 = sun_5.split('\n')[0]
    #     sun.append(sun_5)

    for sun_t in sun:
        total_sun.write(sun_t+'\n')

    os.system('sort -u ' + '/home/ytroot/桌面/Update_file/sun_a.csv' + ' > ' + '/home/ytroot/桌面/Update_file/sun_asin.txt')

'''把sun的isbn文件均匀切割'''
def cut_sun_isbn():
    sun_usa = open('/home/ytroot/桌面/Update_file/sun_isbn.txt','r').readlines()
    suns = []

    for sun in sun_usa:
        sun = sun.split('\n')[0]
        suns.append(sun.strip())

    asins_1 = open('/home/ytroot/桌面/Update_file/asins_1.csv','aw')  #usa part1
    for sun_t in suns[:315000]:
        asins_1.write(sun_t+'\n')

    asins_2 = open('/home/ytroot/桌面/Update_file/asins_2.csv','aw') # usa part1
    for sun_i in suns[315000:630000]:
        asins_2.write(sun_i+'\n')

    asins_5 = open('/home/ytroot/桌面/Update_file/asins_5.csv', 'aw')  # usa part5
    for sun_t in suns[630000:945000]:
        asins_5.write(sun_t + '\n')

    asins_6 = open('/home/ytroot/桌面/Update_file/asins_6.csv', 'aw')  # usa part6
    for sun_t in suns[945000:1260000]:
        asins_6.write(sun_t + '\n')

    asins_7 = open('/home/ytroot/桌面/Update_file/asins_7.csv', 'aw')  # usa part7
    for sun_t in suns[1260000:]:
        asins_7.write(sun_t + '\n')

    # asins_8 = open('/home/ytroot/桌面/Update_file/asins_8.csv', 'aw')  # usa part8
    # for sun_t in suns[1350000:]:
    #     asins_8.write(sun_t + '\n')

'''把sun的asin文件均匀切割'''
def cut_sun_asin():
    sun_usa = open('/home/ytroot/桌面/Update_file/sun_asin.txt', 'r').readlines()
    suns = []

    for sun in sun_usa:
        sun = sun.split('\n')[0]
        suns.append(sun)

    asins_1 = open('/home/ytroot/桌面/Update_file/asins_a1.csv', 'aw')  # usa part1
    for sun_t in suns[:315000]:
        asins_1.write(sun_t + '\n')

    asins_2 = open('/home/ytroot/桌面/Update_file/asins_a2.csv', 'aw')  # usa part1
    for sun_i in suns[315000:630000]:
        asins_2.write(sun_i + '\n')

    asins_5 = open('/home/ytroot/桌面/Update_file/asins_a5.csv', 'aw')  # usa part5
    for sun_t in suns[630000:945000]:
        asins_5.write(sun_t + '\n')

    asins_6 = open('/home/ytroot/桌面/Update_file/asins_a6.csv', 'aw')  # usa part6
    for sun_t in suns[945000:1260000]:
        asins_6.write(sun_t + '\n')

    asins_7 = open('/home/ytroot/桌面/Update_file/asins_a7.csv', 'aw')  # usa part7
    for sun_t in suns[1260000:]:
        asins_7.write(sun_t + '\n')

    # asins_8 = open('/home/ytroot/桌面/Update_file/asins_a8.csv', 'aw')  # usa part8
    # for sun_t in suns[1350000:]:
    #     asins_8.write(sun_t + '\n')

'''根据asin找到对应的sku文件'''
def find_sun_sku():
    condition_list = ['11', '1', '2', '3', '4']
    sun_sku1 = []
    sun_sku2 = []
    sun_sku5 = []
    sun_sku6 = []
    sun_sku7 = []
    # sun_sku8 = []
    sun_com = []
    # 总的数据
    for com in open('/home/ytroot/桌面/Update_file/sun_compare.txt', 'r').readlines():
        sun_com.append(com.replace('\r','').replace('\n',''))

    for sun1 in open('/home/ytroot/桌面/Update_file/asins_a1.csv', 'r').readlines():
        for cond in condition_list:
            sku1 = sun1.replace('\t','').replace('\r','').replace('\n','') + "_" + cond + "_O_MM"
            sun_sku1.append(sku1)

    for sun2 in open('/home/ytroot/桌面/Update_file/asins_a2.csv', 'r').readlines():
        for cond in condition_list:
            sku2 = sun2.replace('\t','').replace('\r','').replace('\n','') + "_" + cond + "_O_MM"
            sun_sku2.append(sku2)

    for sun5 in open('/home/ytroot/桌面/Update_file/asins_a5.csv', 'r').readlines():
        for cond in condition_list:
            sku5 = sun5.replace('\t','').replace('\r','').replace('\n','') + "_" + cond + "_O_MM"
            sun_sku5.append(sku5)
    for sun6 in open('/home/ytroot/桌面/Update_file/asins_a6.csv', 'r').readlines():
        for cond in condition_list:
            sku6 = sun6.replace('\t','').replace('\r','').replace('\n','') + "_" + cond + "_O_MM"
            sun_sku6.append(sku6)

    for sun7 in open('/home/ytroot/桌面/Update_file/asins_a7.csv', 'r').readlines():
        for cond in condition_list:
            sku7 = sun7.replace('\t','').replace('\r','').replace('\n','')+ "_" + cond + "_O_MM"
            sun_sku7.append(sku7)

    # for sun8 in open('/home/ytroot/桌面/Update_file/asins_a8.csv', 'r').readlines():
    #     for cond in condition_list:
    #         sku8 = sun8.replace('\t','').replace('\r','').replace('\n','') + "_" + cond + "_O_MM"
    #         sun_sku8.append(sku8)

    sun_com1 = list(set(sun_sku1) & set(sun_com))
    sun_com2 = list(set(sun_sku2) & set(sun_com))
    sun_com5 = list(set(sun_sku5) & set(sun_com))
    sun_com6 = list(set(sun_sku6) & set(sun_com))
    sun_com7 = list(set(sun_sku7) & set(sun_com))
    # sun_com8 = list(set(sun_sku8) & set(sun_com))


    sc1 = open('/home/ytroot/桌面/Update_file/sun_compare1.csv', 'aw')
    for sunc1 in sun_com1:
        sc1.write(sunc1+'\n')
    sc2 = open('/home/ytroot/桌面/Update_file/sun_compare2.csv', 'aw')
    for sunc2 in sun_com2:
        sc2.write(sunc2+'\n')
    sc5 = open('/home/ytroot/桌面/Update_file/sun_compare5.csv', 'aw')
    for sunc5 in sun_com5:
        sc5.write(sunc5+'\n')
    sc6 = open('/home/ytroot/桌面/Update_file/sun_compare6.csv', 'aw')
    for sunc6 in sun_com6:
        sc6.write(sunc6+'\n')
    sc7 = open('/home/ytroot/桌面/Update_file/sun_compare7.csv', 'aw')
    for sunc7 in sun_com7:
        sc7.write(sunc7+'\n')
    # sc8 = open('/home/ytroot/桌面/Update_file/sun_compare8.csv', 'aw')
    # for sunc8 in sun_com8:
    #     sc8.write(sunc8+'\n')


# 22222222222222222222222222222222222222222222222222222222222222222222222

'''把所有的even_sku文件合成一个文件 -- even_compare.txt'''
def zip_even_sku():
    even = []
    for even1 in open('/home/ytroot/桌面/Update_file/even的SKU 1.txt', 'r').readlines():
        even.append(even1)
    for even2 in open('/home/ytroot/桌面/Update_file/even的SKU 2.txt', 'r').readlines():
        even.append(even2)
    for even3 in open('/home/ytroot/桌面/Update_file/even的SKU 3.txt', 'r').readlines():
        even.append(even3)

    for ekus in even:
        with open('/home/ytroot/桌面/Update_file/even_compare_f.txt', 'aw') as sun_f:
            sun_f.write(ekus)

    os.system('sort -u ' + '/home/ytroot/桌面/Update_file/even_compare_f.txt' + ' > ' + '/home/ytroot/桌面/Update_file/even_compare.txt')

'''把所有的even_isbn文件合成一个文件 -- even_isbn.csv'''
def zip_even_isbn():
    even = []
    total_even = open('/home/ytroot/桌面/Update_file/even.csv', 'w')
    for even_1 in open('/home/ytroot/桌面/Update_file/even的ISBN 1.txt', 'r').readlines():
        even_1 = even_1.split('\n')[0]
        even.append(even_1)
    for even_2 in open('/home/ytroot/桌面/Update_file/even的ISBN 2.txt', 'r').readlines():
        even_2 = even_2.split('\n')[0]
        even.append(even_2)
    for even_3 in open('/home/ytroot/桌面/Update_file/even的ISBN 3.txt', 'r').readlines():
        even_3 = even_3.split('\n')[0]
        even.append(even_3)
    for even_t in even:
        total_even.write(even_t + '\n')

    os.system('sort -u ' + '/home/ytroot/桌面/Update_file/even.csv' + ' > ' + '/home/ytroot/桌面/Update_file/even_isbn.txt')

'''把所有的even_asin文件合成一个文件 -- even.csv'''
def zip_even_asin():
    even = []
    total_even = open('/home/ytroot/桌面/Update_file/even_a.csv', 'w')
    for even_1 in open('/home/ytroot/桌面/Update_file/even的ASIN 1.txt', 'r').readlines():
        even_1 = even_1.split('\n')[0]
        even.append(even_1)
    for even_2 in open('/home/ytroot/桌面/Update_file/even的ASIN 2.txt', 'r').readlines():
        even_2 = even_2.split('\n')[0]
        even.append(even_2)
    for even_3 in open('/home/ytroot/桌面/Update_file/even的ASIN 3.txt', 'r').readlines():
        even_3 = even_3.split('\n')[0]
        even.append(even_3)
    for even_t in even:
        total_even.write(even_t + '\n')

    os.system('sort -u ' + '/home/ytroot/桌面/Update_file/even_a.csv' + ' > ' + '/home/ytroot/桌面/Update_file/even_asin.txt')

'''把even的isbn文件均匀切割'''
def cut_even_isbn():
    #-----------------------------------------------------------------------------
    # even_ca = open('/home/ytroot/桌面/Update_file/even_isbn.txt','r').readlines()
    # evens = []
    #
    # for even in even_ca:
    #     even = even.split('\n')[0]
    #     evens.append(even.strip())
    #
    # asins_3 = open('/home/ytroot/桌面/Update_file/asins_3.csv', 'aw')  # usa part3
    # for even_t in evens[:300000]:
    #     asins_3.write(even_t + '\n')
    #
    # asins_4 = open('/home/ytroot/桌面/Update_file/asins_4.csv','aw') #ca part4
    # for even_t in evens[300000:600000]:
    #     asins_4.write(even_t+'\n')
    #
    # asins_8 = open('/home/ytroot/桌面/Update_file/asins_8.csv', 'aw')  # ca part8
    # for even_t in evens[600000:900000]:
    #     asins_8.write(even_t + '\n')
    #
    # asins_9 = open('/home/ytroot/桌面/Update_file/asins_9.csv', 'aw')  # ca part9
    # for even_t in evens[900000:1200000]:
    #     asins_9.write(even_t + '\n')
    #
    # asins_10 = open('/home/ytroot/桌面/Update_file/asins_10.csv', 'aw')  # ca part10
    # for even_t in evens[1200000:]:
    #     asins_10.write(even_t + '\n')

    #-----------------------------------------------------------------------------
    even_ca = open('/home/ytroot/桌面/Update_file/even_isbn.txt', 'r').readlines()
    evens = []

    for even in even_ca:
        even = even.split('\n')[0]
        evens.append(even.strip())
    asins_1 = open('/home/ytroot/桌面/Update_file/asins_1.csv', 'aw')  # usa part3
    for even_t in evens[:200000]:
        asins_1.write(even_t + '\n')

    asins_2 = open('/home/ytroot/桌面/Update_file/asins_2.csv', 'aw')  # usa part3
    for even_t in evens[:300000]:
        asins_2.write(even_t + '\n')

    asins_3 = open('/home/ytroot/桌面/Update_file/asins_3.csv', 'aw')  # usa part3
    for even_t in evens[:300000]:
        asins_3.write(even_t + '\n')

    asins_4 = open('/home/ytroot/桌面/Update_file/asins_4.csv','aw') #ca part4
    for even_t in evens[300000:600000]:
        asins_4.write(even_t+'\n')

    asins_5 = open('/home/ytroot/桌面/Update_file/asins_5.csv', 'aw')  # ca part4
    for even_t in evens[300000:600000]:
        asins_5.write(even_t + '\n')

    asins_6 = open('/home/ytroot/桌面/Update_file/asins_6.csv', 'aw')  # ca part4
    for even_t in evens[300000:600000]:
        asins_6.write(even_t + '\n')

    asins_7 = open('/home/ytroot/桌面/Update_file/asins_7.csv', 'aw')  # ca part4
    for even_t in evens[300000:600000]:
        asins_7.write(even_t + '\n')

    asins_8 = open('/home/ytroot/桌面/Update_file/asins_8.csv', 'aw')  # ca part8
    for even_t in evens[600000:900000]:
        asins_8.write(even_t + '\n')

    asins_9 = open('/home/ytroot/桌面/Update_file/asins_9.csv', 'aw')  # ca part9
    for even_t in evens[900000:1200000]:
        asins_9.write(even_t + '\n')

    asins_10 = open('/home/ytroot/桌面/Update_file/asins_10.csv', 'aw')  # ca part10
    for even_t in evens[1200000:]:
        asins_10.write(even_t + '\n')

'''把even的asin文件均匀切割'''
def cut_even_asin():
    # ---------------------------------------------------------------------------
    # even_ca = open('/home/ytroot/桌面/Update_file/even_asin.txt', 'r').readlines()
    # evens = []
    # # print len(even_ca)
    # for even in even_ca:
    #     even = even.split('\n')[0]
    #     evens.append(even)
    #
    # asins_3 = open('/home/ytroot/桌面/Update_file/asins_a3.csv', 'aw')  # usa part3
    # for even_t in evens[:300000]:
    #     asins_3.write(even_t + '\n')
    #
    # asins_4 = open('/home/ytroot/桌面/Update_file/asins_a4.csv', 'aw')  # ca part4
    # for even_t in evens[300000:600000]:
    #     asins_4.write(even_t + '\n')
    #
    # asins_8 = open('/home/ytroot/桌面/Update_file/asins_a8.csv', 'aw')  # ca part4
    # for even_t in evens[600000:900000]:
    #     asins_8.write(even_t + '\n')
    #
    # asins_9 = open('/home/ytroot/桌面/Update_file/asins_a9.csv', 'aw')  # ca part4
    # for even_t in evens[900000:1200000]:
    #     asins_9.write(even_t + '\n')
    #
    # asins_10 = open('/home/ytroot/桌面/Update_file/asins_a10.csv', 'aw')  # ca part4
    # for even_t in evens[1200000:]:
    #     asins_10.write(even_t + '\n')

    # -------------------------------------------------------------------------------
    even_ca = open('/home/ytroot/桌面/Update_file/even_asin.txt', 'r').readlines()
    evens = []
    # print len(even_ca)
    for even in even_ca:
        even = even.split('\n')[0]
        evens.append(even)
    asins_1 = open('/home/ytroot/桌面/Update_file/asins_a1.csv', 'aw')  # usa part3
    for even_t in evens[:300000]:
        asins_1.write(even_t + '\n')

    asins_2 = open('/home/ytroot/桌面/Update_file/asins_a2.csv', 'aw')  # usa part3
    for even_t in evens[:300000]:
        asins_2.write(even_t + '\n')

    asins_3 = open('/home/ytroot/桌面/Update_file/asins_a3.csv', 'aw')  # usa part3
    for even_t in evens[:300000]:
        asins_3.write(even_t + '\n')

    asins_4 = open('/home/ytroot/桌面/Update_file/asins_a4.csv', 'aw')  # ca part4
    for even_t in evens[300000:600000]:
        asins_4.write(even_t + '\n')

    asins_5 = open('/home/ytroot/桌面/Update_file/asins_a5.csv', 'aw')  # usa part3
    for even_t in evens[:300000]:
        asins_5.write(even_t + '\n')

    asins_6 = open('/home/ytroot/桌面/Update_file/asins_a6.csv', 'aw')  # usa part3
    for even_t in evens[:300000]:
        asins_6.write(even_t + '\n')

    asins_7 = open('/home/ytroot/桌面/Update_file/asins_a7.csv', 'aw')  # usa part3
    for even_t in evens[:300000]:
        asins_7.write(even_t + '\n')

    asins_8 = open('/home/ytroot/桌面/Update_file/asins_a8.csv', 'aw')  # ca part4
    for even_t in evens[600000:900000]:
        asins_8.write(even_t + '\n')

    asins_9 = open('/home/ytroot/桌面/Update_file/asins_a9.csv', 'aw')  # ca part4
    for even_t in evens[900000:1200000]:
        asins_9.write(even_t + '\n')

    asins_10 = open('/home/ytroot/桌面/Update_file/asins_a10.csv', 'aw')  # ca part4
    for even_t in evens[1200000:]:
        asins_10.write(even_t + '\n')

'''根据asin找到对应的sku文件'''
def find_even_sku():
    condition_list = ['11', '1', '2', '3', '4']
    even_sku1 = []
    even_sku2 = []
    even_sku3 = []
    even_sku4 = []
    even_sku5 = []
    even_sku6 = []
    even_sku7 = []
    even_sku8 = []
    even_sku9 = []
    even_sku10 = []

    even_com = []

    for com in open('/home/ytroot/桌面/Update_file/even_compare.txt', 'r').readlines():
        even_com.append(com.replace('\r','').replace('\n',''))

    for even6 in open('/home/ytroot/桌面/Update_file/asins_a1.csv', 'r').readlines():
        for cond in condition_list:
            sku6 = cond+'EVEN'+even6.replace('\r','').replace('\n','')+'_'
            even_sku6.append(sku6)

    for even7 in open('/home/ytroot/桌面/Update_file/asins_a2.csv', 'r').readlines():
        for cond in condition_list:
            sku7 = cond+'EVEN'+even7.replace('\r','').replace('\n','')+'_'
            even_sku7.append(sku7)

    for even1 in open('/home/ytroot/桌面/Update_file/asins_a3.csv', 'r').readlines():
        for cond in condition_list:
            sku1 = cond+'EVEN'+even1.replace('\r','').replace('\n','')+'_'
            even_sku1.append(sku1)

    for even2 in open('/home/ytroot/桌面/Update_file/asins_a4.csv', 'r').readlines():
        for cond in condition_list:
            sku2 = cond+'EVEN'+even2.replace('\r','').replace('\n','')+'_'
            even_sku2.append(sku2)

    for even8 in open('/home/ytroot/桌面/Update_file/asins_a5.csv', 'r').readlines():
        for cond in condition_list:
            sku8 = cond+'EVEN'+even8.replace('\r','').replace('\n','')+'_'
            even_sku2.append(sku8)

    for even9 in open('/home/ytroot/桌面/Update_file/asins_a6.csv', 'r').readlines():
        for cond in condition_list:
            sku9 = cond+'EVEN'+even9.replace('\r','').replace('\n','')+'_'
            even_sku2.append(sku9)

    for even10 in open('/home/ytroot/桌面/Update_file/asins_a7.csv', 'r').readlines():
        for cond in condition_list:
            sku10 = cond+'EVEN'+even10.replace('\r','').replace('\n','')+'_'
            even_sku2.append(sku10)

    for even4 in open('/home/ytroot/桌面/Update_file/asins_a8.csv', 'r').readlines():
        for cond in condition_list:
            sku4 = cond+'EVEN'+even4.replace('\r','').replace('\n','')+'_'
            even_sku4.append(sku4)

    for even3 in open('/home/ytroot/桌面/Update_file/asins_a9.csv', 'r').readlines():
        for cond in condition_list:
            sku3 = cond+'EVEN'+even3.replace('\r','').replace('\n','')+'_'
            even_sku3.append(sku3)

    for even5 in open('/home/ytroot/桌面/Update_file/asins_a10.csv', 'r').readlines():
        for cond in condition_list:
            sku5 = cond+'EVEN'+even5.replace('\r','').replace('\n','')+'_'
            even_sku5.append(sku5)

    even_com1 = list(set(even_sku1) & set(even_com))
    even_com2 = list(set(even_sku2) & set(even_com))
    even_com3 = list(set(even_sku3) & set(even_com))
    even_com4 = list(set(even_sku4) & set(even_com))
    even_com5 = list(set(even_sku5) & set(even_com))
    even_com6 = list(set(even_sku6) & set(even_com))
    even_com7 = list(set(even_sku7) & set(even_com))
    even_com8 = list(set(even_sku8) & set(even_com))
    even_com9 = list(set(even_sku9) & set(even_com))
    even_com10 = list(set(even_sku10) & set(even_com))


    ec1 = open('/home/ytroot/桌面/Update_file/even_compare1.csv', 'aw')
    for evenc1 in even_com1:
        ec1.write(evenc1+'\n')

    ec2 = open('/home/ytroot/桌面/Update_file/even_compare2.csv', 'aw')
    for evenc2 in even_com2:
        ec2.write(evenc2+'\n')

    ec3 = open('/home/ytroot/桌面/Update_file/even_compare3.csv', 'aw')
    for evenc3 in even_com3:
        ec3.write(evenc3 + '\n')

    ec4 = open('/home/ytroot/桌面/Update_file/even_compare4.csv', 'aw')
    for evenc4 in even_com4:
        ec4.write(evenc4 + '\n')

    ec5 = open('/home/ytroot/桌面/Update_file/even_compare5.csv', 'aw')
    for evenc5 in even_com5:
        ec5.write(evenc5 + '\n')

    ec6 = open('/home/ytroot/桌面/Update_file/even_compare6.csv', 'aw')
    for evenc6 in even_com6:
        ec6.write(evenc6 + '\n')

    ec7 = open('/home/ytroot/桌面/Update_file/even_compare7.csv', 'aw')
    for evenc7 in even_com7:
        ec7.write(evenc7 + '\n')

    ec8 = open('/home/ytroot/桌面/Update_file/even_compare8.csv', 'aw')
    for evenc8 in even_com8:
        ec8.write(evenc8 + '\n')

    ec9 = open('/home/ytroot/桌面/Update_file/even_compare9.csv', 'aw')
    for evenc9 in even_com9:
        ec9.write(evenc9 + '\n')

    ec10 = open('/home/ytroot/桌面/Update_file/even_compare10.csv', 'aw')
    for evenc10 in even_com10:
        ec10.write(evenc10 + '\n')


if __name__ == '__main__':
    # ---------------
    # zip_sun_sku()
    # zip_sun_isbn()
    # zip_sun_asin()
    # cut_sun_asin()
    # cut_sun_isbn()
    # find_sun_sku()


    zip_even_sku()
    zip_even_isbn()
    zip_even_asin()
    cut_even_isbn()
    cut_even_asin()
    find_even_sku()

