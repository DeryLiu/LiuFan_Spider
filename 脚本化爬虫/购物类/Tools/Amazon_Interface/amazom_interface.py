from Tools.util.xml_util import get_element_by_tag
from xml.dom.minidom import parseString
from Tools.Amazon_Interface.Amazon_API import Amazon_Finance
from Tools.Amazon_Interface.Amazon_API import Amazon_Reports
# from webStore_API import webStore
# from order.models import Amazon_Account
# import re
# import xmltodict
# import json

class AmazonFinancial:
    """
     amazon 财务信息接口
    """
    def __init__(self,account):
        self.api = Amazon_Finance(account['access_key'],account['secret_key'],account['account_id'],account['mkplace_id'],account['MWSAuthToken'])

    def list_finace_eventgroup(self,from_date,to_date):
        """
        获取财务信息　分组id
        :param from_date:2016-11-28T00:44:39
        :param to_date: 2016-12-02T00:44:39
        :return:{'result':True,'groupId':'125568'}/{'result':False,'message':''}
        """
        try:
            finance_event_group_obj = self.api.list_finace_event_group(from_date,to_date)
        except Exception as e:
            return {'result':False,'messgae':str(e)}
        # try:
            # dom = parseString(finance_event_group_obj)
            # root = dom.documentElement
            # listFinancialEventGroupsResponse = root.getElementsByTagName("ListFinancialEventGroupsResponse")
            # group_id = []
            # group_id_list_dom = get_element_by_tag(dom, "FinancialEventGroupId")
            # for groupID in listFinancialEventGroupsResponse:
            #     group_id.append(groupID.gegetElementsByTagName)
        # except:
        #     return {'result':False, 'message':'未解析到groupId'}
        return {'result':True, 'group_xml':finance_event_group_obj}

    def list_finace_event(self,group_id):
        """
        :param group_id: 财务信息　分组id
        :return:
        """
        try:
            finance_event_group_obj = self.api.list_finace_event(group_id)
        except Exception as e:
            return {'result':False,'messgae':str(e)}

        try:
            dom = parseString(finance_event_group_obj)
            nextToken = get_element_by_tag(dom,"NextToken")
        except:
            return {'result':False,'message':'已无NextToken'}

        return {'result':True, 'finance_event_group_obj':finance_event_group_obj,'NextToken':nextToken}

    def list_finace_event_by_nextToken(self,nextToken):
        """
        :param nextToken: list_finance_event 的NextToken
        :return:
        """
        try:
            finance_event_group_obj = self.api.list_finace_event_by_nextToken(nextToken)
        except Exception as e:
            return {'result':False,'message':str(e)}

        return {'result':True,'finance_event_group_obj':finance_event_group_obj}

    def finace_event_info(self,group_id):
        """
        :param group_id:
        :return: 解析成python 数据类型的财务信息
        """
        get_finace_event = self.list_finace_event(group_id)


class AmazonReport:
    """
     amazon 报表信息接口
    """
    def __init__(self,account):
        self.api = Amazon_Reports(account['access_key'],account['secret_key'],account['account_id'],account['mkplace_id'],account['MWSAuthToken'])

    def get_report_request_list(self,from_date,to_date):

        try:
            report_request_request = self.api.get_report_request_list(from_date,to_date)
            return {'result': True, 'report_xml': report_request_request}
        except Exception as e:
            return {'result':False,'messgae':str(e)}
        # try:
            # dom = parseString(finance_event_group_obj)
            # root = dom.documentElement
            # listFinancialEventGroupsResponse = root.getElementsByTagName("ListFinancialEventGroupsResponse")
            # group_id = []
            # group_id_list_dom = get_element_by_tag(dom, "FinancialEventGroupId")
            # for groupID in listFinancialEventGroupsResponse:
            #     group_id.append(groupID.gegetElementsByTagName)
        # except:
        #     return {'result':False, 'message':'未解析到groupId'}


    def get_report(self,report_id):
        """
        :param group_id: 财务信息　分组id
        :return:
        """
        try:
            report_request_info = self.api.get_report(report_id)
            return {'result': True, 'report_request_info': report_request_info}

        except Exception as e:
            return {'result':False,'messgae':str(e)}
