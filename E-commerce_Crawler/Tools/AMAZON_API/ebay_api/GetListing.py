# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pytz
import random
import HTMLParser
from datetime import datetime, timedelta
from xml.dom.minidom import  parseString

from ProApiandERPGateway.utils import get_element_by_tag
from ProApiandERPGateway.ebay_api.ebayorder.eBay import Get_listing_products
from django.utils.encoding import smart_str, smart_unicode

def deal_ebay_product_data(data, Token):
    return_product_list = []
    products = data.getElementsByTagName("Item")
    for item in products:
        return_product = {}
        return_product['ItemID'] = smart_str(get_element_by_tag(item, 'ItemID'))
        return_product['Location'] = smart_str(get_element_by_tag(item, 'Location'))
        return_product['EndTime'] = smart_str(get_element_by_tag(item, 'ListingDetails','EndTime'))
        return_product['ListingDuration'] = smart_str(get_element_by_tag(item, 'ListingDuration'))
        return_product['Quantity'] = smart_str(get_element_by_tag(item, 'Quantity'))
        return_product['CurrentPrice'] = smart_str(get_element_by_tag(item, 'SellingStatus','CurrentPrice'))
        return_product['ListingStatus'] = smart_str(get_element_by_tag(item, 'SellingStatus','ListingStatus'))
        return_product['QuantitySold'] = smart_str(get_element_by_tag(item, 'SellingStatus','QuantitySold'))
        return_product['Title'] = smart_str(get_element_by_tag(item, 'Title'))
        return_product['SKU'] = smart_str(get_element_by_tag(item, 'SKU'))
        return_product['GalleryURL'] = smart_str(get_element_by_tag(item, 'PictureDetails','GalleryURL'))

        return_product_list.append(return_product)
    return return_product_list
    
def store_listing_product(Token,from_time=None, to_time=None):
    '''
        得到网店的在线产品信息
    @param Token: 商店标示
    @param create_after,created_before: 订单的创建起始时间
    @param max_results: 每页的最大订单数量
    @return: 返回指定条件的产品列表，
                        格式为：{'data': [{'orderID': '106-8576586-2696225',}, {'orderID': '108-8969984-4010611',}], 'result': True}
    '''
    
    try:
        product_list_return = []
        current_number = 1
        Ack_time = 1
        while(True):
            try:
                Ack_time = Ack_time + 1
                my_dom = Get_listing_products(str(from_time), str(to_time), Token, current_number, 200)
                my_dom = parseString(my_dom)
                if get_element_by_tag(my_dom, "Ack") != 'Failure' :
                    break
                if Ack_time > 10:
                    break
            except Exception,e:
                print e
            
        product_list_return.extend(deal_ebay_product_data(my_dom, Token))
        current_number = current_number + 1
        try:
            totalPages = int(get_element_by_tag(my_dom, "TotalNumberOfPages"))
        except:
            totalPages = 1
        print 'product_list_return  ',len(product_list_return)
        while current_number <= totalPages:
            Ack_time = 1
            while(True):
                try:
                    Ack_time = Ack_time + 1
                    my_dom = Get_listing_products(str(from_time), str(to_time), Token, current_number,200)
                    my_dom = parseString(my_dom)
                    if my_dom.getElementsByTagName('Ack')[0].childNodes[0].data != 'Failure':
                        break
                    if Ack_time > 10:
                        break
                except Exception,e:
                    print e
    
            product_list_return.extend(deal_ebay_product_data(my_dom, Token))
            current_number = current_number + 1
            print 'product_list_return  ',len(product_list_return)
                            
        return {'result':True, 'data':product_list_return}
    except Exception, e:
        return {'result':False, 'error_message':str(e)}
     
    
    
    

if __name__ == "__main__":
    to_time = str(datetime.now(pytz.UTC) + timedelta(days=60)).split('.')[0].replace(' ', 'T') + 'Z'
    from_time = str(datetime.now(pytz.UTC) ).split('.')[0].replace(' ', 'T') + 'Z'
    token = "AgAAAA**AQAAAA**aAAAAA**g8NBVA**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6AGkICmDpiBpw6dj6x9nY+seQ**CZ4BAA**AAMAAA**wuGuFAuvHlJzDX10nKheYWGDe2hiRUWavkpCDss027L+zusWUgyhX9M6jqrShQiqK3wA1wGIeE7E1v+bXieDFGV5Lo630rhHByDaK9Zq5BeeAkvqADAU3SuB9jvjiECgdMN0qGFeEteet6Qbx2gtQGRKXPn3mU0kpIsVNAY/ZVfk3VykQBnKV3SP7uBKiJbdXaKLzD1J6xZ5eBIYCA+TpcNuSuHLJhLCs5VLSUrvGqoqU3+djEWDz3HcuGZcKE2oSl9xp4l7PTLkxmUo/BdiKbd2B5V1T/eV2akO+UWS+2DpBuhdZ0pgeplVixUXB3aCZpe7dlgk1C0Ibej+FBjO+1/sumE6FLD1f59XMjmDlYAdnyDkMwYbKlXiZhaeWVg1mpQHuBSNf2wu5E2/7auGZ5ulcSdyebv7VdTL0VtwglG2t+HFCBAg7tekGSG9qmrXHbeAa50UFHR1y9Vjz9WsAtFiENOOJzpA2DtJlYVNVCMNU+fY1WNv2SH3xOvkHLYAA0p9FRVY3Ky8WC8pvBNSX4jzwx5crX6EZFHhAGgYsQ6z48zcpPRxXz03vM+Tn7GfkbBQoKZbykVb4O+CvgjfYvLywxErQzLbBmb3e2eOU6XsOxYiyK8K2VnkN/PH6FxVDVxG+1wRHpXFgA48ejru86k4cKFBjJdaGH1D3Tsh3k7BcnND44YcTNSAHgfxJGaHvxdhnj7fMEUycykDdZ1cUFYK/QCQ3UcYyzj1n7vXdbWUe4xrCAo0peigNfjSc0lc"
    print store_listing_product(token, from_time, to_time)
