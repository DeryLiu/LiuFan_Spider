#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import json

def insert_db():
        global warn,null
        warn = 'warn'
        null = 'null'

        db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
        cursor = db.cursor()
        select_sql = "SELECT * FROM `test`;"
        cursor.execute(select_sql)

        for i in cursor.fetchall():
            qy_id,qy_name,qybj,qyfz,sffx,jyfx,jyzk,zscq,jbxx = i
            # print(qy_id,qy_name,qybj,qyfz,sffx,jyfx,jyzk,zscq,jbxx)
            #
            #
            try:
                provider_id = ''
                base_info = ' '
                # qybj - ['对外投资', '变更记录', '主要人员', '股东信息', '基本信息', '分支机构']
                main_person = clean_result(qybj,'主要人员')
                shareholder_info = clean_result(qybj,'股东信息')
                change_record = clean_result(qybj,'变更记录')
                branch = clean_result(qybj,'分支机构')
                # qyfz - ['融资历史', '投资事件', '企业业务', '竞品信息', '核心团队']
                financing_history = eval(eval(qyfz)['融资历史'])['page']['rows']
                core_team = eval(eval(qyfz)['核心团队'])['page']['rows']
                enterprise_business = eval(eval(qyfz)['企业业务'])['page']['rows']

                # sffx - ['失信人', '法律诉讼', '法院公告', '被执行人']
                legal_proceedings = clean_items(sffx,'法律诉讼')
                court_notice = eval(sffx)['法院公告']
                dishonest_person = clean_items(sffx,'失信人')
                person_subjected_execution = eval(sffx)['被执行人']

                # jyfx - ['严重违法', '行政处罚', '欠税公告', '动产抵押', '经营异常', '股权出资']
                abnormal_operation = clean_result(jyfx,'经营异常')
                administrative_sanction = clean_items(jyfx,'行政处罚')
                serious_violation = clean_items(jyfx,'严重违法')
                stock_ownership = clean_items(jyfx,'股权出资')
                chattel_mortgage = eval(jyfx)['动产抵押']
                # print(chattel_mortgage)
                tax_notice = eval(jyfx)['欠税公告']

                # jyzk - ['产品信息', '购地信息', '债券信息', '招投标', '抽查检查', '资质证书', '税务评级']
                bidding = clean_items(jyzk,'招投标')
                # ======
                # purchase_information = eval(jyzk)['购地信息']
                # tax_rating = eval(jyzk)['税务评级']
                # qualification_certificate = eval(jyzk)['资质证书']

                # zscq - ['著作权', '商标信息', '专利', '网站备案']
                # print(eval(zscq).keys())
                trademark_information = clean_items(zscq,'商标信息')
                patent = clean_items(zscq,'专利')
                # ======

                try:
                    insert_sql = "INSERT INTO fq_provider_business(`provider_id`,`base_info`,`main_person`,`shareholder_info`,`change_record`,`branch`,`financing_history`,`core_team`,`enterprise_business`,`legal_proceedings`,`court_notice`,`dishonest_person`,`person_subjected_execution`,`abnormal_operation`,`administrative_sanction`,`serious_violation`,`stock_ownership`,`chattel_mortgage`,`tax_notice`,`bidding`,`purchase_information`,`tax_rating`,`qualification_certificate`,`trademark_information`,`patent`) VALUES ({},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(provider_id,base_info,main_person,shareholder_info,change_record,branch,financing_history,core_team,enterprise_business,legal_proceedings,court_notice,dishonest_person,person_subjected_execution,abnormal_operation,administrative_sanction,serious_violation,stock_ownership,chattel_mortgage,tax_notice,bidding,purchase_information,tax_rating,qualification_certificate,trademark_information,patent)
                    cursor.execute(insert_sql)
                    db.commit()
                except:
                    db.rollback()
            except Exception as e:
                print(e)

def clean_result(qybj,keys):
    info_dict = eval(qybj)[keys]
    if info_dict != 'warn':
        info = eval(info_dict)['result']
    else:
        info = []
    return info

def clean_items(qybj,keys):
    info_dict = eval(qybj)[keys]
    if info_dict != 'error':
        info = eval(info_dict)['items']
    else:
        info = []
    return info

def test():
    a = {"招投标": "warn", "税务评级": "warn", "资质证书": "warn", "购地信息": "{\"totalRows\": 0, \"companyPurchaseLandList\": []}"}
    print(a['购地信息'])


def dbdab():
    db = pymysql.connect("localhost","root","123456","tyc",charset='utf8')
    cursor = db.cursor()
    select_sql = "SELECT * FROM `tyc_jbxx`;"
    cursor.execute(select_sql)
    for i in cursor.fetchall():
        # jb_id,name,ssxx,qybj,qyfz,sffx,jyfx,jyzk,zscq = i
        jb_id,name,jbxx = i

        # print(jb_id,name,ssxx,qybj,qyfz,sffx,jyfx,jyzk,zscq)
        # ssxx = ssxx.replace("'"," ")
        # qybj = qybj.replace("'"," ")
        # qyfz = qyfz.replace("'"," ")
        # sffx = sffx.replace("'"," ")
        # jyfx = jyfx.replace("'"," ")
        # jyzk = jyzk.replace("'"," ")
        # zscq = zscq.replace("'"," ")
        # print(jb_id,name,jbxx)
        try:
            # insert_sql = "INSERT INTO tianyancha_info(`name`,`jbxx`,`ssxx`,`qybj`,`qyfz`,`sffx`,`jyfx`,`jyzk`,`zscq`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(name,'',ssxx,qybj,qyfz,sffx,jyfx,jyzk,zscq)
            update_sql = "UPDATE tianyancha_info SET jbxx='{}' WHERE company_name='{}';".format(jbxx,name)
            cursor.execute(update_sql)
            db.commit()
        except Exception as e:
            db.rollback()
            print(e,name)
#


if __name__ == '__main__':
    # insert_db()
    # test()
    dbdab()

