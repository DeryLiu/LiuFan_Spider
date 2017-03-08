# class webStore(object):
'''
    account ={
          'Token':Token,
          'Developer':Developer,
          'Application':Application,
          'Certificate':Certificate,
          'Runname':Runname
          }
    account = {
          'access_key':access_key,
          'secret_key':secret_key,
          'account_id':account_id,
          'mkplace_id':mkplace_id,
          'MWSAuthToken':MWSAuthToken,
          }
'''
from importlib import import_module

channels = ['eBay', 'Amazon', 'Aliexpress', 'Wish', 'Lazada']
cmd_modules = {}
for channel in channels:
    #    if channel != 'Amazon':
    #        cmd_module = import_module('.'.join(__name__.split('.')[0:-1]) +  '.'+channel)
    #        cmd_modules[channel] = cmd_module.Interface
    #    else:
    if channel in ['Aliexpress', 'Wish', 'Lazada', 'Amazon']:
        cmd_module = import_module('order.webStore.' + channel)
    else:
        cmd_module = import_module('order.webStore2.' + channel)

    cmd_modules[channel] = cmd_module.Interface


def webStore(channel):
    return cmd_modules[channel]


if __name__ == '__main__':
    import pytz
    from datetime import datetime, timedelta

    account_ebay = {}
    account_amazon = {}
    account_aliexpress = {
        'app_key': '8804320',
        'secret_key': 'cpYvKMR452F6',
        'refresh_token': 'f058121d-ca0c-48d9-ab2a-781044cfdf96',
        'access_token': '5d4f105c-247e-40bc-9ae3-c3135856ff94',
        'code': '1aef368e-5850-44da-bf62-dcec7c2cf253',
    }
    now_time = datetime.now(pytz.UTC) - timedelta(seconds=120)
    timeTo = now_time.strftime('%FT%TZ')
    timeFrom = (now_time - timedelta(hours=4)).strftime('%FT%TZ')

    #    -----------------------------------------aliexpress---------------------------------------
    timeTo = now_time.strftime('%m/%d/%Y %H:%M:%S')
    timeFrom = (now_time - timedelta(hours=24)).strftime('%m/%d/%Y %H:%M:%S')
    # temp_dict = {'page' : 1, 'pageSize' : 5, 'orderStatus' : 'WAIT_SELLER_SEND_GOODS', 'createDateStart' : timeFrom, 'createDateEnd' : timeTo}

    # print temp_dict
    aliexpress = webStore('Aliexpress')(account_aliexpress)

    # od = aliexpress.get_order_list(**temp_dict)
    # print od
    temp_dict = {'orderId': 71122365356513}
    od = aliexpress.get_order(**temp_dict)
    print (od)