import sys

def handle():
    print ('handle()...')
    with open('par_pro_info.txt') as f:
        lines = f.readlines()
    with open('de_toys_pro.csv','aw') as f:
        #f.write('product_id\turl\ttitle\tbrand\tprice\treviews\tcategory1\tcategory2\tcategory3\tcategory4\tcategory5\tcategory6\timg1\timg2\timg3\n')
        for line in lines:
            info = eval(line)
            category = info['category']
            category.reverse()
            if len(category) < 6:
                category += [{'category_id':'','category_name':''} for _i in range(6 - len(category))]
            print (type(category),category[5])
            img = info['image_list']
            if len(img) < 3:
                img += ['' for _i in range(3 - len(img))]
            pro = info['asin'] + '\thttp://www.amazon.de/dp/' + info['asin'] + '\t' +info['title'].replace('\t',' ').replace('\n',',') + '\t' + info['brand'] + '\t' + info['price'].split('-')[0] + '\t' + info['reviews'] + '\t' + category[0]['category_name'] + '\t' + category[1]['category_name'] + '\t' + category[2]['category_name'] + '\t' + category[3]['category_name'] + '\t' + category[4]['category_name'] + '\t' + category[5]['category_name'] + '\t' + img[0] + '\t' + img[1] + '\t' + img[2]
            print (pro)
            f.write(pro + '\n')
if __name__=='__main__':
    handle()
    print ('end')
