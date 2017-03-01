#!/usr/bin/python
# -*- coding: utf-8 -*- 
import httplib

class eBay_Call:
    RequestData = "<xml />"
    DetailLevel = "ReturnAll"
    SiteID = "0"
    
    Developer = "ed67f460-65c9-460d-bcf0-f0ffa3bb6207"
    Application = "StarMerx-060d-418e-9358-8252bbe9b89b"
    Certificate = "a69abcc2-989e-4560-a339-9329bd291ffe"
    Runname = 'StarMerx-StarMerx-060d-4-sfjlzrkd'
    
    ServerURL = "https://api.ebay.com/ws/api.dll"
    Command = "/ws/api.dll"
    Server = "api.ebay.com"
    
     
#     def __init__(self,Developer,Application,Certificate):
#         self.Developer = Developer
#         self.Application = Application
#         self.Certificate = Certificate

    def MakeCall(self, CallName):
        while True:
            try:
                conn = httplib.HTTPSConnection(self.Server, timeout=20)
                if CallName == 'UploadSiteHostedPictures':
                    conn.request("POST", self.Command, self.RequestData, self.GenerateHeaders_upload_picture(CallName, len(self.RequestData), self.Developer, self.Application, self.Certificate))
                    response = conn.getresponse()
                    break
                else:
                    conn.request("POST", self.Command, self.RequestData, self.GenerateHeaders(CallName, self.Developer, self.Application, self.Certificate))
                    response = conn.getresponse()
                    break
                
            except Exception, e:
                    pass               
        
        data = response.read()
        conn.close()
        return data


    def GenerateHeaders(self, CallName, Developer, Application, Certificate):
        headers = {"X-EBAY-API-COMPATIBILITY-LEVEL": "863",
                   "X-EBAY-API-SESSION-CERTIFICATE": Developer + ";" + Application + ";" + Certificate,
                   "X-EBAY-API-DEV-NAME": Developer,
                   "X-EBAY-API-APP-NAME": Application,
                   "X-EBAY-API-CERT-NAME": Certificate,
                   "X-EBAY-API-CALL-NAME": CallName,
                   "X-EBAY-API-SITEID": self.SiteID,
                   "X-EBAY-API-DETAIL-LEVEL": self.DetailLevel,
                   "Content-Type": "text/xml"}
        return headers


    def GenerateHeaders_upload_picture(self, CallName, length, Developer, Application, Certificate):
        headers = {
                  "Content-Type": "multipart/form-data; boundary=MIME_boundary",
                  "Content-Length":length,
                  "X-EBAY-API-COMPATIBILITY-LEVEL": "863",
                  "X-EBAY-API-DEV-NAME": Developer,
                  "X-EBAY-API-APP-NAME": Application,
                  "X-EBAY-API-CERT-NAME": Certificate,
                  "X-EBAY-API-CALL-NAME": CallName,
                  "X-EBAY-API-SITEID": self.SiteID,
                  }
        return headers

def getSessionID():
    '''
    获取SeesionID
    '''
    api = eBay_Call()
    api.RequestData = """
        <?xml version="1.0" encoding="utf-8"?>
        <GetSessionIDRequest xmlns="urn:ebay:apis:eBLBaseComponents">
            <RuName>%(MyRuNameHere)s</RuName>
        </GetSessionIDRequest>
            """
    api.RequestData = api.RequestData % { 'MyRuNameHere': api.Runname, }
    responseDOM = api.MakeCall("GetSessionID")
    SessionID = responseDOM.getElementsByTagName("SessionID")[0].childNodes[0].data
    return SessionID

def geturl(SessionID):
    '''
    获取链接url
    '''
    api = eBay_Call()
    ebay_urls = ("https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&RuName=%s&SessID=%s") % ((api.Runname), (SessionID))
    return ebay_urls

def getToken(SessionID):
    '''
    获取eBay用户的token
    '''
    api = eBay_Call()
    api.RequestData = """
        <?xml version="1.0" encoding="utf-8"?>
        <FetchTokenRequest xmlns="urn:ebay:apis:eBLBaseComponents">
            <SessionID>%(SessionID)s</SessionID>
        </FetchTokenRequest>
            """
    api.RequestData = api.RequestData % { 'SessionID': SessionID, }
    responseDOM = api.MakeCall("FetchToken")
    
    if(responseDOM.getElementsByTagName("Ack")[0].childNodes[0].data == 'Success'):
        status = "success"
        data = responseDOM.getElementsByTagName("eBayAuthToken")[0].childNodes[0].data
    else:
        status = "failed"
        data = responseDOM.getElementsByTagName("Errors")[0].getElementsByTagName("ShortMessage")[0].childNodes[0].data
    
    return {"status": status, "data" : data, }
    
def Get_items(Token, itemID):
    '''
    获取item信息
    @param Token: eBay网店的标示
    @param itemID: 获取的标识信息
    '''
    api = eBay_Call()
    api.RequestData = """
        <?xml version="1.0" encoding="utf-8"?>
        <GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
            <RequesterCredentials>
                <eBayAuthToken>%(token)s</eBayAuthToken>
            </RequesterCredentials>
            <ItemID>%(itemID)s</ItemID>
        </GetItemRequest>
            """
    api.RequestData = api.RequestData % { 'token': Token,
                                          'itemID' :  itemID,
                                        }
    responseDOM = api.MakeCall("GetItem")
    return responseDOM

def get_ebay_img_url(Token, ItemID):
    '''
    获取eBay的item信息
    @param Token: eBay网店的标示
    @param ItmeID: item的标识
    '''
    my_dom = Get_items(Token, ItemID)
    try:
        img_url = my_dom.getElementsByTagName("PictureURL")[0].childNodes[0].data
    except Exception, e:
        img_url = my_dom.getElementsByTagName("GalleryURL")[0].childNodes[0].data
    return img_url

def Get_orders(timeFrom, timeTo, Token, Pagenumber, perpage):
    '''
    获取order信息
    @param timeFrom: 起始时间
    @param timeTo: 结束时间
    @param Token: 网店的标识
    @param Pagenumber: 订单的页数
    '''
    api = eBay_Call()
    api.RequestData = """
        <?xml version="1.0" encoding="utf-8"?>
        <GetOrdersRequest xmlns="urn:ebay:apis:eBLBaseComponents">
        <RequesterCredentials>
        <eBayAuthToken>%(token)s</eBayAuthToken>
        </RequesterCredentials>
        <ModTimeFrom>%(startTime)s</ModTimeFrom>
        <ModTimeTo>%(endTime)s</ModTimeTo>
        <IncludeFinalValueFee>True</IncludeFinalValueFee>
        <OrderRole>Seller</OrderRole>
        <OrderStatus>Completed</OrderStatus>
        <DetailLevel>ReturnAll</DetailLevel>
        <Pagination> 
        <EntriesPerPage>%(perpage)s</EntriesPerPage>
        <PageNumber>%(pagenumber)s</PageNumber>
        </Pagination>
        </GetOrdersRequest>
    """
    api.RequestData = api.RequestData % { 'token': Token,
                                          'startTime' :  timeFrom,
                                          'endTime' :  timeTo,
                                          'pagenumber': Pagenumber,
                                          'perpage':perpage,
                                        }
    responseDOM = api.MakeCall("GetOrders")
    return responseDOM

def Mark(OrderID, Token, Supplier, TrackingNumber):
    '''
    上传tracknumber到eBay网站
    @param OrderID: 订单ID
    @param Token: 网店标识
    @param Supplier: 订单的物流方式
    @param TrackingNumber: 订单的跟踪号
    '''
    my_api = eBay_Call()
    my_api.RequestData = """
        <?xml version="1.0" encoding="utf-8"?>
        <CompleteSaleRequest xmlns="urn:ebay:apis:eBLBaseComponents">
        <RequesterCredentials>
            <eBayAuthToken>%(token)s</eBayAuthToken>
        </RequesterCredentials>
        <OrderID>%(orderID)s</OrderID>
        <Shipped>true</Shipped>
        <Shipment>
          <ShipmentTrackingDetails>
           
            <ShipmentTrackingNumber>%(trackingnumber)s</ShipmentTrackingNumber>
            <ShippingCarrierUsed>%(supplier)s</ShippingCarrierUsed>
           
          </ShipmentTrackingDetails>
        </Shipment>
        </CompleteSaleRequest>
    """
    my_api.RequestData = my_api.RequestData % { 'token': Token,
                                          'orderID' : OrderID,
                                          'trackingnumber' : TrackingNumber,
                                          'supplier' : Supplier,
                                        }
    responseDOM = my_api.MakeCall("CompleteSale")
    return responseDOM


def Get_listing_products(timeFrom, timeTo, Token, Pagenumber, perpage):
    '''
    获取order信息
    @param timeFrom: 起始时间
    @param timeTo: 结束时间
    @param Token: 网店的标识
    @param Pagenumber: 产品页数
    '''
    api = eBay_Call()

    api.RequestData ='''
        <?xml version="1.0" encoding="utf-8"?>
        <GetSellerListRequest xmlns="urn:ebay:apis:eBLBaseComponents">
        <RequesterCredentials>
            <eBayAuthToken>%(token)s</eBayAuthToken>
        </RequesterCredentials>
        <EndTimeFrom>%(startTime)s</EndTimeFrom> 
        <EndTimeTo>%(endTime)s</EndTimeTo>
        <IncludeWatchCount>true</IncludeWatchCount>
        <OutputSelector>ItemArray.Item.ItemID</OutputSelector>
        <OutputSelector>ItemArray.Item.Title</OutputSelector>
        <OutputSelector>ItemArray.Item.ShippingDetails.ShippingServiceOptions</OutputSelector>
        <OutputSelector>ItemArray.Item.PictureDetails.GalleryURL</OutputSelector>
        <OutputSelector>ItemArray.Item.PictureDetails.PictureURL</OutputSelector>
        <OutputSelector>ItemArray.Item.SKU</OutputSelector>
        <OutputSelector>ItemArray.Item.SellingStatus</OutputSelector>
        <OutputSelector>ItemArray.Item.Quantity</OutputSelector>
        <OutputSelector>ItemArray.Item.ListingType</OutputSelector>
        <OutputSelector>ItemArray.Item.ListingDuration</OutputSelector>
        <OutputSelector>ItemArray.Item.Location</OutputSelector>
        <OutputSelector>ItemArray.Item.PrimaryCategory</OutputSelector>
        <OutputSelector>ItemArray.Item.SecondaryCategory</OutputSelector>
        <OutputSelector>PaginationResult</OutputSelector>
        <OutputSelector>ListingDetails.StartTime</OutputSelector>
        <OutputSelector>ItemArray.Item.ListingDetails.EndTime</OutputSelector>
        <Pagination> 
            <EntriesPerPage>%(perpage)s</EntriesPerPage>
            <PageNumber>%(pagenumber)s</PageNumber>
        </Pagination> 
        <GranularityLevel>Coarse</GranularityLevel> 
        </GetSellerListRequest>'''

    api.RequestData = api.RequestData % { 'token': Token,
                                          'startTime' :  timeFrom,
                                          'endTime' :  timeTo,
                                          'pagenumber': Pagenumber,
                                          'perpage':perpage,
                                        }

    responseDOM = api.MakeCall("GetSellerList")

    return responseDOM