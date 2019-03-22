import requests,pymysql,random
import http.cookiejar,time
from bs4 import BeautifulSoup
import pymysql,re,json

'''
http://www.buildnet.cn/
会员名：mhmt     密码：43ec371b

项目名称 project_name
项目阶段（哪些选项） 对应项目阶段表id字段
开发商名称
项目类型（扩建/新建/翻新/室内装饰/设备安装）"
# 项目所在省份
# 项目所在城市
项目详细地址（不含省市）
# 主体设计阶段（未开始/进行中/已结束）  项目阶段和项目进展
# 主体施工阶段（未开始/进行中/已结束）
# 室内精装修阶段（未开始/进行中/已结束）
是否精装修（是/否） # 装修状况
# 有无电梯（是/否）
# 有无空调（是/否）
有无钢结构（是/否） # 项目结构
建筑面积（㎡）
总投资额
造价（万元）
建筑层数（层数）
# 供暖方式
# 外墙材料
项目开工时间
项目结束时间
# 所需材料（从71个二级分类里面选） 是个图片
项目概况、简介	项目信息更新时间
项目联系人姓名
# 性别
所属公司（开发商/施工方/设计方/其他）
所属公司名称
职位
电话
工作地址
# 备注
# 是否主要联系人/负责人
# 招标文件（附件形式）
# 商业标文件/技术标文件
'''

def get_proxies_ip():
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    # db = pymysql.connect("192.168.1.231","root","3jw9lketj0","ConstructionMaterials",charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM proxies_info;"
    proxies_list = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            proxy_ip = row[1]
            proxy_port = str(row[2])
            proxies_list.append(proxy_ip+':'+proxy_port)
    except:
        db.rollback()
    db.close()
    proxies = {
        'http':'http://'+random.choice(proxies_list)
    }
    # return random.choice(proxies_list)
    return proxies

def get_url():
    # session = requests.Session()
    # # 建立LWPCookieJar实例，可以存Set-Cookie3类型的文件。
    # # 而MozillaCookieJar类是存为'/.txt'格式的文件
    # # session.cookies = http.cookiejar.LWPCookieJar(filename)
    # # 若本地有cookie则不用再post数据了
    # try:
    #     session.cookies.load(filename=filename, ignore_discard=True)
    # except:
    #     print('Cookie未加载！')
    #
    # content = session.post(login_url,data=login_data,headers={'User-Agent':random.choice(USER_AGENTS)})
    # # print(content.content)
    # # 保存cookie到本地
    # session.cookies.save(ignore_discard=True, ignore_expires=True)
    # url_info_file = open('url_info.csv','w')
    url_error = open('error.csv','w')

    with open('url_info.csv','w') as url_info_file:
        # url_list = ['http://gc.buildnet.cn/search/SearchFocus/{}?type=C'.format(i) for i in range(1,359)]
        url_list = ['http://gc.buildnet.cn/project/cusInstered/{}'.format(i) for i in range(1,360)]
        for url in url_list:
            print(url)
            headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Cache-Control':'max-age=0',
            'Cookie':'UM_distinctid=15ac5834dd5826-02a6cbfd64da5-1c3f6b52-1fa400-15ac5834dd675; Hm_lvt_278c40d73e1c74701321281c547dee93=1491809466; Hm_lvt_ad7a9a07410789cde726ecf1c0812be2=1489372313,1491805334; ASP.NET_SessionId=vabbuwi3yyrdlpasqx1ng1z4; _pk_ref.1.4c71=%5B%22%22%2C%22%22%2C1491877607%2C%22http%3A%2F%2Fwww.buildnet.cn%2F%22%5D; _pk_id.1.4c71=1733b1fe037cf981.1488870977.15.1491878569.1491877607.; Hm_lvt_63f6b5042ab289e50fc4496a601e350d=1491810625,1491875455; Hm_lpvt_63f6b5042ab289e50fc4496a601e350d=1491887303',
            'Host':'gc.buildnet.cn',
            # 'Origin':'http://gc.buildnet.cn',
            'Proxy-Connection':'keep-alive',
            # 'Referer':url,
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'''
            }
            try:
                time.sleep(5)
                reponse = requests.get(url,headers=headers,timeout=60)
                print(reponse.status_code)
                soup = BeautifulSoup(reponse.text,'html.parser')
                company_url_list = soup.select('tr > td.td_line > h3 > a')
                for company_url in company_url_list:
                    finall_url = 'http://gc.buildnet.cn'+company_url['href']
                    url_info_file.write(finall_url+'\n')
                    url_info_file.flush()
                    print(finall_url)
            except Exception as e:
                url_error.write(url+'\n')
                print(e)


def get_info():
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    # db = pymysql.connect("192.168.1.231","root","3jw9lketj0","fq_spider",charset='utf8')
    cursor=db.cursor()
    url_error = open('error.csv','w')
    # 读取url
    with open('0413.csv','r') as company_url_file:
    # with open('company_url.csv','r') as company_url_file:
        headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Connection':'keep-alive',
        'Cookie':'UM_distinctid=15ac5834dd5826-02a6cbfd64da5-1c3f6b52-1fa400-15ac5834dd675; Hm_lvt_278c40d73e1c74701321281c547dee93=1491809466; Hm_lvt_ad7a9a07410789cde726ecf1c0812be2=1489372313,1491805334; ASP.NET_SessionId=vabbuwi3yyrdlpasqx1ng1z4; _pk_ref.1.4c71=%5B%22%22%2C%22%22%2C1491887347%2C%22http%3A%2F%2Fwww.buildnet.cn%2F%22%5D; _pk_id.1.4c71=1733b1fe037cf981.1488870977.16.1491887347.1491887347.; Hm_lvt_63f6b5042ab289e50fc4496a601e350d=1491810625,1491875455; Hm_lpvt_63f6b5042ab289e50fc4496a601e350d=1491908458',
        'Host':'gc.buildnet.cn',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
        time_sleep = [5,6,7,8,9,10,11,12,13,14,15]
        for company_url in company_url_file.readlines():
            time.sleep(random.choice(time_sleep))
            print(company_url.strip())
            try:
                response = requests.get(company_url.strip(),headers=headers,timeout=70)

                soup = BeautifulSoup(response.text,'html.parser')
                try:
                    project_name = soup.select('#param_100100_2 > span')[0].text.split(':')[1].strip('-').strip() # 项目名 必填
                except:
                    project_name = soup.select('#param_100100_2 > span')[0].text.strip('-').strip()
                try:
                    project_stage = soup.select('#param_10001_2')[0].text.strip()
                except:
                    project_stage = ''
                # --------
                developer_name = ''
                developer_part = soup.select('#tbc_02 div.line_b')

                company_info = []
                for developer_info in developer_part:
                    # print(developer_info)
                    try:
                        company_section = developer_info.div.text.strip() # 所属公司 类别
                        contact_list_info = []
                        company_info.append({"section":company_section,"contact_list":contact_list_info})
                        # print(company_section)
                        part_re_info = re.findall('<table(.*?)</table>',str(developer_info),re.S)
                        for part_info in part_re_info:
                            type_contact_list = re.findall(': bold;">(.*?)</td>',part_info,re.S)
                            developer_role = type_contact_list[0] # 职位

                            contact_info = re.findall('FirmAddress(.*?);',part_info,re.S)[0].split("'")
                            contact_name = contact_info[1] # 项目联系人姓名
                            contact_genl = contact_info[3] # 性别
                            company_name_l = contact_info[7] # 公司名称

                            if developer_role == '发展商':
                                developer_name = company_name_l

                            contact_line_info = re.findall('<span class="line_span">(.*?)</span>',part_info,re.S)
                            # print(contact_line_info)

                            # 联系电话
                            try:
                                if int(contact_line_info[2].strip().split(' ')[1]) < 100000000:
                                    contact_telphone = int(contact_line_info[3].strip().split(' ')[1])
                                    if contact_telphone < 100000000:
                                        contact_telphone = contact_line_info[2].strip()
                                else:
                                    contact_telphone = contact_line_info[2].strip().split(' ')[1]
                                # print(contact_telphone)
                            except:
                                contact_telphone = contact_line_info[2].strip().split(' ')[1]

                            # 联系地址
                            if "(" in contact_line_info[-1]:
                                contact_address = contact_line_info[-1].strip()
                            else:
                                contact_address = contact_line_info[-2].strip()

                            # print(contact_telphone,contact_address)
                            contact_list_info.append({"公司名称":company_name_l,"职位":developer_role,"联系人":contact_name,"性别":contact_genl,"联系电话":contact_telphone,"联系地址":contact_address})
                    except:
                        pass
                # print(company_info)
                try:
                    project_type = soup.select('#param_10009_2')[0].text.strip()
                except:
                    project_type = ''
                province = ''
                city = ''
                try:
                    project_address = soup.select('#param_10061_2')[0].text.strip()
                except:
                    project_address = ''
                design_stage = ''
                build_stage = ''
                decorate_stage = ''
                try:
                    is_decorate = soup.select('#param_10011_2')[0].text.strip()
                except:
                    is_decorate = ''
                has_elevator = ''
                has_airconditioner = ''
                try:
                    has_steel = soup.select('#param_10106_2')[0].text.strip()
                except:
                    has_steel = ''
                try:
                    floor_space = soup.select('#param_10005_2')[0].text.strip()
                except:
                    floor_space = ''
                try:
                    investments = int(soup.select('#param_10033_2')[0].text.strip().split('(')[0])
                except:
                    investments = 0
                try:
                    cost = int(soup.select('#param_10030_2')[0].text.strip().split('(')[0])
                except:
                    cost = 0
                try:
                    floor_numbers = int(soup.select('#param_10007_2')[0].text.strip().split('层')[0])
                except:
                    floor_numbers = 0
                heating_mode = ''
                wall_materials = ''
                try:
                    time_start = soup.select('#param_10018_2')[0].text.strip()
                except:
                    time_start = ''
                try:
                    time_end = soup.select('#param_10019_2')[0].text.strip()
                except:
                    time_end = ''
                try:
                    need_materials = 'http://gc.buildnet.cn'+soup.select('tr.line_02 > td > img')[0]['src']
                except:
                    need_materials = ''
                try:
                    project_info = soup.select('#param_10017_2')[0].text.strip()
                except:
                    project_info
                # contact_name = company_info
                contact_gen = ''
                company_type = ''
                company_name = ''
                job = ''
                telphone = ''
                work_address = ''
                remark = ''
                is_main = ''
                file = ''
                buisness_file = ''
                # print(project_name,project_stage,developer_name,project_type,province,city,project_address,design_stage,
                #       build_stage,decorate_stage,is_decorate,has_elevator,has_airconditioner,has_steel,floor_space,investments,
                #       cost,floor_numbers,heating_mode,wall_materials,time_start,time_end,need_materials,project_info,company_info,
                #       contact_gen,company_type,company_name,job,telphone,work_address,remark,is_main,file,buisness_file)
                try:
                    search_sql = "SELECT * FROM `TianChen` WHERE project_name = '{}';".format(project_name)
                    cursor.execute(search_sql)
                    if len(cursor.fetchall()):
                        update_sql = "UPDATE TianChen SET project_name='{}',project_stage='{}',developer_name='{}',project_type='{}',province='{}',city='{}',project_address='{}',design_stage='{}',build_stage='{}',decorate_stage='{}',is_decorate='{}',has_elevator='{}',has_airconditioner='{}',has_steel='{}',floor_space='{}',investments={},cost={},floor_numbers={},heating_mode='{}',wall_materials='{}',time_start='{}',time_end='{}',need_materials='{}',project_info='{}',contact_name='{}',contact_gen='{}',company_type='{}',company_name='{}',job='{}',telphone='{}',work_address='{}',remark='{}',is_main='{}',file='{}',buisness_file".format(project_name,project_stage,developer_name,project_type,province,city,project_address,design_stage,build_stage,decorate_stage,is_decorate,has_elevator,has_airconditioner,has_steel,floor_space,investments,cost,floor_numbers,heating_mode,wall_materials,time_start,time_end,need_materials,project_info,json.dumps(company_info,ensure_ascii=False),contact_gen,company_type,company_name,job,telphone,work_address,remark,is_main,file,buisness_file)+" WHERE project_name = '{}';".format(project_name)
                        # print(update_sql)
                        cursor.execute(update_sql)
                        db.commit()
                        print(project_name)
                    else:
                        insert_sql = "INSERT INTO TianChen(project_name,project_stage,developer_name,project_type,province,city,project_address,design_stage,build_stage,decorate_stage,is_decorate,has_elevator,has_airconditioner,has_steel,floor_space,investments,cost,floor_numbers,heating_mode,wall_materials,time_start,time_end,need_materials,project_info,contact_name,contact_gen,company_type,company_name,job,telphone,work_address,remark,is_main,file,buisness_file) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},{},{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(project_name,project_stage,developer_name,project_type,province,city,project_address,design_stage,build_stage,decorate_stage,is_decorate,has_elevator,has_airconditioner,has_steel,floor_space,investments,cost,floor_numbers,heating_mode,wall_materials,time_start,time_end,need_materials,project_info,json.dumps(company_info,ensure_ascii=False),contact_gen,company_type,company_name,job,telphone,work_address,remark,is_main,file,buisness_file)
                        cursor.execute(insert_sql)
                        db.commit()
                        print(project_name)

                except Exception as e:
                    db.rollback()
                    print(e)

            except Exception as e:
                url_error.write(company_url.strip()+'\n')
                print(e)

    cursor.close()
    db.close()

get_info()