# -*- coding:utf-8 -*-

import json
import pymysql
from list import zyry,bgjl,fzjg,rzls,hxtd,qyyw,flss,sxr,bzxr,jyyc,xzcf,yzwf,gqcz,dcdy,qsgg,ztb,xxgd,swpj,zzzs,sbxx,zl
import chardet
import re

def get_all_json():

    global warn ,error,null
    warn= 'warn'
    error = 'error'
    null ='null'

    def get_jbxx(jbxxss):
        if jbxxss == '':
            return ' '
        else:
            jbxxs = eval(jbxxss.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))
            base_info1 = {}
            base_info2 = {}
            base_info1['legal_representative'] = jbxxs['法人代表']

            base_info1['registered_capital'] = jbxxs['注册资本']
            base_info1['registered_time'] = jbxxs['注册时间']
            base_info1['management_status'] = jbxxs['经营状态']
            base_info1['business_registration_number'] = jbxxs['工商注册号']
            base_info1['organization_code'] = jbxxs['组织机构代码']
            base_info1['uniform_credit_code'] = jbxxs['统一信用代码']
            base_info1['industry'] = jbxxs['企业类型']
            base_info1['enterprise_type'] = jbxxs['行业']
            base_info1['business_term'] = jbxxs['营业期限']
            base_info1['approval_date'] = jbxxs['核准日期']
            base_info1['registration_authority'] = jbxxs['登记机关']
            base_info1['registered_address'] = jbxxs['注册地址']
            base_info1['scope_of_business'] = jbxxs['经营范围']

            # base_info_list = []
            # base_info_list.append(base_info1)
            # base_info_list = str(base_info_list)

            base_info2 ['base_info'] = base_info1
            base_info2 = json.dumps(base_info2,ensure_ascii=False)
            return  base_info2

    db = pymysql.connect(host = "localhost", user = "root", password = "123456", db = "tyc", port=3306, charset='utf8')
    cursor = db.cursor()
    select_sql = "SELECT * FROM tianyancha_info;"
    db.commit()
    cursor.execute(select_sql)
    for i in cursor.fetchall():
        id,name,jbxx,ssxx,qybj, qyfz, sffx, jyfx, jyzk, zscq= i

        provider_id = 1
        # qybj - ['基本信息','主要人员', '股东信息','变更记录','分支机构']
        try:
            base_info = get_jbxx(jbxx)
        except:
            base_info = ''

        # main_person = get_data_json(qybj,**zyry)
        try:
            main_person_post = [i['typeJoin'] for i in eval(qybj.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['主要人员']['result']]
            main_person_name = [i['name'] for i in eval(qybj.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['主要人员']['result']]
            main_person_list = []
            for i in range(len(main_person_post)):
                main_person_list.append({'post':main_person_post[i][0],'name':main_person_name[i]})
            # print(main_person_list)
            main_person = json.dumps({'main_person':main_person_list},ensure_ascii=False)
        except:
            main_person = ''

        # print(shareholder_info)
        try:
            shareholder_info_dict = [i for i in eval(qybj.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['股东信息']['result']]
            shareholder_info_name = shareholder_info_dict[0]['name']
            shareholder_info_amomon = [shareholder_info_dict[0]['capital'][i]['amomon'] for i in range(len(shareholder_info_dict[0]['capital']))]
            shareholder_info_percent = [shareholder_info_dict[0]['capital'][i]['percent'] for i in range(len(shareholder_info_dict[0]['capital']))]
            list1 = []
            for i in range(len(shareholder_info_amomon)):
                list1.append({'contributive_proportion':shareholder_info_percent[i],'subscribed_capital_contribution':shareholder_info_amomon[i]})
            shareholder_info = json.dumps({'shareholder_info':{'shareholder':shareholder_info_name,'list1':list1}},ensure_ascii=False)
        except:
            shareholder_info = ''
        # print(shareholder_info)

        try:
            change_record_dict = [i for i in eval(qybj.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['变更记录']['result']]

            change_record_change_time = [change_record_dict[i]['changeTime'] for i in range(len(change_record_dict))]
            change_record_change_project = [change_record_dict[i]['changeItem'] for i in range(len(change_record_dict))]
            change_record_change_before = [change_record_dict[i]['contentAfter'] for i in range(len(change_record_dict))]

            change_record_list = []
            for i in range(len(change_record_change_time)):
                change_record_list.append({'change_time':change_record_change_time[0],'change_project':change_record_change_project[0],'change_before':change_record_change_before[0]})

            change_record = json.dumps({'change_record':change_record_list},ensure_ascii=False)

        except:
            change_record = ''
        # print(change_record)
        # #
        try:
            branch_dict = [i for i in eval(qybj.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['分支机构']['result']]
            branch_enterprise_name = [branch_dict[i]['name'] for i in range(len(branch_dict))]

            branch_legal_representative = [branch_dict[i]['legalPersonName'] if 'legalPersonName' in branch_dict[i].keys() else ' ' for i in range(len(branch_dict)) ]
            branch_status = [branch_dict[i]['regStatus'] if 'regStatus' in branch_dict[i].keys() else ' ' for i in range(len(branch_dict))]
            branch_register_time = [branch_dict[i]['estiblishTime'] if 'estiblishTime' in branch_dict[i].keys() else ' ' for i in range(len(branch_dict))]
            branch_list = []
            for i in range(len(branch_legal_representative)):
                branch_list.append({'enterprise_name':branch_enterprise_name[i],'legal_representative':branch_legal_representative[i],'status':branch_status[i],'register_time':branch_register_time[i]})

            branch = json.dumps({'branch':branch_list},ensure_ascii=False)
        except:
            branch = ''
        # print(branch)

        # # qyfz - ['融资历史', '核心团队','企业业务']
        #
        # financing_history = get_data_qyfz(qyfz,**rzls)
        try:
            financing_history_dict = [i for i in eval(qyfz.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['融资历史']['page']['rows']]

            financing_history_time = [branch_dict[i]['date'] if 'date' in financing_history_dict[i].keys() else ' ' for i in range(len(financing_history_dict)) ]
            financing_history_round = [branch_dict[i]['round'] if 'round' in financing_history_dict[i].keys() else ' ' for i in range(len(financing_history_dict)) ]
            financing_history_valuation = [branch_dict[i]['value'] if 'value' in financing_history_dict[i].keys() else ' ' for i in range(len(financing_history_dict)) ]
            financing_history_money = [branch_dict[i]['money'] if 'money' in financing_history_dict[i].keys() else ' ' for i in range(len(financing_history_dict)) ]
            financing_history_proportion = [branch_dict[i]['share'] if 'share' in financing_history_dict[i].keys() else ' ' for i in range(len(financing_history_dict)) ]
            financing_history_investors = [branch_dict[i]['Map'] if 'Map' in financing_history_dict[i].keys() else ' ' for i in range(len(financing_history_dict)) ]
            financing_history_news_source = [branch_dict[i]['newsTitle'] if 'newsTitle' in financing_history_dict[i].keys() else ' ' for i in range(len(financing_history_dict)) ]
            financing_history_list = []
            for i in range(len(financing_history_time)):
                financing_history_list.append({'time':financing_history_time[i],'round':financing_history_round[i],'valuation':financing_history_valuation[i],'money':financing_history_money[i],'proportion':financing_history_proportion[i],'investors':financing_history_investors[0],'news_source':financing_history_news_source[i]})

            financing_history = json.dumps({'financing_history_time':financing_history_list},ensure_ascii=False)
        except:
            financing_history = ''
        # print(financing_history)

        # core_team = get_data_qyfz(qyfz,**hxtd)
        try:
            core_team_dict = [i for i in eval(qyfz.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['核心团队']['page']['rows']]

            core_team_name = [core_team_dict[i]['name'] if 'name' in core_team_dict[i].keys() else ' ' for i in range(len(core_team_dict)) ]
            core_team_logo_url = [core_team_dict[i]['icon'] if 'icon' in core_team_dict[i].keys() else ' ' for i in range(len(core_team_dict)) ]
            core_team_post = [core_team_dict[i]['title'] if 'title' in core_team_dict[i].keys() else ' ' for i in range(len(core_team_dict)) ]
            core_team_content = [core_team_dict[i]['desc'] if 'desc' in core_team_dict[i].keys() else ' ' for i in range(len(core_team_dict)) ]
            core_team_list = []
            for i in range(len(core_team_name)):
                core_team_list.append({'name':core_team_name[i],'icon':core_team_logo_url[i],'post':core_team_post[i],'content':core_team_content[i]})

            core_team = json.dumps({'core_team':core_team_list},ensure_ascii=False)
        except:
            core_team = ''
        # print(core_team)


        # enterprise_business = get_data_qyfz(qyfz,**qyyw)
        try:
            enterprise_business_dict = [i for i in eval(qyfz.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['企业业务']['page']['rows']]

            enterprise_business_img_url = [enterprise_business_dict[i]['logo'] if 'logo' in enterprise_business_dict[i].keys() else ' ' for i in range(len(enterprise_business_dict)) ]
            enterprise_business_business_name = [enterprise_business_dict[i]['product'] if 'product' in enterprise_business_dict[i].keys() else ' ' for i in range(len(enterprise_business_dict)) ]
            enterprise_business_business_introduce = [enterprise_business_dict[i]['hangye'] if 'hangye' in enterprise_business_dict[i].keys() else ' ' for i in range(len(enterprise_business_dict)) ]
            enterprise_business_content = [enterprise_business_dict[i]['yewu'] if 'yewu' in enterprise_business_dict[i].keys() else ' ' for i in range(len(enterprise_business_dict)) ]

            enterprise_business_list = []
            for i in range(len(enterprise_business_img_url)):
                enterprise_business_list.append({'img_url':enterprise_business_img_url[i],'business_name':enterprise_business_business_name[i],'business_introduc':enterprise_business_business_introduce[i],'content':enterprise_business_content[i]})

            enterprise_business = json.dumps({'enterprise_business':enterprise_business_list},ensure_ascii=False)
        except:
            enterprise_business = ''
        # print(enterprise_business)

        # # sffx - ['法律诉讼',  '法院公告', '失信人', '被执行人']
        # legal_proceedings = get_data_json(sffx,**flss)
        try:
            legal_proceedings_dict = [i for i in eval(sffx.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['法律诉讼']['items']]
            legal_proceedings_time = [legal_proceedings_dict[i]['submittime'] if 'submittime' in legal_proceedings_dict[i].keys() else ' ' for i in range(len(legal_proceedings_dict)) ]
            legal_proceedings_referee_documen = [legal_proceedings_dict[i]['title'] if 'title' in legal_proceedings_dict[i].keys() else ' ' for i in range(len(legal_proceedings_dict)) ]
            legal_proceedings_documen_type = [legal_proceedings_dict[i]['casetype'] if 'casetype' in legal_proceedings_dict[i].keys() else ' ' for i in range(len(legal_proceedings_dict)) ]
            legal_proceedings_document_number = [legal_proceedings_dict[i]['casetype'] if 'casetype' in legal_proceedings_dict[i].keys() else ' ' for i in range(len(legal_proceedings_dict)) ]

            legal_proceedings_list = []
            for i in range(len(legal_proceedings_time)):
                legal_proceedings_list.append({'time':legal_proceedings_time[i],'referee_documen':legal_proceedings_referee_documen[i],'documen_type':legal_proceedings_documen_type[i],'document_number':legal_proceedings_document_number[i]})

            legal_proceedings = json.dumps({'legal_proceedings':legal_proceedings_list},ensure_ascii=False)
        except:
            legal_proceedings = ''
        # print(legal_proceedings)


        # court_notice = get_fygg(sffx)
        try:
            court_notice_dict = [i for i in eval(sffx.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['法院公告']]
            court_notice_time = [court_notice_dict[i]['publishdate'] if 'publishdate' in court_notice_dict[i].keys() else ' ' for i in range(len(court_notice_dict)) ]
            court_notice_appellant = [court_notice_dict[i]['party1'] if 'party1' in court_notice_dict[i].keys() else ' ' for i in range(len(court_notice_dict)) ]
            court_notice_defendant = [court_notice_dict[i]['party2'] if 'party2' in court_notice_dict[i].keys() else ' ' for i in range(len(court_notice_dict)) ]
            court_notice_announcement_type = [court_notice_dict[i]['bltntypename'] if 'bltntypename' in court_notice_dict[i].keys() else ' ' for i in range(len(court_notice_dict)) ]
            court_notice_court = [court_notice_dict[i]['courtcode'] if 'courtcode' in court_notice_dict[i].keys() else ' ' for i in range(len(court_notice_dict)) ]

            court_notice_list = []

            for i in range(len(court_notice_time)):
                court_notice_list.append({'time':court_notice_time[i],'appellan':court_notice_appellant[i],
                                          'defendan':court_notice_defendant[i],'announcement_type':court_notice_announcement_type[i],
                                          'court':court_notice_court[i]})
            court_notice = json.dumps({'court_notice':court_notice_list},ensure_ascii=False)
        except:
            court_notice = ''
        # print(court_notice)

        # dishonest_person = get_data_json(sffx,**sxr)
        #
        try:
            dishonest_person_dict = [i for i in eval(sffx.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['失信人']['items']]

            dishonest_person_time = [dishonest_person_dict[i]['publishdate'] if 'publishdate' in dishonest_person_dict[i].keys() else ' ' for i in range(len(dishonest_person_dict)) ]
            dishonest_person_case_no = [dishonest_person_dict[i]['gistid'] if 'gistid' in dishonest_person_dict[i].keys() else ' ' for i in range(len(dishonest_person_dict)) ]
            dishonest_person_court_execution = [dishonest_person_dict[i]['courtname'] if 'courtname' in dishonest_person_dict[i].keys() else ' ' for i in range(len(dishonest_person_dict)) ]
            dishonest_person_performance_status = [dishonest_person_dict[i]['performance'] if 'performance' in dishonest_person_dict[i].keys() else ' ' for i in range(len(dishonest_person_dict)) ]
            dishonest_person_execution_reference_number = [dishonest_person_dict[i]['casecode'] if 'casecode' in dishonest_person_dict[i].keys() else ' ' for i in range(len(dishonest_person_dict)) ]

            dishonest_person_list = []
            for i in range(len(dishonest_person_time)):
                dishonest_person_list.append({'time':dishonest_person_time[i],'case_no':dishonest_person_case_no[i],
                                          'court_execution':dishonest_person_court_execution[i],'performance_status':dishonest_person_performance_status[i],
                                          'reference_number':dishonest_person_execution_reference_number[i]})
            dishonest_person = json.dumps({'dishonest_person':dishonest_person_list},ensure_ascii=False)
        except:
            dishonest_person = ''
        # print(dishonest_person)

        # person_subjected_execution = get_data_json(sffx,**bzxr)
        try:
            person_subjected_execution_dict = [i for i in eval(sffx.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['被执行人']['items']]

            person_subjected_execution_time = [person_subjected_execution_dict[i]['caseCreateTime'] if 'caseCreateTime' in person_subjected_execution_dict[i].keys() else ' ' for i in range(len(person_subjected_execution_dict)) ]
            person_subjected_execution_case_no = [person_subjected_execution_dict[i]['caseCode'] if 'caseCode' in person_subjected_execution_dict[i].keys() else ' ' for i in range(len(person_subjected_execution_dict)) ]
            person_subjected_execution_object_execution = [person_subjected_execution_dict[i]['execMoney'] if 'execMoney' in person_subjected_execution_dict[i].keys() else ' ' for i in range(len(person_subjected_execution_dict)) ]
            person_subjected_execution_court_justice = [person_subjected_execution_dict[i]['execCourtName'] if 'execCourtName' in person_subjected_execution_dict[i].keys() else ' ' for i in range(len(person_subjected_execution_dict)) ]

            person_subjected_execution_list = []
            for i in range(len(person_subjected_execution_time)):
                person_subjected_execution_list.append({'time':person_subjected_execution_time[i],'case_no':person_subjected_execution_case_no[i],
                                          'object_execution':person_subjected_execution_object_execution[i],'court_justice':person_subjected_execution_court_justice[i]})
            person_subjected_execution = json.dumps({'person_subjected_execution':person_subjected_execution_list},ensure_ascii=False)
        except:
            person_subjected_execution = ''
        # print(person_subjected_execution)
        #
        # # jyfx - ['经营异常',  '行政处罚', '严重违法',  '股权出资, '动产抵押', '欠税公告',  ']
        # abnormal_operation = get_data_json(jyfx, **jyyc)
        try:
            abnormal_operation_dict = [i for i in eval(jyfx.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['经营异常']['result']]

            abnormal_operation_time = [abnormal_operation_dict[i]['putDate'] if 'putDate' in abnormal_operation_dict[i].keys() else ' ' for i in range(len(abnormal_operation_dict)) ]
            abnormal_operation_case = [abnormal_operation_dict[i]['putReason'] if 'putReason' in abnormal_operation_dict[i].keys() else ' ' for i in range(len(abnormal_operation_dict)) ]
            abnormal_operation_decision_organ = [abnormal_operation_dict[i]['putDepartment'] if 'putDepartment' in abnormal_operation_dict[i].keys() else ' ' for i in range(len(abnormal_operation_dict)) ]

            abnormal_operation_list = []
            for i in range(len(abnormal_operation_time)):
                abnormal_operation_list.append({'time':abnormal_operation_time[i],'case':abnormal_operation_case[i],
                                          'decision_organ':abnormal_operation_decision_organ[i]})
            abnormal_operation = json.dumps({'abnormal_operation':abnormal_operation_list},ensure_ascii=False)
        except:
            abnormal_operation = ''
        # print(abnormal_operation)

        # administrative_sanction = get_data_json(jyfx,**xzcf)
        try:
            administrative_sanction_dict = [i for i in eval(jyfx.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['行政处罚']['items']]
            # print(administrative_sanction_dict)
            administrative_sanction_time = [administrative_sanction_dict[i]['decisionDate'] if 'decisionDate' in administrative_sanction_dict[i].keys() else ' ' for i in range(len(administrative_sanction_dict)) ]
            administrative_sanction_letter_decision = [administrative_sanction_dict[i]['punishNumber'] if 'punishNumber' in administrative_sanction_dict[i].keys() else ' ' for i in range(len(administrative_sanction_dict)) ]
            administrative_sanction_type = [administrative_sanction_dict[i]['type'] if 'type' in administrative_sanction_dict[i].keys() else ' ' for i in range(len(administrative_sanction_dict)) ]
            administrative_sanction_decision_organ = [administrative_sanction_dict[i]['departmentName'] if 'departmentName' in administrative_sanction_dict[i].keys() else ' ' for i in range(len(administrative_sanction_dict)) ]

            administrative_sanction_list = []
            for i in range(len(administrative_sanction_time)):
                administrative_sanction_list.append({'time':administrative_sanction_time[i],'letter_decision':administrative_sanction_letter_decision[i],
                                          'type':administrative_sanction_type[i],'decision_organ':administrative_sanction_decision_organ[i]})
            administrative_sanction = json.dumps({'administrative_sanction':administrative_sanction_list},ensure_ascii=False)
        except:
            administrative_sanction = ''
        # print(administrative_sanction)

        # serious_violation = get_data_json(jyfx, **yzwf)
        try:
            serious_violation_dict = [i for i in eval(jyfx.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['严重违法']['items']]
            # print(serious_violation_dict)
            serious_violation_time = [serious_violation_dict[i]['putDate'] if 'putDate' in serious_violation_dict[i].keys() else ' ' for i in range(len(serious_violation_dict)) ]
            serious_violation_executive_council = [serious_violation_dict[i]['putReason'] if 'putReason' in serious_violation_dict[i].keys() else ' ' for i in range(len(serious_violation_dict)) ]
            serious_violation_decision_organ = [serious_violation_dict[i]['putDepartment'] if 'putDepartment' in serious_violation_dict[i].keys() else ' ' for i in range(len(serious_violation_dict)) ]

            serious_violation_list = []
            for i in range(len(serious_violation_time)):
                serious_violation_list.append({'time':serious_violation_time[i],'executive_council':serious_violation_executive_council[i],
                                          'decision_organ':serious_violation_decision_organ[i]})
            serious_violation = json.dumps({'serious_violation':serious_violation_list},ensure_ascii=False)
        except:
            serious_violation = ''

        #
        # stock_ownership = get_data_json(jyfx, **gqcz)
        try:
            stock_ownership_dict = [i for i in eval(jyfx.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['股权出资']['items']]
            # print(stock_ownership_dict)

            stock_ownership_time = [stock_ownership_dict[i]['regDate'] if 'regDate' in stock_ownership_dict[i].keys() else ' ' for i in range(len(stock_ownership_dict)) ]
            stock_ownership_registration_number = [stock_ownership_dict[i]['regNumber'] if 'regNumber' in stock_ownership_dict[i].keys() else ' ' for i in range(len(stock_ownership_dict)) ]
            stock_ownership_pledgor = [stock_ownership_dict[i]['pledgor'] if 'pledgor' in stock_ownership_dict[i].keys() else ' ' for i in range(len(stock_ownership_dict)) ]
            stock_ownership_apledgee = [stock_ownership_dict[i]['pledgee'] if 'pledgee' in stock_ownership_dict[i].keys() else ' ' for i in range(len(stock_ownership_dict)) ]
            stock_ownership_status = [stock_ownership_dict[i]['state'] if 'state' in stock_ownership_dict[i].keys() else ' ' for i in range(len(stock_ownership_dict)) ]

            stock_ownership_list = []
            for i in range(len(stock_ownership_time)):
                stock_ownership_list.append({'time':stock_ownership_time[i],'registration_number':stock_ownership_registration_number[i],
                                          'pledgor':stock_ownership_pledgor[i],'apledge':stock_ownership_apledgee[i],'status':stock_ownership_status[i]})
            stock_ownership = json.dumps({'stock_ownership':stock_ownership_list},ensure_ascii=False)
        except:
            stock_ownership = ''
        # print(stock_ownership)

        # chattel_mortgage = get_data_json(jyfx, **dcdy)
        try:
            chattel_mortgage_dict = [i for i in eval(jyfx.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['动产抵押']]
            # print(chattel_mortgage_dict)
            chattel_mortgage = ''
        except:
            chattel_mortgage = ''

        # tax_notice = get_data_json(jyfx,**qsgg)
        try:
            tax_notice_dict = [i for i in eval(jyfx.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['欠税公告']['items']]
            # print(tax_notice_dict)
            tax_notice_taxes_taxes = [tax_notice_dict[i]['taxCategory'] if 'taxCategory' in tax_notice_dict[i].keys() else ' ' for i in range(len(tax_notice_dict)) ]
            tax_notice_balance_tax_arrearss = [tax_notice_dict[i]['ownTaxAmount'] if 'ownTaxAmount' in tax_notice_dict[i].keys() else ' ' for i in range(len(tax_notice_dict)) ]

            tax_notice_list = []
            for i in range(len(tax_notice_taxes_taxes)):
                tax_notice_list.append({'taxes_taxes':tax_notice_taxes_taxes[i],'balance_tax_arrearss':tax_notice_balance_tax_arrearss[i]})
            tax_notice = json.dumps({'tax_notice':tax_notice_list},ensure_ascii=False)
        except:
            tax_notice = ''
        #
        # # jyzk - [ '招投标', '购地信息', '税务评级', '资质证书', ]
        # bidding = get_data_json(jyzk, **ztb)
        try:
            bidding_dict = [i for i in eval(jyzk.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['招投标']['items']]
            # print(bidding_dict)
            tax_notice_time = [bidding_dict[i]['publishTime'] if 'publishTime' in bidding_dict[i].keys() else ' ' for i in range(len(bidding_dict)) ]
            tax_notice_title = [bidding_dict[i]['title'] if 'title' in bidding_dict[i].keys() else ' ' for i in range(len(bidding_dict)) ]
            tax_notice_purchaser = [bidding_dict[i]['purchaser'] if 'purchaser' in bidding_dict[i].keys() else ' ' for i in range(len(bidding_dict)) ]
            bidding_list = []
            for i in range(len(tax_notice_time)):
                bidding_list.append({'time':tax_notice_time[i],'title':tax_notice_title[i],'purchaser':tax_notice_purchaser[i]})
            bidding = json.dumps({'bidding':bidding_list},ensure_ascii=False)
        except:
            bidding = ''
        # print(bidding)

        # purchase_information = get_data_json(jyzk, **xxgd)
        try:
            purchase_information_dict = [i for i in eval(jyzk.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['购地信息']['companyPurchaseLandList']]
            # print(purchase_information_dict)
            purchase_information_time = [purchase_information_dict[i]['signedDate'] if 'signedDate' in purchase_information_dict[i].keys() else ' ' for i in range(len(purchase_information_dict)) ]
            purchase_information_electronic_regulatory_number = [purchase_information_dict[i]['elecSupervisorNo'] if 'elecSupervisorNo' in purchase_information_dict[i].keys() else ' ' for i in range(len(purchase_information_dict)) ]
            purchase_information_agreed_commencement_date = [purchase_information_dict[i]['createTime'] if 'createTime' in purchase_information_dict[i].keys() else ' ' for i in range(len(purchase_information_dict)) ]
            purchase_information_gross_floor_area = [purchase_information_dict[i]['totalArea'] if 'totalArea' in purchase_information_dict[i].keys() else ' ' for i in range(len(purchase_information_dict)) ]
            purchase_information_administrative_region = [purchase_information_dict[i]['location'] if 'location' in purchase_information_dict[i].keys() else ' ' for i in range(len(purchase_information_dict)) ]

            purchase_information_list = []
            for i in range(len(purchase_information_time)):
                purchase_information_list.append({'time':purchase_information_time[i],'electronic_regulatory_number':purchase_information_electronic_regulatory_number[i],'agreed_commencement_date':purchase_information_agreed_commencement_date[i],
                                                  'gross_floor_area':purchase_information_gross_floor_area[i],'administrative_region':purchase_information_administrative_region})
            purchase_information = json.dumps({'purchase_information':purchase_information_list},ensure_ascii=False)
        except:
            purchase_information = ''

        # tax_rating = get_data_json(jyzk, **swpj)
        try:
            tax_rating_dict = [i for i in eval(jyzk.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['税务评级']['items']]
            # print(tax_rating_dict)
            tax_rating_particular_year = [tax_rating_dict[i]['year'] if 'year' in tax_rating_dict[i].keys() else ' ' for i in range(len(tax_rating_dict)) ]
            tax_rating_tax_rating = [tax_rating_dict[i]['grade'] if 'grade' in tax_rating_dict[i].keys() else ' ' for i in range(len(tax_rating_dict)) ]
            tax_rating_type = [tax_rating_dict[i]['type'] if 'type' in tax_rating_dict[i].keys() else ' ' for i in range(len(tax_rating_dict)) ]
            tax_rating_taxpayer_identification_number = [tax_rating_dict[i]['idNumber'] if 'idNumber' in tax_rating_dict[i].keys() else ' ' for i in range(len(tax_rating_dict)) ]
            tax_rating_evaluation_unit = [tax_rating_dict[i]['evalDepartment'] if 'evalDepartment' in tax_rating_dict[i].keys() else ' ' for i in range(len(tax_rating_dict)) ]

            tax_rating_list = []
            for i in range(len(tax_rating_particular_year)):
                tax_rating_list.append({'particular_year':tax_rating_particular_year[i],'tax_rating':tax_rating_tax_rating[i],
                                        'type':tax_rating_type[i],'taxpayer_identification_number':tax_rating_taxpayer_identification_number[i],
                                        'evaluation_unit':tax_rating_evaluation_unit[i]})
            tax_rating = json.dumps({'tax_rating':tax_rating_list},ensure_ascii=False)
        except:
            tax_rating = ''
        # print(tax_rating)
        # qualification_certificate = get_data_json(jyzk, **zzzs)
        try:
            qualification_certificate_dict = [i for i in eval(jyzk.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['资质证书']['items']]
            # print(qualification_certificate_dict)
            qualification_certificate_device_name = [qualification_certificate_dict[i]['deviceName'] if 'deviceName' in qualification_certificate_dict[i].keys() else ' ' for i in range(len(qualification_certificate_dict)) ]
            qualification_certificate_certificate_type = [qualification_certificate_dict[i]['licenceType'] if 'licenceType' in qualification_certificate_dict[i].keys() else ' ' for i in range(len(qualification_certificate_dict)) ]
            qualification_certificate_date_issue = [qualification_certificate_dict[i]['issueDate'] if 'issueDate' in qualification_certificate_dict[i].keys() else ' ' for i in range(len(qualification_certificate_dict)) ]
            qualification_certificate_closing_date = [qualification_certificate_dict[i]['toDate'] if 'toDate' in qualification_certificate_dict[i].keys() else ' ' for i in range(len(qualification_certificate_dict)) ]
            qualification_certificate_device_number = [qualification_certificate_dict[i]['deviceType'] if 'deviceType' in qualification_certificate_dict[i].keys() else ' ' for i in range(len(qualification_certificate_dict)) ]
            qualification_certificate_license_number = [qualification_certificate_dict[i]['licenceNum'] if 'licenceNum' in qualification_certificate_dict[i].keys() else ' ' for i in range(len(qualification_certificate_dict)) ]

            qualification_certificate_list = []
            for i in range(len(qualification_certificate_device_name)):
                qualification_certificate_list.append({'device_name':qualification_certificate_device_name[i],
                                                       'certificate_type':qualification_certificate_certificate_type[i],
                                                       'date_issue':qualification_certificate_date_issue[i],
                                                  'closing_date':qualification_certificate_closing_date[i],
                                                       'device_number':qualification_certificate_device_number[i],
                                                       'license_number':qualification_certificate_license_number})
            qualification_certificate = json.dumps({'qualification_certificate':qualification_certificate_list},ensure_ascii=False)
        except:
            qualification_certificate = ''
        # print(qualification_certificate)

        # # zscq - ['商标信息', '专利']
        # trademark_information = get_data_json(zscq, **sbxx)
        try:
            trademark_information_dict = [i for i in eval(zscq.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['商标信息']['items']]
            # print(trademark_information_dict)
            trademark_information_date_application = [trademark_information_dict[i]['appDate'] if 'appDate' in trademark_information_dict[i].keys() else ' ' for i in range(len(trademark_information_dict)) ]
            trademark_information_status = [trademark_information_dict[i]['category'] if 'category' in trademark_information_dict[i].keys() else ' ' for i in range(len(trademark_information_dict)) ]
            trademark_information_trademark = [trademark_information_dict[i]['tmPic'] if 'tmPic' in trademark_information_dict[i].keys() else ' ' for i in range(len(trademark_information_dict)) ]
            trademark_information_trademark_name = [trademark_information_dict[i]['tmName'] if 'tmName' in trademark_information_dict[i].keys() else ' ' for i in range(len(trademark_information_dict)) ]
            trademark_information_register_number = [trademark_information_dict[i]['regNo'] if 'regNo' in trademark_information_dict[i].keys() else ' ' for i in range(len(trademark_information_dict)) ]
            trademark_information_type = [trademark_information_dict[i]['intCls'] if 'intCls' in trademark_information_dict[i].keys() else ' ' for i in range(len(trademark_information_dict)) ]

            trademark_information_list = []
            for i in range(len(trademark_information_date_application)):
                trademark_information_list.append({'date_application':trademark_information_date_application[i],
                                                   'trademark':trademark_information_trademark[i],
                                                   'trademark_name':trademark_information_trademark_name[i],
                                                  'register_number':trademark_information_register_number[i],
                                                   'type':trademark_information_type[i],
                                                   'status':trademark_information_status[i]})
            trademark_information = json.dumps({'trademark_information':trademark_information_list},ensure_ascii=False)
        except:
            trademark_information = ''
        # print(trademark_information)

        # patent = get_data_json(zscq, **zl)
        try:
            patent_dict = [i for i in eval(zscq.replace('"{','{').replace('}"','}').replace('"[','[').replace(']"',']'))['专利']['items']]
            # print(tax_rating_dict)
            patent_application_date = [patent_dict[i]['applicationPublishTime'] if 'applicationPublishTime' in patent_dict[i].keys() else ' ' for i in range(len(patent_dict)) ]
            patent_patent_name = [patent_dict[i]['patentName'] if 'patentName' in patent_dict[i].keys() else ' ' for i in range(len(patent_dict)) ]
            patent_application_number = [patent_dict[i]['patentNum'] if 'patentNum' in patent_dict[i].keys() else ' ' for i in range(len(patent_dict)) ]
            patent_application_publication_number = [patent_dict[i]['applicationPublishNum'] if 'applicationPublishNum' in patent_dict[i].keys() else ' ' for i in range(len(patent_dict)) ]

            patent_list = []
            for i in range(len(patent_application_date)):
                patent_list.append({'application_date':patent_application_date[i],
                                    'patent_name':patent_patent_name[i],
                                    'application_number':patent_application_number[i],
                                    'application_publication_number':patent_application_publication_number[i],})
            patent = json.dumps({'patent':patent_list},ensure_ascii=False)
        except:
            patent = ''
        # print(patent)
        try:
            insert_sql = "INSERT INTO fq_provider_business(`provider_id`,`base_info`,`main_person`,`shareholder_info`,`change_record`,`branchs`,`financing_history`,`core_team`,`enterprise_business`,`legal_proceedings`,`court_notice`,`dishonest_person`,`person_subjected_execution`,`abnormal_operation`,`administrative_sanction`,`serious_violation`,`stock_ownership`,`chattel_mortgage`,`tax_notice`,`bidding`,`purchase_information`,`tax_rating`,`qualification_certificate`,`trademark_information`,`patent`,`company`) VALUES ({},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(provider_id,base_info, main_person, shareholder_info, change_record, branch, financing_history,core_team, enterprise_business, legal_proceedings, court_notice, dishonest_person,person_subjected_execution, abnormal_operation, administrative_sanction, serious_violation,stock_ownership, chattel_mortgage, tax_notice, bidding, purchase_information, tax_rating,qualification_certificate, trademark_information, patent,name)
            # print(insert_sql)
            # print('\n')
            cursor.execute(insert_sql)
            db.commit()
        except Exception as e:
            db.rollback()
            print(e,name)

if __name__ == '__main__':
    # get_all_json()
    db = pymysql.connect(host = "localhost", user = "root", password = "123456", db = "Spider_Data", port=3306, charset='utf8')
    cursor = db.cursor()
    select_SQL = 'SELECT company,change_record FROM fq_provider_business;'
    cursor.execute(select_SQL)
    for i in cursor.fetchall():
        # print(i)
        try:
            a = type(eval(i[1]))
        except:
            print(i[0],i[1])








