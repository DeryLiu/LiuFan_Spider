from multiprocessing import Pool
import operator
import re
import requests
from Tools.AMAZON_API.amazon_api.Amazon_api import Amazon_AWS,Amazon_MWS
# from pro_db_models.models.market_product_models import *


seller_url = 'http://www.amazon.com/s/ref=sr_fapo?me=[seller_id]&rh=i%3Amerchant-items&page=[page]&ie=UTF8&lo=merchant-items&fap=1'
config_reg_all_count = r'<h2 id="s-result-count" class="a-size-base a-spacing-small a-spacing-top-small a-text-normal">.*? of (.*?) result'
per_count = 60


class NewStorefrontUrl:

    def __init__(self, seller_id, page):
        self.url = seller_url.replace('[seller_id]', seller_id).replace('[page]', str(page))
        
        print (self.url)

    def get_url(self):
        try:
            return self.url
        except Exception as e:
            print (e, 'location:StorefrontUrlManager get_url')
            return None
  
class ProductAreast:
    def get_page_html(self, url):
        try:
            headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.12 Safari/537.4"}
            req = requests.get(url,None,headers,timeout=10)
            stust = req.status_code
            if stust ==404:
                return 404
            else:
                html_source = req.text
                req.close()
                return html_source
        except Exception as e:
            print (e)
            return ""

    def parse_html(self, html_source):
        import lxml.html as HTML
        root = HTML.document_fromstring(html_source)
        with open('test.html','w') as f:
            f.write(html_source)
        class_name = re.findall(r'<li id="result_\d+".*? class="(.*?)"', html_source)
        if class_name:
            class_name = class_name[0]
        else:
            class_name = "s-result-item  celwidget"
        print (class_name)
        pdivs = root.xpath(".//li[@class='"+class_name+"']")
        print ('len', len(pdivs))
        products = []
        if len(pdivs)==0: 
            return products
        for pdiv in pdivs:
            try:
                product = {}
                ASIN = pdiv.xpath("./@data-asin")
            
                link = pdiv.xpath(".//a[@class='a-link-normal a-text-normal']/@href")
            
                image = pdiv.xpath(".//a[@class='a-link-normal a-text-normal']/img/@src")

                title = pdiv.xpath(".//h2[@class='a-size-base a-color-null s-inline s-access-title a-text-normal']/text()")

                price = pdiv.xpath(".//span[@class='a-color-price']/text()|.//span[@class='a-size-base a-color-price s-price a-text-bold']/text()")

                isfba = len(pdiv.xpath(".//i[@class='a-icon a-icon-prime a-icon-small s-align-text-bottom']"))
                review=pdiv.xpath(".//a[@class='a-size-small a-link-normal a-text-normal']/text()")
                
                try:
                    product['ASIN'] = ASIN[0]
                except:
                    product['ASIN'] = ''
                    
                    
                try:
                    product['link'] = link[0]
                except:
                    product['link'] = ''
                    
                try:
                    product['image'] = image[0]
                except:
                    product['image'] = ''
                try:
                    product['title'] = title[0]
                except:
                    product['title'] = ''               
                
                try:
                    product['price'] = price[0]
                except:
                    product['price'] = '0'
                    
                product['iamge_list'] = []
                


                product['isfba'] = isfba
                # can't find these code 20170117
                # product_count=MarketProductsCandidates.objects.filter(product_id=ASIN[0],market__market_name="Amazon.com")
                # if product_count.exists():
                #     product['in_db']='True'
                # else:
                #     product['in_db']='False'
                # productas=MarketProductAssignment.objects.filter(product__product_id=ASIN[0],product__market__market_name="Amazon.com")
                # if productas.exists():
                #     product['in_assign']='True'
                # else:
                #     product['in_assign']='False'
                try:  
                    if review[-1]==' ':
                        product['review']=0
                    else:              
                        if len(review)==0:
                            product['review']=0
                        else:
                            product['review']=int(review[-1].replace(',',''))
                except:
                    product['review']=0
                products.append(product)
            except Exception as e:
                print (e, 'location: parse_html')
        return products

def get_products(doc):
    products = []
    flag = False
    fail_counter = 0
    cur_page_products = []
    obj = ProductAreast()
    url = 'url' in doc and doc['url'] or NewStorefrontUrl(doc['seller_id'], doc['page']).get_url()

    while flag==False:
        if fail_counter >= 5:
            break         
        
        page_html = obj.get_page_html(url)
        if page_html==404:
            print (doc['page'], 404)
            break
        try:
            cur_page_products = obj.parse_html(page_html)
        except Exception as e:
            print (e)
        if cur_page_products:
            products = cur_page_products
            flag = True
        else:
            fail_counter = fail_counter + 1            
        
    return {'page': doc['page'], 'pro': products}
  
class NewStorefront:
    def __init__(self, seller_id, page=0, netloc="www.amazon.com"):
        
        self.products = []
        self.seller_id = seller_id
        self.page = page
        self.netloc = netloc
        
    def get_storefront_products(self):
        num = 0
        if self.page != 0:
            pass
        else:
            self.page=1
        num = self.page + 1
        page_list = []
        for i in range(1, num):
            page_list.append({'seller_id': self.seller_id, 'page': i})
        pool = Pool(processes = 3)
        result = pool.map(get_products, page_list)
        pool.close()
        pool.join()
        new_res = sorted(result, key=lambda result : result['page']) 
        for k in new_res:
            if k['pro']:
                self.products += k['pro']
                
        self.products.sort(key=operator.itemgetter('review'),reverse=True)
        print ('get storefront finished')
        return 

def get_count(html):
    
    
    
    count = 0
    if html:
        
        try:
            count = re.findall(config_reg_all_count, html)
            count = count[0].replace(' ','').replace(',','')
            return int(count)
        except Exception as e:
            print (e)
            count = 0
        
    return count



def get_url_products(url,page,per_counts=20):
    
    
    products = []
    page_per_count = per_counts #每次抓取页数
    product_arest_obj = ProductAreast()
    html = product_arest_obj.get_page_html(url)
    
    count = get_count(html)
    
    if count == 0:
        
        return products,0,0
    
    page_count = count/per_count 
    if count%per_count:
        page_count += 1
        
    page_count = min([page_count,400]) #最多获取400页
    c_page_list = [i for i in range((page-1)*page_per_count+1,page*page_per_count+1)]
    
    all_page_list = [i for i in range(1,page_count+1)]
    
    
    page_list = list(set(c_page_list).intersection(set(all_page_list)))
    
    print (page_list)

    
    if page_list:
        url = url +'&page=[page]'
        url_list = []
        for page in page_list:
            url_list.append({'url':url.replace('[page]',str(page)),'page':page})
            
        pool = Pool(processes = 3)
        result = pool.map(get_products, url_list)
        pool.close()
        pool.join()
        print (len(result))
        new_res = sorted(result, key=lambda result : result['page']) 
        for k in new_res:
            if k['pro']:
                products += k['pro']
        products.sort(key=operator.itemgetter('review'),reverse=True)
        
        AMAZON_AWS = Amazon_AWS()
        for product in products:
            p_dt = AMAZON_AWS.get_product_info(product['ASIN'],'US')
            if p_dt['result']:
                product['image_list'] = p_dt['data']['image_list']
    return products,count,page_count
        

            
                        
