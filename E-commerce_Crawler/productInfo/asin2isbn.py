# 先运行text.py，获得./Result/result 在字典里找'detail'对应的value，再在value的'EVN‘里着对应的isbn

'''把获取到的api数据中提取isbn并保存'''
def isbn_file_save():
    result_file = open('./result.txt','r').readlines()
    isbn_file = open('./isbn_part2.txt','w')
    # asin_file = open('./Result/asin_done_part2.txt','aw')

    result = []
    for results in result_file:
        results = results.split('\n')[0]
        result.append(results)

    inf = ''
    try:
        for isbns in result:
            isbns_dict = eval(isbns)
            isbns = isbns_dict['detail']

            if isbns.has_key('EAN'):
                isbn_file.write(isbns['EAN']+'\n')
            elif isbns.has_key('EANList'):
                isbn_file.write(isbns['EANList']['EANListElement']+'\n')
            # elif isbns.has_key('EISBN'):
            #     isbn_file.write(isbns['EISBN'] + '\n')
            else:
                isbn_file.write(isbns_dict['asin']+'\n')

            # except Exception,e:
            #     print isbns_dict['asin']
            #     isbn_file.write(isbns_dict['asin'])
            #     print '-------------'
                # print isbns
    except Exception as e:
        print (e)

'''测试amazon的数据抓取'''
def text_amazon():
    for amazon_result in open('./amazon_spider.txt','r').readlines():

        print (amazon_result)


if __name__ == '__main__':
    # text_amazon()

    isbn_file_save()