# -*- coding: utf-8 -*-



import pytz
import random
import HTMLParser
import time
from datetime import datetime,timedelta
from xml.dom.minidom import  parseString
from django.utils.encoding import smart_str

from ProApiandERPGateway.utils import get_element_by_tag
from ProApiandERPGateway.amazon_api.config import CONFIG_MWS,CONFIG_MPI,CONFIG_AWS,CATEGORY_ROOT,ACCESS_KEY_ID,SECRET_ACCESS_KEY,ASSOCIATE_TAG
from ProApiandERPGateway.amazon_api.amazonorder.mws import Orders,Products,Inventory,Reports,Feeds,InboundShipments,Subscriptions,\
    MWSError
from ProApiandERPGateway.amazon_api.amazonproduct import API

import Queue
import threading
import time


class Work(threading.Thread):
    def __init__(self, work_queue, result_queue, flag , lock, condition):
        threading.Thread.__init__(self)
        self._flag = {"flag" : True}
        self._lock = lock
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.wait = True
        self._condition = condition

    def run(self):
        #Dead cycle, to create threads under certain conditions close to exit
        while self._flag["flag"]:
            self._lock.acquire()
            if  self.work_queue.qsize() > 0:
                do = None
                args = None
                do, args = self.work_queue.get()#The task asynchronous dequeue, Queue internal implementation of the synchronization mechanism
                self._lock.release()
                try:
                    temp_result = do(args)
                    self.result_queue.put(temp_result)
                except Exception, e:
                    print "Unkown Exception", e
                    print str(do), str(args)
                    self.result_queue.put(None)
            else:
                self._lock.release()
                self._condition.acquire()
                self._condition.wait()
                self._condition.release()


class PoolManager(object):
    
    def __init__(self,threads=2):
        self.threads = []    
        self._flag = {"flag" : True}
        self.work_queue = Queue.Queue()
        self.work_num = 0
        self.result_queue = Queue.Queue()
        self._threadLock = threading.Lock()
        self._condition = threading.Condition()
        self.threads = threads
        self.__init_thread_pool(self.threads)
        
    def __init_thread_pool(self,threads):
        '''
        Initialization thread function 
        '''
        self.threads = []
        for i in range(threads):
            tempthreand = Work(self.work_queue, self.result_queue, self._flag, self._threadLock, self._condition)
            self.threads.append(tempthreand)
            tempthreand.start()

    def addJob(self, func, args):
        for arg in args:
            self.work_queue.put((func, arg))
            self.work_num = self.work_num + 1
        
        self.notify_all()


    def map(self, func, args):
        """
        Add a working team
        """
        for arg in args:
            self.work_queue.put((func, arg))#task enqueue, Queue internal synchronization mechanism
            self.work_num = self.work_num + 1
        
        self.notify_all()
                
        self.wait_jobscomplete()

        return self.getResult()

    def close(self):
        for t in self.threads:
            t._flag["flag"] = False
        
        self.notify_all()
    
        self.threads = []
    
    def getResult(self):
        result = []
        while self.result_queue.qsize() > 0:
            temp = self.result_queue.get()
            self.work_num = self.work_num - 1
            result.append(temp)
        return result
    
    def wait_jobscomplete(self):
        while 1:
            if self.work_num == self.result_queue.qsize():
                return 1

    def notify_all(self):
        self._condition.acquire()
        self._condition.notify_all()
        self._condition.release()

    def wait_allcomplete(self):
        """
        Wait for all threads to finish
        """   
        for item in self.threads:
            if item.isAlive():
                item.join()

    def activateFlag(self):
        '''
        all work are added into queue,
        After threads have finished all work, the threads will stop
        '''
        self._flag["flag"] = True


class create_api_exception(Exception):
    def __init__(self, value , locale):
        self.value = 'AWS.InvalidLocaleValue: ' + locale +' is not a valid value for Locale'
    def __str__(self):
        return repr(self.value)

class Amazon_AWS(object):
    '''
    amazon产品相关,主要涉及到品类树,产品信息
    '''
    threadpool = None
    graph = {}
    error_list = []
    locale = 'us'
    number = 1
    error_number = 1
    def __create_api(self,locale):
        """
        Create a API instance for request.
        @param locale: The locale where your want select.
        @return: Return a aws api.Search the key in config by locale.
        """
        try:
            random_number = int(random.randint(0, len(ACCESS_KEY_ID)-1))
            api = API(ACCESS_KEY_ID[random_number],SECRET_ACCESS_KEY[random_number],str(locale).lower(),ASSOCIATE_TAG)
#            cfg = CONFIG_AWS[locale]
#            api = API(cfg['access_key'],cfg['secret_key'],cfg['locale'],cfg['associate_tag'])
            return api
        except Exception,e:
            print 'error',str(e)
            raise create_api_exception(e,locale)
     
    def __parse_node_result(self,result):
        """Parse the result. The result source is a XML document."""
        category_list = {}
        print 'start parse node'
        category_list['name'] = result.BrowseNodes.BrowseNode.Name
        category_list['id'] = result.BrowseNodes.BrowseNode.BrowseNodeId
        category_list['leaf'] = False
        category_list['children'] = []
        try:
            for child in result.BrowseNodes.BrowseNode.Children.BrowseNode:
                category_list['children'].append(child.BrowseNodeId)
        except Exception,e:
            category_list['leaf'] = True
        return category_list
    
    def __item_lookup(self,asin, locale='US', group='Large'):
        '''
            Use item_lookup method to request a product information.
            @param asin: The asin you want get product infomation
            @param locale: The default is 'us' ,and you can set this as 'ca','cn','de','fr','jp','it','uk','us'
            @return:
                if success,this will return a product information as Json 
                if false ,if will return {'status':False,'Msg':'Not have item'}
        '''
        try:
            api = self.__create_api(locale)
            result = api.item_lookup(asin,ResponseGroup=group)
            if result['Items']['Request']['IsValid'] == 'True':
                return {'result':True,'data':result}
            else:
                return {'result':False,'error_message':'Items Request IsValid'}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
        
        
    def __item_search(self,cate, key_words,locale='US'):
        '''
            Use item_lookup method to request a product information.
            @param asin: The asin you want get product infomation
            @param locale: The default is 'us' ,and you can set this as 'ca','cn','de','fr','jp','it','uk','us'
            @return:
                if success,this will return a product information as Json 
                if false ,if will return {'status':False,'Msg':'Not have item'}
        '''
        try:
            api = self.__create_api(locale)
            result = api.item_search(cate,Keywords=key_words)
            
            print dir(result)
            print result._pagecache[1].Items.__dict__
            if result['Items']['Request']['IsValid'] == 'True':
                return {'result':True,'data':result}
            else:
                return {'result':False,'error_message':'Items Request IsValid'}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
    
    def __parse_product_result(self,result):
        """Parse the result. The result source is a XML document."""
        try:
            product = {}
            category_list = []
            try:
                node = result.Items.Item.BrowseNodes.BrowseNode
                while True:
                    category_id = node.BrowseNodeId.text
                    try:
                        node = node.Ancestors.BrowseNode
                    except Exception, e:
                        category_id = node.BrowseNodeId.text
                        category_list.append(category_id)
                        break
                    category_list.append(category_id)
            except Exception,e:
                category_list = []
                pass
            product['category'] = category_list
            product['asin'] = result.Items.Item.ASIN.text
            try:   
                product['title'] = result.Items.Item.ItemAttributes.Title.text.replace("'", "`").replace('"', '`')
            except Exception,e:
                product['title'] = 'N/A'
            try:        
                product['brand'] = result.Items.Item.ItemAttributes.Brand.text
            except Exception,e:
                product['brand'] = 'N/A'
            try:
                product['medium_image'] = smart_str(result.Items.Item.ImageSets.ImageSet.MediumImage.URL.text)
            except Exception,e:
                product['medium_image'] = ''
            product['image_list'] = []
            try:
                for ImageSet in result.Items.Item.ImageSets.iterchildren():
                    product['image_list'].append(smart_str(ImageSet.LargeImage.URL.text))
            except Exception,e:
                product['image_list'] = []
                
            try: 
                product['salesrank'] = result.Items.Item.SalesRank.text
            except Exception,e:
                product['salesrank'] = '999999'
            
            try:
                product['description'] = result.Items.Item.EditorialReviews.EditorialReview.Content.text
            except Exception, e:
                product['description'] = 'N/A'
            
            product['detail'] = {}
            # print '-----=====--result.Items.Item.ItemAttributes.__dict__----=====----'
            # print result.Items.Item.ItemAttributes.__dict__
            # print '------------------'
            for attr in result.Items.Item.ItemAttributes.iterchildren():
                attr.tag = attr.tag.replace('{http://webservices.amazon.com/AWSECommerceService/2011-08-01}', '')
                if attr.tag == 'Listprice':
                    print attr.tag
                if product['detail'].has_key(attr.tag) and attr.text is not None:
                    if type(product['detail'][attr.tag]) is not list:
                        product['detail'][attr.tag] = [product['detail'][attr.tag]]
                    product['detail'][attr.tag].append(smart_str(attr.text).replace("'", "`").replace('"', "'"))
                else:
                    if attr.text is not None:
                        product['detail'][attr.tag] = smart_str(attr.text).replace("'", "`").replace('"', "'")
                    else:
                        s = {}
                        for item in attr.iterchildren():
                            if item.text is not None:
                                item.tag = item.tag.replace('{http://webservices.amazon.com/AWSECommerceService/2011-08-01}', '')
                                s[item.tag]= item.text
                        product['detail'][attr.tag] = s
               
            return {'result':True,'data':product}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
        
        
    def __parse_products_result(self,result):
        """Parse the result. The result source is a XML document."""
        try:

            products = []
            for item in result.Items.Item:
                
                product = {}
                try:
                    product['ParentASIN'] = item.ParentASIN.text
                except:
                    product['ParentASIN'] = ''
                
                category_list = []
                try:
                    node = item.BrowseNodes.BrowseNode
                    while True:
                        category_id = node.BrowseNodeId.text
                        category_name = node.Name
                        category = {'category_id':category_id,'category_name':category_name}
                        try:
                            node = node.Ancestors.BrowseNode
                        except Exception, e:
                            category_id = node.BrowseNodeId.text
                            category_name = node.Name
                            category = {'category_id':category_id,'category_name':category_name}
                            category_list.append(category)
                            break
                        category_list.append(category)
                except Exception,e:
                    category_list = []
                    pass
                product['category'] = category_list
                product['asin'] = item.ASIN.text
                try:   
                    product['title'] = item.ItemAttributes.Title.text.replace("'", "`").replace('"', '`')
                except Exception,e:
                    product['title'] = 'N/A'
                try:        
                    product['brand'] = item.ItemAttributes.Brand.text
                except Exception,e:
                    product['brand'] = 'N/A'
                try:
                    product['medium_image'] = smart_str(item.ImageSets.ImageSet.MediumImage.URL.text)
                except Exception,e:
                    product['medium_image'] = ''
                product['image_list'] = []
                try:
                    for ImageSet in item.ImageSets.iterchildren():
                        product['image_list'].append(smart_str(ImageSet.LargeImage.URL.text))
                except Exception,e:
                    product['image_list'] = []
                    
                try: 
                    product['salesrank'] = item.SalesRank.text
                except Exception,e:
                    product['salesrank'] = '999999'
                
                try:
                    product['description'] = item.EditorialReviews.EditorialReview.Content.text
                except Exception, e:
                    product['description'] = 'N/A'
                
                product['detail'] = {}
                
                for attr in item.ItemAttributes.iterchildren():
                    attr.tag = attr.tag.replace('{http://webservices.amazon.com/AWSECommerceService/2011-08-01}', '')

                    if product['detail'].has_key(attr.tag) and attr.text is not None:
                        if type(product['detail'][attr.tag]) is not list:
                            product['detail'][attr.tag] = [product['detail'][attr.tag]]
                        product['detail'][attr.tag].append(smart_str(attr.text).replace("'", "`").replace('"', "'"))
                    else:
                        if attr.text is not None:
                            product['detail'][attr.tag] = smart_str(attr.text).replace("'", "`").replace('"', "'")
                        else:
                            s = {}
                            for item in attr.iterchildren():
                                if item.text is not None:
                                    item.tag = item.tag.replace('{http://webservices.amazon.com/AWSECommerceService/2011-08-01}', '')
                                    s[item.tag]= item.text
                            product['detail'][attr.tag] = s
                products.append(product)
                   
            return {'result':True,'data':products}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
        
        
    def __parse_products_variation(self,result):
        """Parse the result. The result source is a XML document."""
        try:

            products = []
            for item in result.Items.Item:
                for item in item.Variations.Item:
                
                    product = {}
                    try:
                        product['ParentASIN'] = item.ParentASIN.text
                    except:
                        product['ParentASIN'] = ''
                    
                    product['asin'] = item.ASIN.text
                    try:   
                        product['title'] = item.ItemAttributes.Title.text.replace("'", "`").replace('"', '`')
                    except Exception,e:
                        product['title'] = 'N/A'
                    try:        
                        product['brand'] = item.ItemAttributes.Brand.text
                    except Exception,e:
                        product['brand'] = 'N/A'
                    try:
                        product['medium_image'] = smart_str(item.ImageSets.ImageSet.MediumImage.URL.text)
                    except Exception,e:
                        product['medium_image'] = ''
                    product['image_list'] = []
                    try:
                        for ImageSet in item.ImageSets.iterchildren():
                            product['image_list'].append(smart_str(ImageSet.LargeImage.URL.text))
                    except Exception,e:
                        product['image_list'] = []
                        
                    try: 
                        product['salesrank'] = item.SalesRank.text
                    except Exception,e:
                        product['salesrank'] = ''
                    
                    try:
                        product['description'] = item.EditorialReviews.EditorialReview.Content.text
                    except Exception, e:
                        product['description'] = 'N/A'
                    
                    product['detail'] = {}
                    
                    for attr in item.ItemAttributes.iterchildren():
                        attr.tag = attr.tag.replace('{http://webservices.amazon.com/AWSECommerceService/2011-08-01}', '')
    
                        if product['detail'].has_key(attr.tag) and attr.text is not None:
                            if type(product['detail'][attr.tag]) is not list:
                                product['detail'][attr.tag] = [product['detail'][attr.tag]]
                            product['detail'][attr.tag].append(smart_str(attr.text).replace("'", "`").replace('"', "'"))
                        else:
                            if attr.text is not None:
                                product['detail'][attr.tag] = smart_str(attr.text).replace("'", "`").replace('"', "'")
                            else:
                                s = {}
                                for item in attr.iterchildren():
                                    if item.text is not None:
                                        item.tag = item.tag.replace('{http://webservices.amazon.com/AWSECommerceService/2011-08-01}', '')
                                        s[item.tag]= item.text
                                product['detail'][attr.tag] = s
                    products.append(product)
                       
            return {'result':True,'data':products}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
         
    def __browse_node_lookup(self,browse_node_id=None):
        '''
            Use browse_node_lookup method to request a node information.
            @param locale: The default is 'us' ,and you can set this as 'ca','cn','de','fr','jp','it','uk','us'
            @param browse_node_id: The tree of the node
            @return:
                                {
                    'list': {
                                                665033051: {}, 2017640051: {}
                                                }, 
                    'leaf': False, 
                    'name': u'\u8f66\u8f7d\u914d\u4ef6'
                                }
        '''
            
        try:
            category_result = {}
            if  self.graph.has_key(browse_node_id):
                return True
            api = self.__create_api(self.locale)
            if browse_node_id is None:
                category_result['id'] = ''
                category_result['name'] = 'rootNode'
                category_result['leaf'] = False
                category_result['children'] = []
                CATEGORY_ROOT_list   = CATEGORY_ROOT[self.locale]
                for browse_node_id in CATEGORY_ROOT_list:
                    category_result['children'].append(browse_node_id)
            else:
                category_result ={}
#                while True:
                return_api_lookup = api.browse_node_lookup(browse_node_id,proxy = True)
                category_result  = self.__parse_node_result(return_api_lookup)
            
            lock = self.threadpool._threadLock
            lock.acquire()
            self.graph[browse_node_id] = category_result
            print 'number = ',self.number,' , browse_node_id = ',browse_node_id
            self.number = self.number + 1
            lock.release()
            
            if category_result['leaf'] is False:
                for category_result_node in category_result['children']:
                    self.threadpool.addJob(self.__browse_node_lookup,[category_result_node])
            return True
        except Exception, e:
            print 'error_number:',self.error_number,' , browse_node_id = ',browse_node_id,' ,error:',str(e)
            self.error_number = self.error_number + 1
            self.error_list.append(browse_node_id)
            return {}

    def get_category_tree(self,locale='us',pool_number = 15):
        '''
        @param locale: The locale value,default is 'us'
        @return: 
        '''
        self.locale = locale
        self.threadpool = PoolManager(pool_number)
        self.threadpool.addJob(self.__browse_node_lookup,[None])
        self.threadpool.wait_jobscomplete()
        result = self.threadpool.getResult()
        self.threadpool.close()
        
        print 'start error node:',self.error_number
        
        limit  = 5
        
        while len(self.error_list) > 0 and limit >0:
            self.threadpool = PoolManager(pool_number)
#            print 'result1=',result
            if len(self.error_list) > 0:
                for error_each in self.error_list:
#                    print 'deal_error_node',error_each
                    self.threadpool.addJob(self.__browse_node_lookup,[error_each])
            self.threadpool.wait_jobscomplete()
            result = self.threadpool.getResult()
#            print 'result2=',result
#            print 'graph',self.graph
            self.threadpool.close()
            limit = limit - 1
        return [self.graph,self.error_list]

    def get_product_info(self,ASIN, locale='US', lists = False):
        """
        Get a product information.
        @param ASIN:The asin value.
        @param locale:The locale value,default is 'us'
        @return: 
        """
        try:
            result = self.__item_lookup(ASIN, locale)
            if result['result'] is False:
                return result
            elif result['result'] is True:
                if lists:
                    product = self.__parse_products_result(result['data'])
                else:
                    product = self.__parse_product_result(result['data'])
                
                if product['result'] is False:
                    return {'result':False,'error_message':product['error_message']}
                elif product['result'] is True:
                    if not lists:
                        product['data']['locale'] = locale
                    return {'result':True,'data':product['data']}
        except Exception, e:
            return {'result':False,'error_message':str(e)}
    def get_product_variation(self,asin,locale = 'US',group = 'Variations'):
        
        try:
            result = self.__item_lookup(asin,locale,group)
            if result['result'] is False:
                return result
            elif result['result'] is True:
                product = self.__parse_products_variation(result['data'])
                
                if product['result'] is False:
                    return {'result':False,'error_message':product['error_message']}
                elif product['result'] is True:
                    return {'result':True,'data':product['data']}
        except Exception, e:
            return {'result':False,'error_message':str(e)}
        
        
    def get_product_search(self,key_words, locale='US', group='Small'):
        """
        Get a product information.
        @param ASIN:The asin value.
        @param locale:The locale value,default is 'us'
        @return: 
        """
        try:
            result = self.__item_search('Electronics','nokia')
            if result['result'] is False:
                return result
            elif result['result'] is True:
                product = self.__parse_product_result(result['data'])
                
                if product['result'] is False:
                    return {'result':False,'error_message':product['error_message']}
                elif product['result'] is True:
                    product['data']['locale'] = locale
                    return {'result':True,'data':product['data']}
        except Exception, e:
            return {'result':False,'error_message':str(e)}


class Amazon_MWS(object):
    '''
    amazon Merchant 相关,主要涉及到   网店订单获取,网店商品获取,网店商品库存获取,网店商品上传价格,
    '''
    def __create_api(self,type,account_info):
        
        access_key = account_info.access_key
        secret_key = account_info.secret_key
        account_id = account_info.store_key
        mws_auth_token = account_info.store_token
        region = account_info.region
            
        cfg = CONFIG_MWS[region]
        
        if type == 'Orders':
            return Orders(access_key, secret_key, account_id,mws_auth_token,region = region)
        elif type == 'Inventory':
            return Inventory(access_key,secret_key, account_id,mws_auth_token,region = region)
        elif type == 'Products':
            return Products(access_key,secret_key, account_id,mws_auth_token,region = region)
        elif type == 'Reports':
            return Reports(access_key,secret_key, account_id,mws_auth_token,region = region)
        elif type == 'Feeds':
            return Feeds(access_key,secret_key, account_id,mws_auth_token,region = region)
        elif type == 'Inbounds':
            return InboundShipments(access_key,secret_key, account_id,mws_auth_token,region = region)
        elif type == 'Subscriptions':
            return Subscriptions(access_key,secret_key, account_id,mws_auth_token,region = region)        
        else:
            error_msg = "Incorrect type supplied ('%(type)s')" % {"type" : type }
            raise MWSError(error_msg)
    
    def __get_inventory_list(self,Inventory_list):
        
        members_return_list = []
        for member_data in Inventory_list:
            members_data_list ={}
            members_data_list['TotalSupplyQuantity'] = get_element_by_tag(member_data,'TotalSupplyQuantity')
            members_data_list['SellerSKU'] = get_element_by_tag(member_data,'SellerSKU')
            members_data_list['ASIN'] = get_element_by_tag(member_data,'ASIN')
            members_data_list['FNSKU'] = get_element_by_tag(member_data,'FNSKU')
            members_data_list['Condition'] = get_element_by_tag(member_data,'Condition')
            members_data_list['InStockSupplyQuantity'] = get_element_by_tag(member_data,'InStockSupplyQuantity')
            members_return_list.append(members_data_list)
        return members_return_list
        
    def __get_order_line_list(self,order_items):
        html_parser = HTMLParser.HTMLParser()
        order_line_list = []
        for each_item in order_items:
            order_line_item = {}
            order_line_item['QuantityOrdered'] = get_element_by_tag(each_item,'QuantityOrdered')
            order_line_item['Title'] = get_element_by_tag(each_item,'Title')
            order_line_item['OrderItemId'] = get_element_by_tag(each_item,'OrderItemId')
            order_line_item['CurrencyCode'] = get_element_by_tag(each_item,'CurrencyCode')
            order_line_item['ItemPrice'] = get_element_by_tag(each_item,'ItemPrice','Amount')
            order_line_item['ItemTax'] = get_element_by_tag(each_item,'ItemTax','Amount')
            order_line_item['OrderItemId'] = get_element_by_tag(each_item,'OrderItemId')        
            order_line_item['ShippingPrice'] = get_element_by_tag(each_item,'ShippingPrice','Amount')
            order_line_item['ASIN'] = html_parser.unescape(html_parser.unescape(get_element_by_tag(each_item,'ASIN')))
            order_line_item['SellerSKU'] = html_parser.unescape(html_parser.unescape(get_element_by_tag(each_item,'SellerSKU')))
    #        order_line_item['image_url'] = get_amazon_img_url(product_amazon,MKPLACEID,IdType,[ASIN])
            order_line_list.append(order_line_item)
        return   order_line_list
    
    def __deal_amazon_data(self,orders,amazon):
        return_order_list = []
        for item in orders:
            return_order = {}
            return_order['orderID'] = get_element_by_tag(item,'AmazonOrderId')
    #        print 'order_id',return_order['orderID']
            return_order['order_Status'] = get_element_by_tag(item,'OrderStatus')
            return_order['total_Amount'] = get_element_by_tag(item,'OrderTotal','Amount')
            return_order['CurrencyCode'] = get_element_by_tag(item,'OrderTotal','CurrencyCode')
            return_order['ShipServiceLevel'] = get_element_by_tag(item,'ShipServiceLevel')
            return_order['Phone'] = get_element_by_tag(item,'ShippingAddress','Phone')
            return_order['PostalCode'] = get_element_by_tag(item,'ShippingAddress','PostalCode')
            return_order['Name'] = get_element_by_tag(item,'ShippingAddress','Name')
            return_order['CountryCode'] = get_element_by_tag(item,'ShippingAddress','CountryCode')
            return_order['StateOrRegion'] = get_element_by_tag(item,'ShippingAddress','StateOrRegion')
            return_order['AddressLine1'] = get_element_by_tag(item,'ShippingAddress','AddressLine1')
            return_order['AddressLine2'] = get_element_by_tag(item,'ShippingAddress','AddressLine2')
            return_order['AddressLine3'] = get_element_by_tag(item,'ShippingAddress','AddressLine3')
            return_order['City'] = get_element_by_tag(item,'ShippingAddress','City')
            return_order['BuyerEmail'] = get_element_by_tag(item,'BuyerEmail')
            return_order['BuyerName'] = get_element_by_tag(item,'BuyerName')
            return_order['PaymentMethod'] = get_element_by_tag(item,'PaymentMethod')
            return_order['PurchaseDate'] = get_element_by_tag(item,'PurchaseDate')
    
            order_items_obj = amazon.list_order_items(return_order['orderID'])
            data_2 = order_items_obj.response.content
            dom_2 = parseString(data_2)
            next_token_item = dom_2.getElementsByTagName("NextToken")
            order_items = dom_2.getElementsByTagName("OrderItem")
            order_line_list = []
            
            order_line_list.extend(self.__get_order_line_list(order_items))
    
            while len(next_token_item) != 0:
                order_items_obj_next = amazon.list_order_items_by_next_token(next_token_item[0].childNodes[0].data)
                next_data_2 = order_items_obj_next.response.content
                next_dom_2 = parseString(next_data_2)
                next_token_item = next_dom_2.getElementsByTagName("NextToken")
                next_order_items = next_dom_2.getElementsByTagName("OrderItem")
                
                order_line_list.extend(self.__get_order_line_list(next_order_items))
                
            return_order['OrderItem'] = order_line_list
            return_order_list.append(return_order)
        return return_order_list
    
    def __get_order(self,account_info,amazon_order_id):
        
        amazon = self.__create_api('Orders',account_info)
        order = amazon.get_order(amazon_order_id)
        order = order.response.content

    def __deal_product_price(self,price_items):
        price_list = []
        for each_item in price_items:
            order_price_item = {}
            if get_element_by_tag(each_item,'Error','Code') is not '':
                order_price_item['Type'] = get_element_by_tag(each_item,'Error','Type')
                order_price_item['Code'] = get_element_by_tag(each_item,'Error','Code')
                order_price_item['Message'] = get_element_by_tag(each_item,'Error','Message')
            else:
                order_price_item['ASIN'] = get_element_by_tag(each_item,'MarketplaceASIN','ASIN')
                order_price_item['SellerSKU'] = get_element_by_tag(each_item,'SKUIdentifier','SellerSKU')
                order_price_item['SellerId'] = get_element_by_tag(each_item,'SKUIdentifier','SellerId')
                order_price_item['LowestOfferListings'] =[]
                my_price_list = each_item.getElementsByTagName("LowestOfferListing")
                for each_price in my_price_list:
                    LowestOffer = {}
                    LowestOffer['ItemCondition'] = get_element_by_tag(each_price,'Qualifiers','ItemCondition')        
                    LowestOffer['ItemSubcondition'] = get_element_by_tag(each_price,'Qualifiers','ItemSubcondition')
                    LowestOffer['FulfillmentChannel'] = get_element_by_tag(each_price,'Qualifiers','FulfillmentChannel')
                    LowestOffer['ShipsDomestically'] = get_element_by_tag(each_price,'Qualifiers','ShipsDomestically')
                    LowestOffer['ShippingTime'] = get_element_by_tag(each_price,'ShippingTime','Max')        
                    LowestOffer['SellerPositiveFeedbackRating'] = get_element_by_tag(each_price,'Qualifiers','SellerPositiveFeedbackRating')
                    
                    LowestOffer['LandedPrice_Amount'] = get_element_by_tag(each_price,'LandedPrice','Amount')        
                    LowestOffer['LandedPrice_CurrencyCode'] = get_element_by_tag(each_price,'LandedPrice','CurrencyCode')
                    LowestOffer['ListingPrice'] = get_element_by_tag(each_price,'ListingPrice','Amount')
                    LowestOffer['ListingPrice_CurrencyCode'] = get_element_by_tag(each_price,'ListingPrice','CurrencyCode')        
                    LowestOffer['Shipping'] = get_element_by_tag(each_price,'Shipping','Amount')
                    LowestOffer['Shipping_CurrencyCode'] = get_element_by_tag(each_price,'Shipping','CurrencyCode')
                    
                    LowestOffer['SellerFeedbackCount'] = get_element_by_tag(each_price,'SellerFeedbackCount')
                    LowestOffer['NumberOfOfferListingsConsidered'] = get_element_by_tag(each_price,'NumberOfOfferListingsConsidered')
                    
                    order_price_item['LowestOfferListings'].append(LowestOffer)
            price_list.append(order_price_item)
        return   price_list
  
    def __deal_product_competitive_price(self,price_items):
        price_list = []
        for each_item in price_items:
            order_price_item = {}
            if get_element_by_tag(each_item,'Error','Code') is not '':
                order_price_item['Type'] = get_element_by_tag(each_item,'Error','Type')
                order_price_item['Code'] = get_element_by_tag(each_item,'Error','Code')
                order_price_item['Message'] = get_element_by_tag(each_item,'Error','Message')
            else:
                order_price_item['ASIN'] = get_element_by_tag(each_item,'MarketplaceASIN','ASIN')
                order_price_item['SellerSKU'] = get_element_by_tag(each_item,'SKUIdentifier','SellerSKU')
                order_price_item['SellerId'] = get_element_by_tag(each_item,'SKUIdentifier','SellerId')
                order_price_item['CompetitivePricing'] =[]
                my_price_list = each_item.getElementsByTagName("CompetitivePrice")
                for each_price in my_price_list:
                    CompetitiveOffer = {}
                    
                    CompetitiveOffer['CompetitivePriceId'] = get_element_by_tag(each_price,'CompetitivePriceId')
                    CompetitiveOffer['condition'] = str(each_price.getAttribute('condition'))
                    CompetitiveOffer['subcondition'] =str(each_price.getAttribute('subcondition'))
                    CompetitiveOffer['belongsToRequester'] = str(each_price.getAttribute('belongsToRequester'))
                    
                    CompetitiveOffer['LandedPrice_Amount'] = get_element_by_tag(each_price,'LandedPrice','Amount')        
                    CompetitiveOffer['LandedPrice_CurrencyCode'] = get_element_by_tag(each_price,'LandedPrice','CurrencyCode')
                    CompetitiveOffer['ListingPrice'] = get_element_by_tag(each_price,'ListingPrice','Amount')
                    CompetitiveOffer['ListingPrice_CurrencyCode'] = get_element_by_tag(each_price,'ListingPrice','CurrencyCode')        
                    CompetitiveOffer['Shipping'] = get_element_by_tag(each_price,'Shipping','Amount')
                    CompetitiveOffer['Shipping_CurrencyCode'] = get_element_by_tag(each_price,'Shipping','CurrencyCode')
                    
                    
                    order_price_item['CompetitivePricing'].append(CompetitiveOffer)
            price_list.append(order_price_item)
        return   price_list
     
    def get_product_price(self,account_info,SellerSKU=(),ASIN=(),condition=None,excludeme="False"):
        '''
        得到商店产品价格信息
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @param SellerSKU: 需要查找价格的SKU列表,最大值：20 个 SellerSKU
        @param ASIN: 需要查找的ASIN列表,最大值：20 个 ASIN
        @param condition: 根据商品状况筛纳入考虑范围的商品。有效值：New、Used、Collectible、Refurbished、Club
        @return: 返回此商店的产品价格列表，
                            格式为： 
                            
            
        '''
        try:

            amazon = self.__create_api('Products',account_info)
            
            marketplaceids = CONFIG_MPI[account_info.region]
            product_price_return_list = []
            
            
            if SellerSKU is not None:
                sku_list_count = 1
                while True:
                    SellerSKU_temp = SellerSKU[(sku_list_count-1)*20:sku_list_count*20]
                    sku_list_count += 1
                    if len(SellerSKU_temp) == 0:
                        break
                    else:
                        my_price_list = amazon.get_lowest_offer_listings_for_sku(marketplaceids, skus=SellerSKU_temp,condition=condition,excludeme=excludeme)
                        my_price_list = my_price_list.response.content
                        my_price_list = parseString(my_price_list)
                        my_price_list = my_price_list.getElementsByTagName("GetLowestOfferListingsForSKUResult")
                        product_price_return_list.extend(self.__deal_product_price(my_price_list))
                        
            elif ASIN is not None:
                asin_count = 1
                while True:
                    ASIN_temp = ASIN[(asin_count-1)*20:asin_count*20]
                    asin_count += 1
                    if len(ASIN_temp) == 0:
                        break
                    else:
                        my_price_list = amazon.get_lowest_offer_listings_for_asin(marketplaceids, asins=ASIN_temp,condition=condition,excludeme=excludeme)
                        my_price_list = my_price_list.response.content
                        my_price_list = parseString(my_price_list)
                        my_price_list = my_price_list.getElementsByTagName("GetLowestOfferListingsForASINResult")
                        product_price_return_list.extend(self.__deal_product_price(my_price_list))
            else:
                {'result': False, 'error_message': "SellerSKU and ASIN is can't be empty."}
            
            return {'result':True,'data':product_price_return_list}
        except Exception, e:
            return {'result':False,'error_message':str(e)}
    
    def get_product_competitive_price(self,account_info,SellerSKU=(),ASIN=()):
        '''
        得到商店产品价格信息
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @param SellerSKU: 需要查找价格的SKU列表,最大值：20 个 SellerSKU
        @param ASIN: 需要查找的ASIN列表,最大值：20 个 ASIN
        @return: 返回此商店的buybox价格，
                            格式为： 
                            [
                                {
                    'ASIN': 'B003RZ2F08',
                    'SellerId': 'ARWTKM5K67VQV',
                    'SellerSKU': '0B-K5PK-4COJ',
                    'CompetitivePricing':[{
                            'subcondition': u'New', 'condition': u'New','belongsToRequester': 'false',
                            'CompetitivePriceId': '1', 
                            'Shipping_CurrencyCode': 'USD','Shipping': '0.00', 
                            'LandedPrice_Amount': '3.10', 'ListingPrice_CurrencyCode': 'USD', 
                            'LandedPrice_CurrencyCode': 'USD', 'ListingPrice': '3.10', 
                                                     }]
                                }
                            ]
            
        '''
        try:
            amazon = self.__create_api('Products',account_info)
            
            marketplaceids = CONFIG_MPI[account_info.region]
            product_price_return_list = []
            
            
            if SellerSKU:
                sku_list_count = 1
                while True:
                    SellerSKU_temp = SellerSKU[(sku_list_count-1)*20:sku_list_count*20]
                    sku_list_count += 1
                    if len(SellerSKU_temp) == 0:
                        break
                    else:
                        my_price_list = amazon.get_competitive_pricing_for_sku(marketplaceids, skus=SellerSKU_temp)
                        my_price_list = my_price_list.response.content
                        my_price_list = parseString(my_price_list)
                        my_price_list = my_price_list.getElementsByTagName("GetCompetitivePricingForSKUResult")
                        product_price_return_list.extend(self.__deal_product_competitive_price(my_price_list))
                        
            elif ASIN:
                asin_count = 1
                while True:
                    ASIN_temp = ASIN[(asin_count-1)*20:asin_count*20]
                    asin_count += 1
                    if len(ASIN_temp) == 0:
                        break
                    else:
                        my_price_list = amazon.get_competitive_pricing_for_asin(marketplaceids, asins=ASIN_temp)
                        my_price_list = my_price_list.response.content
                        my_price_list = parseString(my_price_list)
                        my_price_list = my_price_list.getElementsByTagName("GetCompetitivePricingForASINResult")
                        product_price_return_list.extend(self.__deal_product_competitive_price(my_price_list))
            else:
                {'result': False, 'error_message': "SellerSKU and ASIN is can't be empty."}
            
            return {'result':True,'data':product_price_return_list}
        except Exception, e:
            return {'result':False,'error_message':str(e)}

    def get_reprot_test(self,account_info):
        try:
            amazon = self.__create_api('Reports',account_info)
            orders = amazon.request_report('_GET_FLAT_FILE_PAYMENT_SETTLEMENT_DATA_',)
            data = orders.response.content
            next_dom = parseString(data)
            
            FeedSubmissionId = get_element_by_tag(next_dom,'ReportRequestId')
            print 'FeedSubmissionId:',FeedSubmissionId
            while True:
                print 'start'
                time.sleep(30)
                print 'sleep(30)'
                orders = amazon.get_report_request_list([FeedSubmissionId])
                data = orders.response.content
                print 'data:',data
                next_dom = parseString(data)
                print 'status:',get_element_by_tag(next_dom,'ReportProcessingStatus')
                if get_element_by_tag(next_dom,'ReportProcessingStatus') == '_DONE_':
                    break
        
            FeedSubmissionId = get_element_by_tag(next_dom,'GeneratedReportId')
            orders = amazon.get_report(FeedSubmissionId)
            
            f = open('abc.txt','w')
            data = orders.response.content
            print '-------------华丽的分割线------------'
            print 'data',data
            f.write(data)
            f.flush()
            f.close()
            print '-------------华丽的分割线------------'
        except Exception,e:
            print 'error:',str(e)
            
    def get_product_report(self,account_info):
        '''
        得到商店产品信息的api
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                        格式为： {
                    'data': [
                                {'SKU': '123456','title':'abc'}, {'SKU': '456789','title':'efg'}
                                                    ], 
                    'result': True
                                }
        '''
        try:
            amazon = self.__create_api('Reports',account_info)
            orders = amazon.request_report('_GET_MERCHANT_LISTINGS_DATA_',)
            data = orders.response.content

            
            next_dom = parseString(data)
            FeedSubmissionId = next_dom.getElementsByTagName("ReportRequestId")[0].childNodes[0].data
        
            while True:
                time.sleep(30)
                orders = amazon.get_report_request_list([FeedSubmissionId])
                data = orders.response.content
                next_dom = parseString(data)
                if next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data == '_DONE_':
                    break
        
            FeedSubmissionId = next_dom.getElementsByTagName("GeneratedReportId")[0].childNodes[0].data
            orders = amazon.get_report(FeedSubmissionId)
            
            data = orders.response.content
            
            product_list_return = []
            product_list = data.split('\n')
#             print '----------------'
#             print product_list
#             print '----------------'
#             return
            product_index = product_list[0].split('\t')
            index_length = len(product_index)
            start_index = 0
            
            for each_product in product_list[1:]:
                product_temp = {}
                product_info  = each_product.split('\t')
                if len(product_info) <= 1:
                    continue
                for i in range(0,index_length):
                    product_temp[product_index[i]] = product_info[i]
                product_list_return.append(product_temp)
            return {'result':True,'data':product_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
       
       
       
       
    def set_product_price(self,account_info,sku_price_list=()):
        '''
        得到商店产品信息的api
        @param ACCOUNT_ID: 商店标示
        @param sku_price_list: {sku1:{'price':price1,'currency':'USD','status':True},sku2:{'price':price2,'currency':'USD','status':True}}
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                            格式为： {
                        'data': {
                                    sku1:{'price':price1,'currency':'USD','status':True},
                                    sku1:{'price':price1,'currency':'USD','status':False,'ResultDescription':'Error description','ResultMessageCode':'00001'}
                                                     },
                         'result': True
                                         }
        '''
        try:
            amazon = self.__create_api('Feeds',account_info)
            MarketplaceID = CONFIG_MPI[account_info.region]
            messageId = 1
            my_feed = '''<?xml version="1.0" encoding="utf-8"?>
    <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
    <Header>
    <DocumentVersion>1.01</DocumentVersion>
    <MerchantIdentifier>%(Account_Id)s</MerchantIdentifier>
    </Header>
    <MessageType>Price</MessageType>'''
            
            my_feed = my_feed % { 'Account_Id': account_info.store_key }
            
            for each_sku in sku_price_list:
                SellerSku = each_sku
                SellPrice = sku_price_list[each_sku]['price']
                Currency = sku_price_list[each_sku]['currency']
                sku_price_list[each_sku]['status'] = True
                my_feed = my_feed + '''\n
    <Message>
        <MessageID>%(MessageID)s</MessageID>
        <OperationType>Update</OperationType>
        <Price>
        <SKU>%(MySku)s</SKU>
        <StandardPrice currency="%(currency)s">%(myprice)s</StandardPrice>
        </Price>
    </Message>'''
                my_feed = my_feed % {
                                     'MessageID':messageId,
                                      'MySku' : SellerSku,
                                      'myprice' : SellPrice,
                                      'currency':Currency
                                                        }
                messageId = messageId+1
            
            my_feed = my_feed + '''\n
</AmazonEnvelope>'''
#            print 'my_feed:',my_feed
            upload_result = amazon.submit_feed(my_feed, '_POST_PRODUCT_PRICING_DATA_')
            data = upload_result.response.content
            print '--------------data:--------------------'
            print 'data:',data
            next_dom = parseString(data)
            FeedSubmissionId = next_dom.getElementsByTagName("FeedSubmissionId")[0].childNodes[0].data
#            FeedSubmissionId = '10799861466'
            while True:
                time.sleep(5)
                orders = amazon.get_feed_submission_list(feedids=[FeedSubmissionId])
                data = orders.response.content
                print '--------------data:--------------------'
                print 'data:',data
                next_dom = parseString(data)
#                print '123'
                if next_dom.getElementsByTagName("FeedProcessingStatus")[0].childNodes[0].data == '_DONE_':
                    break
        
            sub_result_list = amazon.get_feed_submission_result(feedid = FeedSubmissionId)
            
            sub_result_list_xml = sub_result_list.response.content            
#            print 'data:',sub_result_list_xml
#            print '--------------------------------'
            sub_result_list_str = parseString(sub_result_list_xml)
            
#            print 'data:',sub_result_list_str
#            print '--------------------------------'
            
            
            MessagesProcessed = sub_result_list_str.getElementsByTagName("MessagesProcessed")[0].childNodes[0].data
            MessagesSuccessful = sub_result_list_str.getElementsByTagName("MessagesSuccessful")[0].childNodes[0].data
            
            if MessagesProcessed > MessagesSuccessful:
                for each in sub_result_list_str.getElementsByTagName("Result"):
                    sku_price_list[str(each.getElementsByTagName("MessageID")[0].childNodes[0].data)]['status'] = False
                    sku_price_list[str(each.getElementsByTagName("MessageID")[0].childNodes[0].data)]['ResultDescription'] = each.getElementsByTagName("ResultDescription")[0].childNodes[0].data
                    sku_price_list[str(each.getElementsByTagName("MessageID")[0].childNodes[0].data)]['ResultMessageCode'] = each.getElementsByTagName("ResultMessageCode")[0].childNodes[0].data
            
            return {'result':True,'data':sku_price_list}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
    
    def get_fba_product_inventory(self,account_info, sku_list=(),datetime = None ):
        '''
            得到网店的FBA商品的库存信息
        @param ACCOUMNT_ID: 商店标示
        @param regioin: 地区标示
        @param sku_list:需要查找的商品列表
        @param datetime: 商品库存信息发生变化的起始时间
        @return: 设置sku_list的话返回指定的列表
                              格式：{
                        'data': [
                                    {'ASIN': '', 'SellerSKU': 'B00475IIA8', 'FNSKU': '', 'InStockSupplyQuantity': '0', 'Condition': '', 'TotalSupplyQuantity': '0'},
                                                     ],
                         'result': True
                                         }
        '''

        amazon = self.__create_api('Inventory',account_info)
        fba_product_inventory_return_list = []
    
        floop_count = 1
        while True:
            sku_list_temp = sku_list[(floop_count-1)*50:floop_count*50]
            if len(sku_list_temp) == 0:
                break
            else:
                try:
                    orders = amazon.list_inventory_supply(skus=sku_list_temp,datetime=datetime)
                    next_data_2 = orders.response.content
                    next_dom_2 = parseString(next_data_2)
                    Inventory_list = next_dom_2.getElementsByTagName("member")
                    fba_product_inventory_return_list.extend(self.__get_inventory_list(Inventory_list))
                    floop_count = floop_count+1
                except Exception,e:
                    print 'error:',str(e)
            time.sleep(10)
        return {'result':True,'data':fba_product_inventory_return_list}
    
    
    
    
    def get_listing_report(self,account_info,repoprt_type,start_date= None,end_date=None):
        '''
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                        格式为： {
                    'data': [
                                 {'key1': 'value1', 'key2': 'value2', ...},
                                                    ], 
                    'result': True
                                }
        '''
        try:
            amazon = self.__create_api('Reports',account_info)
            orders = amazon.request_report(repoprt_type)
            data = orders.response.content
       
            next_dom = parseString(data)
            FeedSubmissionId = next_dom.getElementsByTagName("ReportRequestId")[0].childNodes[0].data

            while True:
                orders = amazon.get_report_request_list([FeedSubmissionId])
                data = orders.response.content
                next_dom = parseString(data)
                if next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data in ['_DONE_','_CANCELLED_','_DONE_NO_DATA_']:
                    break
                time.sleep(60)
                
            FeedSubmissionId = next_dom.getElementsByTagName("GeneratedReportId")[0].childNodes[0].data
            orders = amazon.get_report(FeedSubmissionId)
            
            data = orders.response.content
            
            product_list_return = []
            product_list = data.replace('\r','').split('\n')

            product_index = product_list[0].split('\t')
            index_length = len(product_index)
            start_index = 0
            
            for each_product in product_list[1:]:
                product_temp = {}
                product_info  = each_product.split('\t')
                if len(product_info) <= 1:
                    continue
                for i in range(0,index_length):
                    product_temp[product_index[i]] = product_info[i]
                product_list_return.append(product_temp)
            return {'result':True,'data':product_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
       

    
    

    def get_payment_report(self,account_info,start_date= None,end_date=None):
        '''
        得到商店产品信息的api
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                        格式为： {
                    'data': [
                                {'SKU': '123456','title':'abc'}, {'SKU': '456789','title':'efg'}
                                                    ], 
                    'result': True
                                }
        '''
        try:
            amazon = self.__create_api('Reports',account_info)
            orders = amazon.request_report('_GET_FLAT_FILE_ORDERS_DATA_',start_date,end_date)
            data = orders.response.content
        
            next_dom = parseString(data)
            print data
            FeedSubmissionId = next_dom.getElementsByTagName("ReportRequestId")[0].childNodes[0].data
            print FeedSubmissionId
#             return
#             FeedSubmissionId = '59897016421' 
            while True:

#                 print 'sleep 60s'
                orders = amazon.get_report_request_list([FeedSubmissionId])
                data = orders.response.content
                next_dom = parseString(data)
                print data
                print next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data
                if next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data == '_DONE_':
                    break
                time.sleep(60)
            FeedSubmissionId = next_dom.getElementsByTagName("GeneratedReportId")[0].childNodes[0].data
            orders = amazon.get_report(FeedSubmissionId)
            
            data = orders.response.content
            print 'success!!!!!'
            print data
            
            product_list_return = []
            product_list = data.split('\n')
#             print '----------------'
#             print product_list
#             print '----------------'
#             return
            product_index = product_list[0].split('\t')
            index_length = len(product_index)
            start_index = 0
            
            for each_product in product_list[1:]:
                product_temp = {}
                product_info  = each_product.split('\t')
                if len(product_info) <= 1:
                    continue
                for i in range(0,index_length):
                    product_temp[product_index[i]] = product_info[i]
                product_list_return.append(product_temp)
            return {'result':True,'data':product_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
       



    def get_fba_health_inventory_report(self,account_info):
        '''
        得到FBA 产品的产品库存销量信息，预计可销天数。
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                        格式为： {
                    'data': [
                                 {'inv-age-91-to-180-days': '77', 'weeks-of-cover-t180': '116.5', 'units-shipped-last-365-days': '17', 
                                 'inbound-recommend-quantity': '', 'lowest-afn-new-price': '12.24', 'lowest-afn-used-price': '0.00', 
                                 'asin-limit': '', 'inv-age-365-plus-days': '0', 'sellable-quantity': '77', 'inv-age-0-to-90-days': '0', 
                                 'currency': 'USD', 'qty-to-be-charged-long-term-storage-in-next-cleanup': '0', 'inv-age-181-to-270-days': '0',
                                  'per-unit-volume': '0.0', 'sku': 'Ash-B005MRAXZI', 'asin': 'B005MRAXZI', 'lowest-mfn-used-price': '0.00', 
                                  'lowest-mfn-new-price': '12.20    ', 'fnsku': 'X000KGFYNX', 'weeks-of-cover-t90': '82.5', 'sales-price': '12.24', 
                                  'sales-rank': '141361', 'units-shipped-last-90-days': '12', 'product-name': 'Dayan 5 ZhanChi 3x3x3 Speed Cube White DIY Kit', 
                                  'units-shipped-last-180-days': '17', 'is-hazmat': 'N', 'qty-in-long-term-storage-program': '0', 'inv-age-271-to-365-days': '0',
                                   'weeks-of-cover-t30': '330', 'snapshot-date': '2014-12-14T08:00:00+00:00', 'qty-with-removals-in-progress': '0', 
                                   'in-bound-quantity': '0', 'units-shipped-last-7-days': '1', 'your-price': '12.24', 'condition': 'New',
                                    'num-afn-used-sellers': '0', 'units-shipped-last-24-hrs': '0', 'unsellable-quantity': '0', 'weeks-of-cover-t365': '236.2',
                                     'units-shipped-last-30-days': '1', 'weeks-of-cover-t7': '77', 'projected-long-term-storage-fees': '0.00', 'total-quantity': '79',
                                      'num-afn-new-sellers': '2', 'product-group': 'toy_display_on_website'},
                                                    ], 
                    'result': True
                                }
        '''
        try:
            amazon = self.__create_api('Reports',account_info)
            orders = amazon.request_report('_GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA_')
            data = orders.response.content
       
            next_dom = parseString(data)
            FeedSubmissionId = next_dom.getElementsByTagName("ReportRequestId")[0].childNodes[0].data
            print FeedSubmissionId

            while True:
                orders = amazon.get_report_request_list([FeedSubmissionId])
                data = orders.response.content
                next_dom = parseString(data)
                print next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data
                if next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data in ['_DONE_','_CANCELLED_','_DONE_NO_DATA_']:
                    break
                time.sleep(60)
                
            FeedSubmissionId = next_dom.getElementsByTagName("GeneratedReportId")[0].childNodes[0].data
            orders = amazon.get_report(FeedSubmissionId)
            
            data = orders.response.content
            
            product_list_return = []
            product_list = data.replace('\r','').split('\n')

            product_index = product_list[0].split('\t')
            index_length = len(product_index)
            start_index = 0
            
            for each_product in product_list[1:]:
                product_temp = {}
                product_info  = each_product.split('\t')
                if len(product_info) <= 1:
                    continue
                for i in range(0,index_length):
                    if product_info[i] == '':
                        product_temp[product_index[i]] = '0'
                    elif product_info[i] == 'Infinite':
                        product_temp[product_index[i]] = '9999'
                    else:
                        product_temp[product_index[i]] = product_info[i]
                        
                product_list_return.append(product_temp)
            return {'result':True,'data':product_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
       



    def get_fba_listing_inventory_report(self,account_info):
        '''
        得到商店产品信息的api
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                        格式为： {
                    'data': [
                                {'sku': '0E-4AS0-OGYA', 'asin': 'B008ATNE8I', 'afn-fulfillable-quantity': '22', 'your-price': '61.99', 'fnsku': 'X000O6JOHB', 'afn-total-quantity': '23', 'afn-listing-exists': 'Yes', 'afn-warehouse-quantity': '23', 'mfn-listing-exists': 'No', 'afn-unsellable-quantity': '0', 'mfn-fulfillable-quantity': '', 'afn-inbound-shipped-quantity': '0', 'afn-reserved-quantity': '1', 'product-name': 'Pixel Vertical Battery Grip for Canon EOS 5D Mark III BG-E11', 'per-unit-volume': '0.1', 'afn-inbound-receiving-quantity': '0', 'condition': 'New', 'afn-inbound-working-quantity': '0'}
                                                    ], 
                    'result': True
                                }
        '''
        try:
            amazon = self.__create_api('Reports',account_info)
            orders = amazon.request_report('_GET_FBA_MYI_ALL_INVENTORY_DATA_')
            data = orders.response.content
     
            next_dom = parseString(data)
            FeedSubmissionId = next_dom.getElementsByTagName("ReportRequestId")[0].childNodes[0].data
            while True:
                orders = amazon.get_report_request_list([FeedSubmissionId])
                data = orders.response.content
                next_dom = parseString(data)
                if '_DONE_' in next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data:
                    break
                time.sleep(60)
            FeedSubmissionId = next_dom.getElementsByTagName("GeneratedReportId")[0].childNodes[0].data
            orders = amazon.get_report(FeedSubmissionId)
            
            data = orders.response.content

            
            product_list_return = []
            product_list = data.split('\n')

            product_index = product_list[0].split('\t')
            index_length = len(product_index)
            start_index = 0
            
            for each_product in product_list[1:]:
                product_temp = {}
                product_info  = each_product.split('\t')
                if len(product_info) <= 1:
                    continue
                for i in range(0,index_length):
                    product_temp[product_index[i]] = product_info[i]
                product_list_return.append(product_temp)
            return {'result':True,'data':product_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
       


    def get_payment_settlement_reports(self,account_info):
        try:
            amazon = self.__create_api('Reports',account_info)
            settlements = amazon.get_report_request_list(types = ['_GET_ALT_FLAT_FILE_PAYMENT_SETTLEMENT_DATA_'])
            data = settlements.response.content
            next_dom = parseString(data)
            
            report_list_return = []
            report_lists = next_dom.getElementsByTagName("ReportRequestInfo")
            for each in report_lists:
                r = {
                     'request_id':each.getElementsByTagName("ReportRequestId")[0].childNodes[0].data,
                     'start_date':each.getElementsByTagName("StartDate")[0].childNodes[0].data,
                     'end_date':each.getElementsByTagName("EndDate")[0].childNodes[0].data,
                     'generated_id':each.getElementsByTagName("GeneratedReportId")[0].childNodes[0].data
                     }
                report_list_return.append(r)
            return {'result':True,'data':report_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
            
    def get_payment_settlement_detail(self,account_info,report_id):
        try:
            amazon = self.__create_api('Reports',account_info)
            settlements = amazon.get_report(report_id)
            data = settlements.response.content
   
            settlement_list_return = []
            settlement_list = data.split('\n')

            settlement_index = settlement_list[0].split('\t')
            index_length = len(settlement_index)
            start_index = 0
            
            for each_settlement in settlement_list[1:]:
                settlement_temp = {}
                settlement_info  = each_settlement.split('\t')
                if len(settlement_info) <= 1:
                    continue
                for i in range(0,index_length):
                    settlement_temp[settlement_index[i]] = settlement_info[i]
                settlement_list_return.append(settlement_temp)
                
            return {'result':True,'data':settlement_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
            



    def get_fba_inventory_receipts_data_report(self,account_info,start_date= None,end_date=None):
        '''
        得到商店产品信息的api
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                        格式为： {
                    'data': [
                                 {'sku': 'NJ-15MP-OPVH', 'fnsku': 'X000P1X3G3', 'received-date': '2014-12-09T08:00:00+00:00', 'fulfillment-center-id': 'AVP1', 'product-name': 'ThinkMax\xae 4 In 1 X4 Battery Charger for Hubsan', 'fba-shipment-id': 'FBA28XS7QB', 'quantity': '200'},
                                                    ], 
                    'result': True
                                }
        '''
        try:
            amazon = self.__create_api('Reports',account_info)
            inventories = amazon.request_report('_GET_FBA_FULFILLMENT_INVENTORY_RECEIPTS_DATA_',start_date,end_date)
            data = inventories.response.content
            next_dom = parseString(data)
            FeedSubmissionId = next_dom.getElementsByTagName("ReportRequestId")[0].childNodes[0].data
            while True:
                inventories = amazon.get_report_request_list([FeedSubmissionId])
                data = inventories.response.content
                next_dom = parseString(data)
                if '_DONE_' in next_dom.getElementsByTagName("ReportProcessingStatus")[0].childNodes[0].data:
                    break
                time.sleep(2 * 60)
            FeedSubmissionId = next_dom.getElementsByTagName("GeneratedReportId")[0].childNodes[0].data
            product_inventories = amazon.get_report(FeedSubmissionId)
            
            data = product_inventories.response.content
            
            product_list_return = []
            product_list = data.split('\n')

            product_index = product_list[0].split('\t')
            index_length = len(product_index)
            start_index = 0
            
            for each_product in product_list[1:]:
                product_temp = {}
                product_info  = each_product.split('\t')
                if len(product_info) <= 1:
                    continue
                for i in range(0,index_length):
                    product_temp[product_index[i]] = product_info[i]
                product_list_return.append(product_temp)
            return {'result':True,'data':product_list_return}
        except Exception,e:
            return {'result':False,'error_message':str(e)}
       
       
    def get_shipment_data(self,ShipmentData):
        shipment_list = []
        try:
            for each_shipment in ShipmentData:
                r = {
                     'PostalCode' : each_shipment.getElementsByTagName("PostalCode")[0].childNodes[0].data,
                     'Name' : each_shipment.getElementsByTagName("Name")[0].childNodes[0].data,
                     'CountryCode' : each_shipment.getElementsByTagName("CountryCode")[0].childNodes[0].data,
                     'StateOrProvinceCode' : each_shipment.getElementsByTagName("StateOrProvinceCode")[0].childNodes[0].data,
                     'AddressLine2' : '',#each_shipment.getElementsByTagName("AddressLine2")[0].childNodes[0].data,                     
                     'AddressLine1' : each_shipment.getElementsByTagName("AddressLine1")[0].childNodes[0].data,
                     'City' : each_shipment.getElementsByTagName("City")[0].childNodes[0].data,
                     'AreCasesRequired' : each_shipment.getElementsByTagName("AreCasesRequired")[0].childNodes[0].data,
                     'ShipmentName' : each_shipment.getElementsByTagName("ShipmentName")[0].childNodes[0].data,
                     'ShipmentStatus' : each_shipment.getElementsByTagName("ShipmentStatus")[0].childNodes[0].data,
                     'ShipmentId' : each_shipment.getElementsByTagName("ShipmentId")[0].childNodes[0].data,
                     'LabelPrepType' : each_shipment.getElementsByTagName("LabelPrepType")[0].childNodes[0].data,
                     'DestinationFulfillmentCenterId' : each_shipment.getElementsByTagName("DestinationFulfillmentCenterId")[0].childNodes[0].data,
                     }
                shipment_list.append(r)
        except Exception,e:
            print 'get_shipment_data ',e
        return shipment_list


    def get_fba_inbound_data(self,account_info,start_date= None,end_date=None):
        '''
        得到商店产品信息的api
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                        格式为： {
                    'data': [
                                 {'sku': 'NJ-15MP-OPVH', 'fnsku': 'X000P1X3G3', 'received-date': '2014-12-09T08:00:00+00:00', 'fulfillment-center-id': 'AVP1', 'product-name': 'ThinkMax\xae 4 In 1 X4 Battery Charger for Hubsan', 'fba-shipment-id': 'FBA28XS7QB', 'quantity': '200'},
                                                    ], 
                    'result': True
                                }
        '''
        try:
            amazon = self.__create_api('Inbounds',account_info)
            shipments = amazon.list_inbound_shipments(start_date,end_date)
            data = shipments.response.content
            print data
            next_dom = parseString(data)
            
            ShipmentData = next_dom.getElementsByTagName("member")
            
            shipment_list = self.get_shipment_data(ShipmentData)
            next_token_tag = next_dom.getElementsByTagName("NextToken")
            
            while next_token_tag:
                
                next_token = next_dom.getElementsByTagName("NextToken")[0].childNodes[0].data
                shipments = amazon.list_inbound_shipments_by_nexttoken(next_token)
                data = shipments.response.content
                next_dom = parseString(data)
    
                ShipmentData = next_dom.getElementsByTagName("member")
                shipment_list.extend(self.get_shipment_data(ShipmentData))
                next_token_tag = next_dom.getElementsByTagName("NextToken")
                
            return {'result':True,'data':shipment_list}
        except Exception,e:
            raise
            return {'result':False,'error_message':str(e)}
       

 
    def get_shipment_items_data(self,ShipmentData):
        shipment_list = []
        try:
            for each_shipment in ShipmentData:
                r = {
                     'SellerSKU' : each_shipment.getElementsByTagName("SellerSKU")[0].childNodes[0].data,
                     'QuantityShipped' : each_shipment.getElementsByTagName("QuantityShipped")[0].childNodes[0].data,
                     'QuantityInCase' : each_shipment.getElementsByTagName("QuantityInCase")[0].childNodes[0].data,
                     'QuantityReceived' : each_shipment.getElementsByTagName("QuantityReceived")[0].childNodes[0].data,
                     'FulfillmentNetworkSKU' : each_shipment.getElementsByTagName("FulfillmentNetworkSKU")[0].childNodes[0].data,
                     }
                shipment_list.append(r)
        except Exception,e:
            print 'get_shipment_items_data ',e
        return shipment_list




    def get_fba_inbound_shipment_items(self,account_info,shipment_id):
        '''
        得到商店产品信息的api
        @param ACCOUNT_ID: 商店标示
        @param region:地区标示
        @return: 返回此商店的产品信息列表，
                        格式为： {
                    'data': [
                                 {'sku': 'NJ-15MP-OPVH', 'fnsku': 'X000P1X3G3', 'received-date': '2014-12-09T08:00:00+00:00', 'fulfillment-center-id': 'AVP1', 'product-name': 'ThinkMax\xae 4 In 1 X4 Battery Charger for Hubsan', 'fba-shipment-id': 'FBA28XS7QB', 'quantity': '200'},
                                                    ], 
                    'result': True
                                }
        '''
        try:
            amazon = self.__create_api('Inbounds',account_info)
            inventories = amazon.list_inbound_shipment_items(shipment_id)
            data = inventories.response.content
            next_dom = parseString(data)
            
            ShipmentData = next_dom.getElementsByTagName("member")
            shipment_list = self.get_shipment_items_data(ShipmentData)
            next_token_tag = next_dom.getElementsByTagName("NextToken")
            
            while next_token_tag:
                
                next_token = next_dom.getElementsByTagName("NextToken")[0].childNodes[0].data
                shipments = amazon.list_inbound_shipment_items_by_nexttoken(next_token)
                data = shipments.response.content
                next_dom = parseString(data)
    
                ShipmentData = next_dom.getElementsByTagName("member")
                shipment_list.extend(self.get_shipment_items_data(ShipmentData))
                next_token_tag = next_dom.getElementsByTagName("NextToken")
                            
                       
            return {'result':True,'data':shipment_list}
        except Exception,e:
            raise
            return {'result':False,'error_message':str(e)}
       
       
       
    def create_destination(self,account_info):
        amazon = self.__create_api('Subscriptions',account_info)
        destination = amazon.registerDestination('ATVPDKIKX0DER')
        data = destination.response.content
        print data
        return data
    
       
    def test_notification_to_destination(self,account_info):
        amazon = self.__create_api('Subscriptions',account_info)
        destination = amazon.testNotificationToDestination('ATVPDKIKX0DER')
        data = destination.response.content
        print data
        return data
    
    def get_list_registered_destinations(self,account_info):
        amazon = self.__create_api('Subscriptions',account_info)
        destination = amazon.getListRegisteredDestinations('ATVPDKIKX0DER')
        data = destination.response.content
        print data
        return data    
    
    
           