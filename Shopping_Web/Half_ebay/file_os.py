import os

def qvzong():
    for i in os.listdir('/home/ytroot/桌面/Update_file/'):
        with open('/home/ytroot/桌面/Update_file/'+i,'r') as asin_file:
            with open('/home/ytroot/桌面/Update_file/zong_file.txt','a') as zong:
                zong.write(asin_file.read())

    with open('/home/ytroot/桌面/WorkSpaceLHW/Half.ebay/Data/snatch/total_asin.txt','r') as total_file:
        total_all = total_file.readlines()
    total = []
    for tt in total_all:
        total.append(tt.replace('\n',''))

    print (len(total))

    with open('/home/ytroot/桌面/Update_file/zong_file.txt','r') as zong_file:
        muyqian_all = zong_file.readlines()

    muyqian = []
    for zz in muyqian_all:
        muyqian.append(zz.replace('\r','').replace('\n',''))

    print (len(muyqian))

    last = list(set(total) - set(muyqian))
    print (len(last))

    print (len(list(set(total)&set(muyqian))))

    with open('/home/ytroot/桌面/Update_file/last.txt','a') as last_file:
        for ll in last:
            last_file.write(ll+'\n')

'''把每天抓取的文件合成一份'''
def Hebing():
    on_shelf = '/home/ytroot/桌面/onshelf_info.csv'
    half_info = '/home/ytroot/桌面/half_info.csv'
    not_crawl = '/home/ytroot/桌面/not_crawl.txt'
    on_shelf_file = open(on_shelf,'aw')
    half_info_file = open(half_info,'aw')
    # not_crawl_file = open(not_crawl,'aw')

    on_shelf_list = []
    for item1 in open('/home/ytroot/桌面/info/onshelf_info1.csv','r').readlines():
        item1 = item1.split('\n')[0]
        on_shelf_list.append(item1)
    for item2 in open('/home/ytroot/桌面/info/onshelf_info2.csv','r').readlines():
        item2 = item2.split('\n')[0]
        on_shelf_list.append(item2)
    for item3 in open('/home/ytroot/桌面/info/onshelf_info3.csv', 'r').readlines():
        item3 = item3.split('\n')[0]
        on_shelf_list.append(item3)
    for item4 in open('/home/ytroot/桌面/info/onshelf_info4.csv','r').readlines():
        item4 = item4.split('\n')[0]
        on_shelf_list.append(item4)
    for item5 in open('/home/ytroot/桌面/info/onshelf_info5.csv','r').readlines():
        item5 = item5.split('\n')[0]
        on_shelf_list.append(item5)
    for item6 in open('/home/ytroot/桌面/info/onshelf_info6.csv','r').readlines():
        item6 = item6.split('\n')[0]
        on_shelf_list.append(item6)
    for item7 in open('/home/ytroot/桌面/info/onshelf_info7.csv','r').readlines():
        item7 = item7.split('\n')[0]
        on_shelf_list.append(item7)
    for item8 in open('/home/ytroot/桌面/info/onshelf_info8.csv','r').readlines():
        item8 = item8.split('\n')[0]
        on_shelf_list.append(item8)
    for item9 in open('/home/ytroot/桌面/info/onshelf_info9.csv','r').readlines():
        item9 = item9.split('\n')[0]
        on_shelf_list.append(item9)
    for item_z in on_shelf_list:
        on_shelf_file.write(item_z+'\n')

    half_info_list = []
    for item1 in open('/home/ytroot/桌面/info/half_info1.csv', 'r').readlines():
        item1 = item1.split('\n')[0]
        half_info_list.append(item1)
    for item2 in open('/home/ytroot/桌面/info/half_info2.csv', 'r').readlines():
        item2 = item2.split('\n')[0]
        half_info_list.append(item2)
    for item3 in open('/home/ytroot/桌面/info/half_info3.csv', 'r').readlines():
        item3 = item3.split('\n')[0]
        half_info_list.append(item3)
    for item4 in open('/home/ytroot/桌面/info/half_info4.csv', 'r').readlines():
        item4 = item4.split('\n')[0]
        half_info_list.append(item4)
    for item5 in open('/home/ytroot/桌面/info/half_info5.csv', 'r').readlines():
        item5 = item5.split('\n')[0]
        half_info_list.append(item5)
    for item6 in open('/home/ytroot/桌面/info/half_info6.csv', 'r').readlines():
        item6 = item6.split('\n')[0]
        half_info_list.append(item6)
    for item7 in open('/home/ytroot/桌面/info/half_info7.csv', 'r').readlines():
        item7 = item7.split('\n')[0]
        half_info_list.append(item7)
    for item8 in open('/home/ytroot/桌面/info/half_info8.csv', 'r').readlines():
        item8 = item8.split('\n')[0]
        half_info_list.append(item8)
    for item9 in open('/home/ytroot/桌面/info/half_info9.csv', 'r').readlines():
        item9 = item9.split('\n')[0]
        half_info_list.append(item9)
    for item_y in half_info_list:
        half_info_file.write(item_y + '\n')

    # not_crawl_list = []
    # for item1 in open('/home/ytroot/桌面/info/not_crawl1.txt', 'r').readlines():
    #     item1 = item1.split('\n')[0]
    #     not_crawl_list.append(item1)
    # for item2 in open('/home/ytroot/桌面/info/not_crawl2.txt', 'r').readlines():
    #     item2 = item2.split('\n')[0]
    #     not_crawl_list.append(item2)
    # for item3 in open('/home/ytroot/桌面/info/not_crawl3.txt', 'r').readlines():
    #     item3 = item3.split('\n')[0]
    #     not_crawl_list.append(item3)
    # for item4 in open('/home/ytroot/桌面/info/not_crawl4.txt', 'r').readlines():
    #     item4 = item4.split('\n')[0]
    #     not_crawl_list.append(item4)
    # for item5 in open('/home/ytroot/桌面/info/not_crawl5.txt', 'r').readlines():
    #     item5 = item5.split('\n')[0]
    #     not_crawl_list.append(item5)
    # for item6 in open('/home/ytroot/桌面/info/not_crawl6.txt', 'r').readlines():
    #     item6 = item6.split('\n')[0]
    #     not_crawl_list.append(item6)
    # for item7 in open('/home/ytroot/桌面/info/not_crawl7.txt', 'r').readlines():
    #     item7 = item7.split('\n')[0]
    #     not_crawl_list.append(item7)
    # for item8 in open('/home/ytroot/桌面/info/not_crawl8.txt', 'r').readlines():
    #     item8 = item8.split('\n')[0]
    #     not_crawl_list.append(item8)
    # for item_y in not_crawl_list:
    #     not_crawl_file.write(item_y + '\n')

'''把抓过的asin从total_asin_everyday20w文件删掉'''
def lalalla():
    total_asin_offshelf_file = []
    for total_asin_offshelf in open('./Data/snatch/1468148.txt','r').readlines():
        total_asin_offshelf = total_asin_offshelf.split('\n')[0]
        if total_asin_offshelf == '\n':
            pass
        total_asin_offshelf_file.append(total_asin_offshelf)

    for part_day20 in total_asin_offshelf_file[:400000]:
        if part_day20 == '\n':
            pass
        else:
            with open('./Data/snatch/total_asin_offshelf_part2.txt','aw') as part_day20_file:
                part_day20_file.write(part_day20+'\n')

    for total_asin_item in total_asin_offshelf_file[400000:]:
        with open('./Data/snatch/1468148_.txt','aw') as total_asin_file:
            total_asin_file.write(total_asin_item+'\n')

if __name__ == '__main__':
    # qvzong()

    # Hebing()
    lalalla()