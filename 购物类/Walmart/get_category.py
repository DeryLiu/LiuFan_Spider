import os
import requests
from Tools import get_html

#通过api获取分类信息，保存为category.txt、category_id以及去重的category_id_last.txt
def get_category():

    print ('')
    global category_file
    category_file=open('./result/category.txt','w')
    category_id_file=open('./result/category_id.txt','w')
    file={'1':'I    ','2':'II    ','3':'III    ','4':'IV    ','5':'V    '}
    
    key=['f7fqv4jzcdr7ccfb2b339cv9','fmwnnrwf53d6c5sw7b4pu2q3','7sd4rpjfmdurwuwzgvpbffd2','jqpyjz92jmaruene4mpbe8pc',
         'z2pqv4dtuwhxe3hkesx9kqpv','nz2gzu5byp9dbnm6jee69jkp' ,'sfpw74s5yte8dj9r9atzyc5m ','2tk5sghn56mnth5uabspkdt6']
    url='http://api.walmartlabs.com/v1/taxonomy?apiKey=2tk5sghn56mnth5uabspkdt6'
    info=get_html.get_html(url)
    info=eval(info)
    categories=info['categories']
    
    print (len(categories))
    for category in categories:
        category1=category['name']
        category1_id=category['id']
        category_file.write(file['1']+category1+'\t'+category1_id+'\n')
        category_file.flush()
        category2_info=category['children']
        print (category2_info)
        for category2_all in category2_info:
            category2=category2_all['name']
            category2_id=category2_all['id']
            category_file.write('\t'+file['2']+category2+'\t'+category2_id+'\n')
            category_file.flush()
            category3_info=category['children']
            for category3_all in category3_info:
                category3=category3_all['name']
                category3_id=category3_all['id']
                category_file.write('\t\t'+file['3']+category3+'\t'+category3_id+'\n')
                category_file.flush()
                if category3_all.has_key('children'):
                    category4_info=category3_all['children']
                    for category4_all in category4_info:
                        category4=category4_all['name']
                        category4_id=category4_all['id']
                        category_file.write('\t\t\t'+category4+'\t'+category4_id+'\n')
                        category_file.flush()
                        category_id_file.write(category4_id+'\n')
                        category_id_file.flush()
                        if category4_all.has_key('children'):
                            category5_info =category4_all['children']
                            print (category5_info)
                else:
                    category_id_file.write(category3_id+'\n')
                    category_id_file.flush()
    category_file.close()
    category_id_file.close()

if __name__=="__main__":
    get_category()
    os.system('sort -u '+'./result/category_id.txt'+' > '+'./result/category_id_last.txt')
    