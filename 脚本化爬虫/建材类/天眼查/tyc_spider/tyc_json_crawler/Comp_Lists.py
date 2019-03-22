# -*- coding:utf-8 -*-
#所有需要采集的json地址，38条
url_list=[r'http://www.tianyancha.com/stock/stockVolatility.json?graphId=%s',                      #number0
          r'http://www.tianyancha.com/stock/companyInfo.json?graphId=%s',                          #number1
          r'http://www.tianyancha.com/stock/seniorExecutive.json?graphId=%s&ps=10&pn=1',         #number2
          r'http://www.tianyancha.com/stock/holdingCompany.json?graphId=%s&ps=100&pn=1',          #number3
          r'http://www.tianyancha.com/stock/announcement.json?graphId=%s&ps=100&pn=1',            #number4
          r'http://www.tianyancha.com/stock/shareholder.json?graphId=%s&type=1',                   #number5
          r'http://www.tianyancha.com/stock/shareholder.json?graphId=%s&type=2',                   #number6
          r'http://www.tianyancha.com/stock/issueRelated.json?graphId=%s',                         #number7
          r'http://www.tianyancha.com/stock/shareStructure.json?graphId=%s',                       #number8
          r'http://www.tianyancha.com/stock/equityChange.json?graphId=%s&ps=100&pn=1',            #number9
          r'http://www.tianyancha.com/stock/bonusInfo.json?graphId=%s&ps=100&pn=1',               #number10
          r'http://www.tianyancha.com/stock/allotment.json?graphId=%s&ps=100&pn=1',               #number11
          r'http://www.tianyancha.com/v2/company/%s.json',                                         #number12
          r'http://www.tianyancha.com/expanse/staff.json?id=%s&ps=20&pn=1',                      #number13
          r'http://www.tianyancha.com/expanse/holder.json?id=%s&ps=20&pn=1',                     #number14
          r'http://www.tianyancha.com/expanse/inverst.json?id=%s&ps=100&pn=1',                    #number15
          r'http://www.tianyancha.com/expanse/changeinfo.json?id=%s&ps=100&pn=1',                 #number16
          r'http://www.tianyancha.com/expanse/branch.json?id=%s&ps=100&pn=1',                     #number17
          r'http://www.tianyancha.com/expanse/findHistoryRongzi.json?name=%s&ps=100&pn=1',        #name18
          r'http://www.tianyancha.com/expanse/findTeamMember.json?name=%s&ps=100&pn=1',           #name19
          r'http://www.tianyancha.com/expanse/findProduct.json?name=%s&ps=100&pn=1',              #name20
          r'http://www.tianyancha.com/expanse/findTzanli.json?name=%s&ps=100&pn=1',               #name21
          r'http://www.tianyancha.com/expanse/findJingpin.json?name=%s&ps=100&pn=1',              #name22
          r'http://www.tianyancha.com/v2/getlawsuit/%s.json?page=1&ps=100',                       #name23
          r'http://www.tianyancha.com/v2/court/%s.json?',                                          #name24
          r'http://www.tianyancha.com/v2/dishonest/%s.json',                                       #name25
          r'http://www.tianyancha.com/expanse/zhixing.json?id=%s&pn=1&ps=100',                     #number26
          r'http://www.tianyancha.com/expanse/abnormal.json?id=%s&ps=100&pn=1',                   #number27
          r'http://www.tianyancha.com/expanse/punishment.json?name=%s&ps=100&pn=1',               #name28
          r'http://www.tianyancha.com/expanse/illegal.json?name=%s&ps=100&pn=1',                  #name29
          r'http://www.tianyancha.com/expanse/companyEquity.json?name=%s&ps=100&pn=1',            #name30
          r'http://www.tianyancha.com/expanse/mortgageInfo.json?name=%s&pn=1&ps=100',             #name31
          r'http://www.tianyancha.com/expanse/owntax.json?id=%s&ps=100&pn=1',                     #number32
          r'http://www.tianyancha.com/expanse/bid.json?id=%s&pn=1&ps=100',                        #number33
          r'http://www.tianyancha.com/extend/getBondList.json?companyName=%s&pn=1&ps=100',        #name34
          r'http://www.tianyancha.com/expanse/purchaseland.json?name=%s&ps=100&pn=1',             #name35
          r'http://www.tianyancha.com/expanse/taxcredit.json?id=%s&ps=100&pn=1',                  #number36
          r'http://www.tianyancha.com/expanse/companyCheckInfo.json?name=%s&pn=1&ps=100',         #name37
          r'http://www.tianyancha.com/expanse/appbkinfo.json?id=%s&ps=100&pn=1',                  #number38
          r'http://www.tianyancha.com/expanse/qualification.json?id=%s&ps=100&pn=1',              #number39
          r'http://www.tianyancha.com/tm/getTmList.json?id=%s&pageNum=1&ps=100',                  #number40
          r'http://www.tianyancha.com/expanse/patent.json?id=%s&pn=1&ps=100',                     #number41
          r'http://www.tianyancha.com/expanse/copyReg.json?id=%s&pn=1&ps=100',                    #number42
          r'http://www.tianyancha.com/v2/IcpList/%s.json',                                         #number43
          ]


#每个小项的名字
infs_list=[u'股票行情',u'企业简介',u'高管信息',u'参股控股',u'上市公告',u'十大股东',u'十大流通',u'发行相关',u'股本结构',u'股本变动',u'分红情况',u'配股情况',
           u'基本信息',u'主要人员',u'股东信息',u'对外投资',u'变更记录',u'分支机构',
           u'融资历史',u'核心团队',u'企业业务',u'投资事件',u'竞品信息',
           u'法律诉讼',u'法院公告',u'失信人',u'被执行人',
           u'经营异常',u'行政处罚',u'严重违法',u'股权出资',u'动产抵押',u'欠税公告',
           u'招投标',u'债券信息', u'购地信息', u'税务评级',u'抽查检查',u'产品信息',u'资质证书',
           u'商标信息',u'专利',u'著作权',u'网站备案'
          ]