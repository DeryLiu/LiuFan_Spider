import sys
import reload

reload(sys)
sys.setdefaultencoding('utf8')

def handle():
    print ('handle()...')
    with open('result11.txt') as f:
        lines = f.readlines()
    with open('buybox211.csv','aw') as f:
        f.write('asin\tISBN-10\tISBN-13\ttitle\tauthor\tbinding\tpublication_date\tweight\tdescription\tdetail\timg1\timg2\timg3\n')
        for line in lines:
            info = eval(line)
            if info['detail'].has_key('ISBN'):
                isbn_10 = info['detail']['ISBN']
                ISBN_10 = 'ISBN-10:' + isbn_10 + '<br>'
                if info['detail'].has_key('EAN'):
                    isbn_13 = info['detail']['EAN']
                    ISBN_13 = 'ISBN-13:' + isbn_13 + '<br>'
                else:
                    isbn_13 = ''
                    ISBN_13 = ''
            else:
                isbn_10 = ''
                isbn_13 = ''
                ISBN_10 = ''
                ISBN_13 = ''
                
            if info['detail'].has_key('Author'):
                author = str(info['detail']['Author']).replace('[','').replace(']','').replace("'",'').replace('\n','')
            else:
                author = 'Unknown.'
            binding = info['detail']['Binding']
            if info['detail'].has_key('PublicationDate'):
                publication_date = info['detail']['PublicationDate']
            else:
                publication_date = ''
            if info['detail'].has_key('NumberOfPages'):
                pages = binding + ':' + info['detail']['NumberOfPages'] + ' pages<br>'
            else:
                pages = binding + '<br>'
                
            weight = ''
            ship_weight = ''
            if info['detail'].has_key('PackageDimensions'):
                if info['detail']['PackageDimensions'].has_key('Weight'):
                    weight = str(float(info['detail']['PackageDimensions']['Weight'])/100) + ' pounds'
                    ship_weight = 'Shipping Weight:' + weight + '<br>'
            
            if info['detail'].has_key('Publisher'):
                publisher = 'Publisher:' + info['detail']['Publisher'] + '(' + publication_date + ')<br>'
            else:
                publisher = ''
            language = 'Languages:English<br>'
            detail = pages + publisher + language + ISBN_10 + ISBN_13 + ship_weight
            
            img = info['image_list']
            if len(img) < 3:
                img += ['' for _i in range(3 - len(img))]
            pro = info['asin'] + '\t' + isbn_10 + '\t' + isbn_13 + '\t' +info['title'].replace('\t',' ').replace('\n',',') + '\t' + author + '\t' + binding + '\t' + publication_date + '\t' + weight + '\t' + info['description'].replace('\n','') + '\t' + detail + '\t' + img[0] + '\t' + img[1] + '\t' + img[2]
            print (pro)
            f.write(pro + '\n')
if __name__=='__main__':
    handle()
    print ('end')
