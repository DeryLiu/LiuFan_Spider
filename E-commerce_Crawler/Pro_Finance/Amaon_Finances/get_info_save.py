from Tools import ALL_CONFIG
import os


def get_data_to_save_db(fee_group_data,account_id):
    setted_date = '2016-12-15 00:00:00'

    try:
        fee_data_all = fee_group_data['ListFinancialEventsResponse']['ListFinancialEventsResult']['FinancialEvents']
    except:
        fee_data_all = fee_group_data['ListFinancialEventsByNextTokenResponse']['ListFinancialEventsByNextTokenResult']['FinancialEvents']
    try:
        # db_time = str(fee_data_all['ShipmentEventList']['ShipmentEvent'][0]['PostedDate']).split('T')[0]
        db_time = str(fee_data_all['ShipmentEventList']['ShipmentEvent'][0]['PostedDate']).replace('T',' ').replace('Z','')
    except:
        db_time = ''
    fee_list = [] # 20161208
    # FBA Inventory Fee 和 Service Fee
    try:
        fbaTransOrService = fee_data_all['ServiceFeeEventList']['ServiceFeeEvent']

        if isinstance(fbaTransOrService,list):
            for fos in fbaTransOrService:
                forS_type = fos['FeeList']['FeeComponent']
                if forS_type['FeeType'] == 'FBAInboundTransportationFee':
                    # fee_f_date = str(fee_data_all['ShipmentEventList']['ShipmentEvent']['PostedDate']).split('T')[0]
                    fee_f_other = forS_type['FeeAmount']['CurrencyAmount']
                    fee_f_total = forS_type['FeeAmount']['CurrencyAmount']
                    fee_fba1_dict = {'datetime':setted_date, 'settlement': '',
                                      'type': 'FBA Inventory Fee','account_id':str(account_id),'orderID': '','sku': '', 'description': '', 'quantity': '',
                                      'marketplace': '','fulfillment':'Amazon',
                                      'productSales': 0.0,'shippingCredits': 0.0, 'giftWrapCredits': 0.0,'promotionalRebates': 0.0,
                                      'salesTaxCollected': 0.0,'sellingFees': 0.0, 'fbaFees': 0.0,'otherTransactionFees': 0.0,
                                      'other': fee_f_other, 'total':fee_f_total, 'acount': ''
                                      }
                    fee_list.append(fee_fba1_dict)
                    # print 'FBAInboundTransportationFee'
                if forS_type['FeeType'] == 'Subscription':
                    # print '==============================================='
                    # fee_s_date = str(fee_data_all['ShipmentEventList']['ShipmentEvent']['PostedDate']).split('T')[0]
                    fee_s_other = forS_type['FeeAmount']['CurrencyAmount']
                    fee_s_total = forS_type['FeeAmount']['CurrencyAmount']
                    fee_fba2_dict = {'datetime': setted_date,'settlement': '','type':'Service Fee', 'account_id':str(account_id),'orderID': '', 'sku': '', 'description': '',
                        'quantity': '','marketplace': '','fulfillment':'Amazon',
                        'productSales': 0.0, 'shippingCredits': 0.0, 'giftWrapCredits': 0.0, 'promotionalRebates': 0.0,
                        'salesTaxCollected': 0.0, 'sellingFees': 0.0, 'fbaFees': 0.0, 'otherTransactionFees': 0.0,
                        'other': fee_s_other,
                        'total': fee_s_total, 'acount': ''
                        }
                    # print fee_fba2_dict
                    fee_list.append(fee_fba2_dict)
                    # print 'Subscription'
        else:
            fbaTransOrService = fee_data_all['ServiceFeeEventList']['ServiceFeeEvent']['FeeList']['FeeComponent']
            if fbaTransOrService['FeeType'] == 'FBAInboundTransportationFee':
                # fee_s_date = str(fee_data_all['ShipmentEventList']['ShipmentEvent']['PostedDate']).split('T')[0]
                fee_s_other = fbaTransOrService['FeeAmount']['CurrencyAmount']
                fee_s_total = fbaTransOrService['FeeAmount']['CurrencyAmount']
                fee_ser1_dict = {'datetime': setted_date,'settlement': '', 'type': 'FBA Inventory Fee','account_id':str(account_id), 'orderID': '', 'sku': '',
                    'description': '', 'quantity': '','marketplace': '', 'fulfillment':'Amazon','productSales': 0.0, 'shippingCredits': 0.0, 'giftWrapCredits': 0.0,
                    'promotionalRebates': 0.0,'salesTaxCollected': 0.0, 'sellingFees': 0.0, 'fbaFees': 0.0,
                    'otherTransactionFees': 0.0,'other': fee_s_other,'total': fee_s_total, 'acount': ''
                    }
                fee_list.append(fee_ser1_dict)
                # print 'FBAInboundTransportationFee'
            if fbaTransOrService['FeeType'] == 'Subscription':
                # print '==============================================='
                # fee_f_date = str(fee_data_all['ShipmentEventList']['ShipmentEvent']['PostedDate']).split('T')[0]
                fee_f_other = fbaTransOrService['FeeAmount']['CurrencyAmount']
                fee_f_total = fbaTransOrService['FeeAmount']['CurrencyAmount']
                fee_ser2_dict = {'datetime': setted_date,'settlement': '','type':'Service Fee','account_id':str(account_id), 'orderID': '', 'sku': '',
                    'description': '','quantity': '','marketplace': '','fulfillment':'Amazon','productSales': 0.0, 'shippingCredits': 0.0, 'giftWrapCredits': 0.0,
                    'promotionalRebates': 0.0,'salesTaxCollected': 0.0, 'sellingFees': 0.0, 'fbaFees': 0.0,
                    'otherTransactionFees': 0.0,'other': fee_f_other,'total': fee_f_total, 'acount': ''
                    }
                # print fee_ser2_dict
                fee_list.append(fee_ser2_dict)
                # print 'Subscription'
    except Exception as e:
        pass

    # Refund
    try:
        refund = fee_data_all['RefundEventList']['ShipmentEvent']
        if isinstance(refund,list):
            for redund_info in refund:
                fee_r_date = redund_info['PostedDate']
                fee_r_date = str(fee_r_date).replace('T',' ').replace('Z','')
                fee_r_orderId = redund_info['AmazonOrderId']
                fee_r_marketplace = redund_info['MarketplaceName']
                fee_r_sku = redund_info['ShipmentItemAdjustmentList']['ShipmentItem']['SellerSKU']
                fee_r_quantity = redund_info['ShipmentItemAdjustmentList']['ShipmentItem']['QuantityShipped']
                try:
                    fee_r_productSales = redund_info['ShipmentItemAdjustmentList']['ShipmentItem']['ItemChargeAdjustmentList']['ChargeComponent'][1]['ChargeAmount']['CurrencyAmount']
                except:
                    fee_r_productSales = 0.0
                try:
                    fee_r_shipping = redund_info['ShipmentItemAdjustmentList']['ShipmentItem']['ItemChargeAdjustmentList']['ChargeComponent'][0]['ChargeAmount']['CurrencyAmount']
                except:
                    fee_r_shipping = 0.0
                fee_r_fbaFees = -float(fee_r_shipping)
                try:
                    fee_r_sellingFee = float(redund_info['ShipmentItemAdjustmentList']['ShipmentItem']['ItemFeeAdjustmentList']['FeeComponent'][0]['FeeAmount']['CurrencyAmount'])+float(redund_info['ShipmentItemAdjustmentList']['ShipmentItem']['ItemFeeAdjustmentList']['FeeComponent'][1]['FeeAmount']['CurrencyAmount'])
                except:
                    fee_r_sellingFee = 0.0
                fee_r_total = float(fee_r_productSales) + float(fee_r_shipping) + float(fee_r_fbaFees) + float(fee_r_sellingFee)
                fee_refund_dict = {'datetime': fee_r_date, 'settlement': '', 'type': 'Refund','account_id':str(account_id),
                                  'orderID': fee_r_orderId,
                                  'sku': fee_r_sku,
                                  'description': '', 'quantity': fee_r_quantity, 'marketplace': fee_r_marketplace,'fulfillment':'Amazon',
                                  'productSales': fee_r_productSales,
                                  'shippingCredits': fee_r_shipping, 'giftWrapCredits': ' ',
                                  'promotionalRebates': ' ', 'salesTaxCollected': '',
                                  'sellingFees': fee_r_sellingFee, 'fbaFees': fee_r_fbaFees, 'otherTransactionFees': 0.0,
                                  'other': 0.0, 'total': fee_r_total, 'acount': ''
                                  }
                fee_list.append(fee_refund_dict)
        else:
            fee_r_date = refund['PostedDate']
            fee_r_date = str(fee_r_date).replace('T', ' ').replace('Z', '')
            fee_r_orderId = refund['AmazonOrderId']
            fee_r_marketplace = refund['MarketplaceName']
            fee_r_sku = refund['ShipmentItemAdjustmentList']['ShipmentItem']['SellerSKU']
            fee_r_quantity = refund['ShipmentItemAdjustmentList']['ShipmentItem']['QuantityShipped']
            fee_r_productSales = refund['ShipmentItemAdjustmentList']['ShipmentItem']['ItemChargeAdjustmentList']['ChargeComponent'][1]['ChargeAmount']['CurrencyAmount']
            fee_r_shipping = refund['ShipmentItemAdjustmentList']['ShipmentItem']['ItemChargeAdjustmentList']['ChargeComponent'][0]['ChargeAmount']['CurrencyAmount']
            fee_r_fbaFees = -float(fee_r_shipping)
            fee_r_sellingFee = float(refund['ShipmentItemAdjustmentList']['ShipmentItem']['ItemFeeAdjustmentList']['FeeComponent'][0]['FeeAmount']['CurrencyAmount'])+float(refund['ShipmentItemAdjustmentList']['ShipmentItem']['ItemFeeAdjustmentList']['FeeComponent'][1]['FeeAmount']['CurrencyAmount'])
            fee_r_total = float(fee_r_productSales) + float(fee_r_shipping) + float(fee_r_fbaFees) + float(fee_r_sellingFee)
            fee_refund_dict = {'datetime':fee_r_date.split('T')[0], 'settlement': '', 'type': 'Refund','account_id':str(account_id),
                              'orderID': fee_r_orderId,
                              'sku': fee_r_sku,
                              'description': '', 'quantity': fee_r_quantity, 'marketplace': fee_r_marketplace,'fulfillment':'Amazon',
                              'productSales': fee_r_productSales,
                              'shippingCredits': fee_r_shipping, 'giftWrapCredits': ' ',
                              'promotionalRebates': ' ', 'salesTaxCollected': '',
                              'sellingFees': fee_r_sellingFee, 'fbaFees': fee_r_fbaFees, 'otherTransactionFees': 0.0,
                              'other': 0.0, 'total': fee_r_total, 'acount': ''
                              }
            fee_list.append(fee_refund_dict)
    except:
        pass

    # order
    for fee_order in fee_data_all['ShipmentEventList']['ShipmentEvent']:
        fee_o_date = fee_order['PostedDate']
        fee_o_date = str(fee_o_date).replace('T', ' ').replace('Z', '')
        fee_o_marketplace = fee_order['MarketplaceName']
        fee_o_orderId = fee_order['AmazonOrderId']
        if isinstance(fee_order['ShipmentItemList']['ShipmentItem'],dict):
            # fee_o_orderId = fee_order['ShipmentItemList']['ShipmentItem']['OrderItemId']
            fee_o_sku = fee_order['ShipmentItemList']['ShipmentItem']['SellerSKU']
            fee_o_quantity = fee_order['ShipmentItemList']['ShipmentItem']['QuantityShipped']

            try:
                fee_o_promotional = 0.0
                for promotion in fee_order['ShipmentItemList']['ShipmentItem']['PromotionList']['Promotion']:
                    fee_o_promotional += float(promotion['PromotionAmount']['CurrencyAmount'])
            except:
                fee_o_promotional = 0.0

            fee_o_productSales = fee_order['ShipmentItemList']['ShipmentItem']['ItemChargeList']['ChargeComponent'][0]['ChargeAmount']['CurrencyAmount']
            fee_o_salesTax = fee_order['ShipmentItemList']['ShipmentItem']['ItemChargeList']['ChargeComponent'][1]['ChargeAmount']['CurrencyAmount']
            fee_o_shipping = fee_order['ShipmentItemList']['ShipmentItem']['ItemChargeList']['ChargeComponent'][4]['ChargeAmount']['CurrencyAmount']
            fee_o_giftWrap = fee_order['ShipmentItemList']['ShipmentItem']['ItemChargeList']['ChargeComponent'][2]['ChargeAmount']['CurrencyAmount']
            fee_o_sellingFees = float(fee_order['ShipmentItemList']['ShipmentItem']['ItemFeeList']['FeeComponent'][3]['FeeAmount']['CurrencyAmount'])+float(fee_order['ShipmentItemList']['ShipmentItem']['ItemFeeList']['FeeComponent'][-1]['FeeAmount']['CurrencyAmount'])

            fab = 0

            try:
                for i in fee_order['ShipmentItemList']['ShipmentItem']['ItemFeeList']['FeeComponent']:
                    # print i
                    if i['FeeType'] == 'FBAPerOrderFulfillmentFee':
                        fab += float(i['FeeAmount']['CurrencyAmount'])
                    if i['FeeType'] == 'FBAPerUnitFulfillmentFee':
                        fab += float(i['FeeAmount']['CurrencyAmount'])
                    if i['FeeType'] == 'FBAWeightBasedFee':
                        fab += float(i['FeeAmount']['CurrencyAmount'])
                        break
            except Exception as e:
                print (e)
            fee_o_fbaFees = fab
            # print fee_o_fbaFees

            fee_o_total = float(fee_o_productSales) + float(fee_o_salesTax) + float(fee_o_shipping) + float(fee_o_giftWrap) + float(fee_o_sellingFees) + float(fee_o_fbaFees)

            fee_order_dict = {'datetime':fee_o_date, 'settlement': '', 'type': 'Order','account_id':str(account_id),
                              'orderID': fee_o_orderId,
                              'sku': fee_o_sku,
                              'description': '', 'quantity': fee_o_quantity, 'marketplace': fee_o_marketplace,'fulfillment':'Amazon',
                              'productSales': fee_o_productSales,
                              'shippingCredits': fee_o_shipping, 'giftWrapCredits': fee_o_giftWrap,
                              'promotionalRebates': fee_o_promotional, 'salesTaxCollected': fee_o_salesTax,
                              'sellingFees': fee_o_sellingFees, 'fbaFees': fee_o_fbaFees, 'otherTransactionFees': 0.0,
                              'other': 0.0, 'total': fee_o_total, 'acount': ''
                              }
            fee_list.append(fee_order_dict)
        else:
            for fee_for_o_order in fee_order['ShipmentItemList']['ShipmentItem']:
                # fee_o_orderId = fee_for_o_order['OrderItemId']
                fee_o_sku = fee_for_o_order['SellerSKU']
                fee_o_quantity = fee_for_o_order['QuantityShipped']
                fee_o_productSales = fee_for_o_order['ItemChargeList']['ChargeComponent'][0]['ChargeAmount']['CurrencyAmount']
                fee_o_salesTax = fee_for_o_order['ItemChargeList']['ChargeComponent'][1]['ChargeAmount']['CurrencyAmount']
                fee_o_shipping = fee_for_o_order['ItemChargeList']['ChargeComponent'][4]['ChargeAmount']['CurrencyAmount']
                fee_o_giftWrap = fee_for_o_order['ItemChargeList']['ChargeComponent'][2]['ChargeAmount']['CurrencyAmount']
                try:
                    fee_o_sellingFees = fee_for_o_order['ItemFeeList']['FeeComponent'][3]['FeeAmount']['CurrencyAmount']
                except:
                    fee_o_sellingFees = 0.0
                try:
                    fee_o_promotional = 0.0
                    for promotion in fee_for_o_order['ShipmentItemList']['ShipmentItem']['PromotionList']['Promotion']:
                        fee_o_promotional += promotion['PromotionAmount']['CurrencyAmount']
                except:
                    fee_o_promotional = 0.0
                fab = 0
                for i in range(len(fee_for_o_order['ItemFeeList']['FeeComponent'])):
                    fab += float(fee_for_o_order['ItemFeeList']['FeeComponent'][i]['FeeAmount']['CurrencyAmount'])
                fee_o_fbaFees = fab
                fee_o_total = float(fee_o_productSales)+ float(fee_o_salesTax)+ float(fee_o_shipping)+ float(fee_o_giftWrap)+ float(fee_o_sellingFees )+ float(fee_o_fbaFees)
                fee_order_dict = {'datetime':fee_o_date, 'settlement': '', 'type': 'Order','account_id':str(account_id),
                                  'orderID': fee_o_orderId,
                                  'sku': fee_o_sku,
                                  'description': '', 'quantity': fee_o_quantity, 'marketplace': fee_o_marketplace,
                                  'fulfillment': 'Amazon',
                                  'productSales': fee_o_productSales,
                                  'shippingCredits': fee_o_shipping, 'giftWrapCredits': fee_o_giftWrap,
                                  'promotionalRebates': fee_o_promotional,
                                  'salesTaxCollected': fee_o_salesTax, 'sellingFees': fee_o_sellingFees,
                                  'fbaFees': fee_o_fbaFees, 'otherTransactionFees': 0.0,
                                  'other': 0.0, 'total': float(fee_o_total), 'acount': ''
                                  }
                fee_list.append(fee_order_dict)
    try:
        for fee_adjust in fee_data_all['AdjustmentEventList']['AdjustmentEvent']:
            adjust = fee_adjust['AdjustmentItemList']['AdjustmentItem']
            fee_a_sku = adjust['SellerSKU']
            # fee_a_description = str(adjust['ProductDescription'])[:200]
            fee_a_description = ''
            fee_a_quantity = adjust['Quantity']
            fee_a_other = adjust['PerUnitAmount']['CurrencyAmount']
            fee_a_total = adjust['TotalAmount']['CurrencyAmount']

            fee_adjust_dict = {'datetime': db_time, 'settlement': '', 'type': 'Adjustment', 'account_id':account_id,'orderID': '', 'sku': fee_a_sku,
                              'description': fee_a_description, 'quantity': fee_a_quantity, 'marketplace': '','fulfillment':'Amazon',
                               'productSales': '',
                              'shippingCredits': 0.0, 'giftWrapCredits': 0.0, 'promotionalRebates': 0.0,'salesTaxCollected': 0.0,
                               'sellingFees': 0.0, 'fbaFees': 0.0,'otherTransactionFees': 0.0,'other': fee_a_other, 'total': fee_a_total, 'acount': ''
                              }
            fee_list.append(fee_adjust_dict)
    except:
        pass

    # title = ['datetime','settlement','type','orderID','sku','description', 'quantity','marketplace',
    #         'fulfillment','orderCity','orderState', 'orderPostal','productSales','shippingCredits','giftWrapCredits',
    #          'promotionalRebates','salesTaxCollected','sellingFees','fbaFees','otherTransactionFees','other','total','acount' ]

    # flie = open(fileName,'aw')
    #
    # for fee_dict in fee_list:
    #     for t in title:
    #         fee_dict[t] = str(fee_dict[t])
    #         flie.write(fee_dict[t] + '\t')
    #         # response.write('\t'.join(amazon[key]))
    #     flie.write('\n')
    # print fee_list
    return fee_list

##promiton PromotionMetaDataDefinitionValue