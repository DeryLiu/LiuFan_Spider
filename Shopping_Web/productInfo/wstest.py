import pytz
import random
from datetime import datetime,timedelta
from Tools.AMAZON_API.ebay_api import GetOrder as GeteBayOrders
from Tools.AMAZON_API.amazon_api.Amazon_api import Amazon_AWS,Amazon_MWS
from multiprocessing import Pool,Lock

    
if __name__=="__main__":
    
    to_time = str(datetime.now(pytz.UTC) - timedelta(hours = 2)).split('.')[0].replace(' ','T') + 'Z'
    print ('start:',datetime.now(pytz.UTC))
    from_time = str(datetime.now(pytz.UTC) - timedelta(days = 1)).split('.')[0].replace(' ','T') + 'Z'
    amazon_mws = Amazon_MWS()
    amazon_aws = Amazon_AWS()
# #    
# 
# #    Token = 'AgAAAA**AQAAAA**aAAAAA**vFecUg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6AFmISiAJSBoQ6dj6x9nY+seQ**MQwCAA**AAMAAA**xWUulPShO7Y1hOjrGmiNPHVjZdDtjLDRV/51lLtl0mwcO7yHaQe7ntfz2va/bzX4wiSm3QkVP6mq1LUtfLlup20SPGw7CShIXINg4p0N2tfxzgzckCnMw6EDNwKV3dmhsF+XwHP2hbbyp8eu/b+LtEBELhPMNhkbZhQ5ajMniaYzGomfpkWWhpbEGlDCCQORjGP43NF/SgYdrGUtf6Y7Liz8cLwseGARVOhHg+SxexptVrrWrKGF66P6zjv4io/Q4ju3cUzzT2zwEs8x3AvFh3dcdJ/DX45hxsCM34TmcpGq4duCesqOtqwout2LTrWYzshIUGM5vQJV7J4Ykd7EtLvG2ezaPVGZ10T7sWdSP5G4HcBW8b+09oWz5RMUKEd7m3BzGANrFMpjuZ3zUP1evMEm33OYG0rcExKaUPBB+vdAckwGfhNeZUicagiPX5pdyfTSHs06MuGK8sz+5KddiVIsACE09Jfy+3kV/X0NOrRaI5taffinT8nHGIRA9+TiCiBBGP8yf1k1yaryuV60WX9yX3XMjW2XWjYRGUGaMdJdk/bccZYIkNL5wNeh2Xc/fK1Z/hCzkZFUh/eg0Olv4kZrXvl6zpOuJ++xnZmgFW7qj84c1/ANEU0i7DNY6orSbAKg5XwlFYU6ROBqnBoXbV0k9F9XVVrLXGGynAELLnU4X7am09M9U0ZYfdDm2Y9cxWkZxvYFiFLhUxOZQvqXukRgrVMmtp+AiHoemJUG/HBw3yBC6zHl/UUUxyeK00Ie'
# #
# #    print 'eBay------------------------------------------------------' 
# #    print GeteBayOrders.list_orders(Token,from_time=from_time,to_time = to_time)
# #    print 'Amazon----------------------------------------------------'
# #    print amazon_mws.list_orders('ARWTKM5K67VQV',created_after = from_time,created_before = to_time,buyer_email='b1jc50253h7twc3@marketplace.amazon.com')
# #    print 'list_orders is OK----------------------------'
# #    print amazon_mws.get_fba_product_inventory('ARWTKM5K67VQV',sku_list = ['0B-K5PK-4COJ','2D-55GW-K5BD'])
# #    print 'get_fba_product_inventory is OK----------------------------'
# #     print  amazon_mws.get_product_report('ARWTKM5K67VQV')
# #    print 'get_product_report is OK-----------------------------------'
# #     print amazon_mws.get_product_price('A21RN4NVMV9AWZ',SellerSKU = ['2094869245-KING', 'A02SM107887-KING', 'B000A7S636-KING', 'B000BSLW8U-KING', 'B000EG4ITY-KING', 'B000FIVQBO-KING', 'B000GA53CO-KING', 'B000HDJT6Q-KING', 'B000IZ9N78-KING', 'B000J4I9VO-KING', 'B000JSGLBK-KING', 'B000K6DH3Q-KING', 'B000NU9VPW-KING', 'B000NUBY0C-KING', 'B000OFSBL6-KING', 'B000P1OA1O-KING', 'B000P583I6-KING', 'B000PT18OS-KING', 'B000Q06LI4', 'B000Q06LI4-KING'])
# #    print 'get_product_price is OK------------------------------------'
# #     print amazon_aws.get_product_search('nokia','US','Small')
#     print amazon_aws.get_product_info('1449372422,B04UUA6MI','US',True)
# #    print 'get_product_info is OK-------------------------------------'
# #     print amazon_aws.get_category_tree('US')
# #    print 'browse_node_lookup is OK-----------------------------------'
# #     print amazon_mws.set_product_price('ARWTKM5K67VQV',sku_price_list = {'B004UUA6MI':{'price':8.99,'currency':'USD'}})   #OK
# #    print 'set product price is OK------------------------------------'
# #    print 'end:',datetime.now(pytz.UTC)
# #     print amazon_mws.get_product_competitive_price('ARWTKM5K67VQV',SellerSKU = ['0B-K5PK-4COJ','2D-55GW-K5BD'])
#     print 'start:',datetime.now(pytz.UTC)

t = datetime.now(pytz.UTC)
fr = open('par_results.txt','w')
ferr = open('paerrors.txt','w')
lock1 = Lock()
lock2 = Lock()
j = 0
def get_product_infos(asins):
    
    global lock1,lock2,fr,ferr,j
    result = amazon_aws.get_product_variation(','.join(asins),'de')
    if result['result']:
        print  ('have')
        for p in result['data']:
            #  lock1.acquire()
            j += 1
            fr.write(str(p)+'\n')
            print (i)
            #  lock1.release()
            
    else:
        print ('not',str(result['error_message']))
        #lock2.acquire()
        ferr.write(str(asins)+'\t'+str(result['error_message'])+'\n')
        #lock2.release()       
        
    print (asins)
         
with open('par_asins.txt') as f:
    
    a = f.readlines()
    
    N = 10
    b=[a[i:i+N] for i in range( 1,len(a)+1,N)]
    

    for ls in b:
        get_product_infos(ls)
    #pool = Pool(processes = 1)
    #result = pool.map(get_product_infos, b)
    #pool.close()
    #pool.join()
            

fr.close()
ferr.close()
tf = datetime.now(pytz.UTC)

print (str(t),str(tf),str(tf-t))
# print(i)
