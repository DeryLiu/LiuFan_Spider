# -*- coding: utf-8 -*-
#!/usr/bin/env python

import pytz
import random
import HTMLParser
from datetime import datetime, timedelta
from xml.dom.minidom import  parseString

from ProApiandERPGateway.utils import get_element_by_tag
from ProApiandERPGateway.ebay_api.ebayorder.eBay import Get_orders


# class eBay_api():
#    Developer = "ed67f460-65c9-460d-bcf0-f0ffa3bb6207"
#    Application = "StarMerx-060d-418e-9358-8252bbe9b89b"
#    Certificate = "a69abcc2-989e-4560-a339-9329bd291ffe"
#    Runname = 'StarMerx-StarMerx-060d-4-sfjlzrkd'
#    def __init__(self):
#        self.Developer = "ed67f460-65c9-460d-bcf0-f0ffa3bb6207"
#        self.Application = "StarMerx-060d-418e-9358-8252bbe9b89b"
#        self.Certificate = "a69abcc2-989e-4560-a339-9329bd291ffe"
#        self.Runname = 'StarMerx-StarMerx-060d-4-sfjlzrkd'
#        
#        return eBay_Call(Developer,Application,Certificate,Runname)
#    

def get_order_line_list(order_items):
    html_parser = HTMLParser.HTMLParser()
    order_line_list = []
    for each_item in order_items:
        order_line_item = {}
        order_line_item['QuantityOrdered'] = get_element_by_tag(each_item, 'QuantityOrdered')
        order_line_item['Title'] = get_element_by_tag(each_item, 'Title')
        order_line_item['OrderItemId'] = get_element_by_tag(each_item, 'OrderItemId')
        order_line_item['CurrencyCode'] = get_element_by_tag(each_item, 'CurrencyCode')
        order_line_item['ItemPrice'] = get_element_by_tag(each_item, 'ItemPrice', 'Amount')
        order_line_item['ItemTax'] = get_element_by_tag(each_item, 'ItemTax', 'Amount')
        order_line_item['OrderItemId'] = get_element_by_tag(each_item, 'OrderItemId')        
        order_line_item['ShippingPrice'] = get_element_by_tag(each_item, 'ShippingPrice', 'Amount')
        order_line_item['ASIN'] = html_parser.unescape(html_parser.unescape(get_element_by_tag(each_item, 'ASIN')))
        order_line_item['SellerSKU'] = html_parser.unescape(html_parser.unescape(get_element_by_tag(each_item, 'SellerSKU')))
#        order_line_item['image_url'] = get_amazon_img_url(product_amazon,MKPLACEID,IdType,[ASIN])
        order_line_list.append(order_line_item)
    return   order_line_list

def deal_ebay_data(data, Token):
    return_order_list = []
    orders = data.getElementsByTagName("Order")
    for item in orders:
        return_order = {}
        return_order['orderID'] = get_element_by_tag(item, 'OrderID')
#        print 'order_id',return_order['orderID']
#        if return_order['orderID'] !='321436733735-1325211565011':
#            continue
        return_order['order_Status'] = get_element_by_tag(item, 'OrderStatus')
        return_order['Total_paid'] = get_element_by_tag(item, 'Total')
        return_order['SellerEmail'] = get_element_by_tag(item, 'SellerEmail')
        return_order['PaymentTime'] = get_element_by_tag(item, 'PaymentTime')
        return_order['PaymentMethod'] = get_element_by_tag(item, 'PaymentMethod')
        return_order['ExternalTransactionID'] = get_element_by_tag(item, 'ExternalTransactionID')
        return_order['ShippingService'] = get_element_by_tag(item, 'ShippingServiceSelected', 'ShippingService')
        return_order['ShippingServiceCost'] = get_element_by_tag(item, 'ShippingServiceSelected', 'ShippingServiceCost')
        return_order['Name'] = get_element_by_tag(item, 'ShippingAddress', 'Name')
        return_order['Street2'] = get_element_by_tag(item, 'ShippingAddress', 'Street2')
        return_order['Street1'] = get_element_by_tag(item, 'ShippingAddress', 'Street1')
        return_order['CityName'] = get_element_by_tag(item, 'ShippingAddress', 'CityName')
        return_order['StateOrProvince'] = get_element_by_tag(item, 'ShippingAddress', 'StateOrProvince')
        return_order['Country'] = get_element_by_tag(item, 'ShippingAddress', 'Country')
        return_order['CountryName'] = get_element_by_tag(item, 'ShippingAddress', 'CountryName')
        return_order['Phone'] = get_element_by_tag(item, 'ShippingAddress', 'Phone')
        return_order['PostalCode'] = get_element_by_tag(item, 'ShippingAddress', 'PostalCode')
        return_order['ShippedTime'] = get_element_by_tag(item, 'ShippedTime')
        return_order['IsMultiLegShipping'] = get_element_by_tag(item, 'IsMultiLegShipping')
        
        print 'aaa:', return_order['IsMultiLegShipping']
        if return_order['IsMultiLegShipping'] == 'true':
            IsMultiLegShipping_detail = {}
            MultiLegShippingDetails = item.getElementsByTagName("MultiLegShippingDetails")[0]
            IsMultiLegShipping_detail['MultiLegShippingDetails_Name'] = get_element_by_tag(MultiLegShippingDetails, 'ShipToAddress', 'Name')
            IsMultiLegShipping_detail['MultiLegShippingDetails_Street1'] = get_element_by_tag(MultiLegShippingDetails, 'ShipToAddress', 'Street1')
            IsMultiLegShipping_detail['MultiLegShippingDetails_CityName'] = get_element_by_tag(MultiLegShippingDetails, 'ShipToAddress', 'CityName')
            IsMultiLegShipping_detail['MultiLegShippingDetails_StateOrProvince'] = get_element_by_tag(MultiLegShippingDetails, 'ShipToAddress', 'StateOrProvince')
            IsMultiLegShipping_detail['MultiLegShippingDetails_Country'] = get_element_by_tag(MultiLegShippingDetails, 'ShipToAddress', 'Country')
            IsMultiLegShipping_detail['MultiLegShippingDetails_CountryName'] = get_element_by_tag(MultiLegShippingDetails, 'ShipToAddress', 'CountryName')
            IsMultiLegShipping_detail['MultiLegShippingDetails_PostalCode'] = get_element_by_tag(MultiLegShippingDetails, 'ShipToAddress', 'PostalCode')
            IsMultiLegShipping_detail['MultiLegShippingDetails_ReferenceID'] = get_element_by_tag(MultiLegShippingDetails, 'ShipToAddress', 'ReferenceID')
            IsMultiLegShipping_detail['MultiLegShippingDetails_ExternalAddressID'] = get_element_by_tag(MultiLegShippingDetails, 'ShipToAddress', 'ExternalAddressID')
            IsMultiLegShipping_detail['MultiLegShippingDetails_Phone'] = get_element_by_tag(MultiLegShippingDetails, 'ShipToAddress', 'Phone')
            IsMultiLegShipping_detail['MultiLegShippingDetails_Street2'] = get_element_by_tag(MultiLegShippingDetails, 'ShipToAddress', 'Street2')            
            IsMultiLegShipping_detail['MultiLegShippingDetails_ShippingService'] = get_element_by_tag(MultiLegShippingDetails, 'ShippingServiceDetails', 'ShippingService')
            IsMultiLegShipping_detail['MultiLegShippingDetails_TotalShippingCost'] = get_element_by_tag(MultiLegShippingDetails, 'ShippingServiceDetails', 'TotalShippingCost')
            return_order['IsMultiLegShipping_detail'] = IsMultiLegShipping_detail
            
        return_order['Transactions'] = []
        Transactions = item.getElementsByTagName("Transaction")
        
        transactioin_return = []                   
        for transactioin in Transactions:
            transactioin_list = {}
            transactioin_list['BuyerEmail'] = get_element_by_tag(transactioin, 'Buyer', 'Email')
            transactioin_list['BuyerStaticAlias'] = get_element_by_tag(transactioin, 'Buyer', 'StaticAlias')
            transactioin_list['ShippingCarrierUsed'] = get_element_by_tag(transactioin, 'ShipmentTrackingDetails', 'ShippingCarrierUsed')
            transactioin_list['ShipmentTrackingNumber'] = get_element_by_tag(transactioin, 'ShipmentTrackingDetails', 'ShipmentTrackingNumber')
            transactioin_list['CreatedDate'] = get_element_by_tag(transactioin, 'CreatedDate')
            transactioin_list['ItemID'] = get_element_by_tag(transactioin, 'Item', 'ItemID')
            transactioin_list['Title'] = get_element_by_tag(transactioin, 'Item', 'Title')
            transactioin_list['SKU'] = get_element_by_tag(transactioin, 'Item', 'SKU')
            transactioin_list['ConditionID'] = get_element_by_tag(transactioin, 'Item', 'ConditionID')
            transactioin_list['ConditionDisplayName'] = get_element_by_tag(transactioin, 'Item', 'ConditionDisplayName')
            transactioin_list['Site'] = get_element_by_tag(transactioin, 'Item', 'Site')
            transactioin_list['QuantityPurchased'] = get_element_by_tag(transactioin, 'QuantityPurchased')
            transactioin_list['TransactionID'] = get_element_by_tag(transactioin, 'TransactionID')
            transactioin_list['TransactionPrice'] = get_element_by_tag(transactioin, 'TransactionPrice')
            transactioin_list['OrderLineItemID'] = get_element_by_tag(transactioin, 'OrderLineItemID')
            transactioin_return.append(transactioin_list)
        return_order['Transactions'] = transactioin_return
        return_order_list.append(return_order)
    return return_order_list

def list_orders(Token, from_time=None, to_time=None):
    '''
        得到网店的订单信息
    @param ACCOUMNT_ID: 商店标示
    @param create_after,created_before: 订单的创建起始时间
    @param max_results: 每页的最大订单数量
    @return: 返回指定条件的订单列表，
                        格式为：{'data': [{'orderID': '106-8576586-2696225',}, {'orderID': '108-8969984-4010611',}], 'result': True}
    '''
    try:
        order_list_return = []
        current_number = 1
        Ack_time = 1
        while(True):
            Ack_time = Ack_time + 1
            my_dom = Get_orders(str(from_time), str(to_time), Token, current_number, 100)
            print 'dom', my_dom
            my_dom = parseString(my_dom)
            print 'dom', my_dom
            if get_element_by_tag(my_dom, "Ack") != 'Failure' :
                break
            if Ack_time > 10:
                break
        order_list_return.extend(deal_ebay_data(my_dom, Token))
#        return {'result':True,'data':order_list_return}
        current_number = current_number + 1
        
        totalPages = int(get_element_by_tag(my_dom, "TotalNumberOfPages"))
        
        while current_number <= totalPages:
            Ack_time = 1
            while(True):
                Ack_time = Ack_time + 1
                my_dom = Get_orders(str(from_time), str(to_time), Token, current_number)
                if my_dom.getElementsByTagName('Ack')[0].childNodes[0].data != 'Failure':
                    break
                if Ack_time > 10:
                    break

            order_list_return.extend(deal_ebay_data(my_dom, Token))
            current_number = current_number + 1
                            
        return {'result':True, 'data':order_list_return}
    except Exception, e:
        return {'result':False, 'error_message':str(e)}

if __name__ == "__main__":
    to_time = str(datetime.now(pytz.UTC) - timedelta(seconds=120)).split('.')[0].replace(' ', 'T') + 'Z'
    from_time = str(datetime.now(pytz.UTC) - timedelta(hours=8)).split('.')[0].replace(' ', 'T') + 'Z'
    print list_orders('A39O62K356TWEB', lastupdatedafter=from_time, lastupdatedbefore=to_time)
