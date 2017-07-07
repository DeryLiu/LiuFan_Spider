from bs4 import BeautifulSoup
from DBUtils.PooledDB import PooledDB
import pymysql,re,json

# 图像识别
def read_pic(img, cleanup=True, plus=''):
    import os
    import subprocess
    # cleanup为True则识别完成后删除生成的文本文件
    # plus参数为给tesseract的附加高级参数
    subprocess.check_output('tesseract ' + img + ' ' +
                            img + ' ' + plus, shell=True)  # 生成同名txt文件
    text = ''
    with open(img + '.txt', 'r') as f:
        text = f.read().strip()
    if cleanup:
        os.remove(img + '.txt')
    return text

# print(read_pic('1.png'),False,'-l chi_sim -psm')

def insert_url():
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    cursor=db.cursor()

    with open('text.html','r',encoding='gbk') as sss:
        soup = BeautifulSoup(sss.read(),'html.parser')

        try:
            project_name = soup.select('#param_100100_2 > span')[0].text.split(':')[1].strip()
        except:
            project_name = soup.select('#param_100100_2 > span')[0].text
        try:
            project_stage = soup.select('#param_10001_2')[0].text.strip()
        except:
            project_stage = ''
        # --------
        developer_name = ''
        developer_part = soup.select('#tbc_02 div.line_b')

        company_info = []
        for developer_info in developer_part:
            try:
                # company_section = re.findall('<div class="x_title">(.*?)</div>',str(developer_info),re.S)[0].strip()
                company_section = developer_info.div.text.strip() # 所属公司 类别
                # print(company_section)
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
                    except:
                        contact_telphone = contact_line_info[2].strip().split(' ')[1]
                    # print(contact_telphone)

                    # 联系地址
                    if "(" in contact_line_info[-1]:
                        contact_address = contact_line_info[-1].strip()
                    else:
                        contact_address = contact_line_info[-2].strip()

                    # print(contact_telphone,contact_address)
                    contact_list_info.append({"公司名称":company_name_l,"职位":developer_role,"联系人":contact_name,"性别":contact_genl,"联系电话":contact_telphone})
            except:
                pass
        # print(company_info)

        project_type = soup.select('#param_10009_2')[0].text.strip()
        province = ''
        city = ''
        project_address = soup.select('#param_10061_2')[0].text.strip()
        design_stage = ''
        build_stage = ''
        decorate_stage = ''
        try:
            is_decorate = soup.select('#param_10011_2')[0].text.strip()
        except:
            is_decorate = ''
        has_elevator = ''
        has_airconditioner = ''
        has_steel = soup.select('#param_10106_2')[0].text.strip()
        floor_space = soup.select('#param_10005_2')[0].text.strip()
        try:
            investments = int(soup.select('#param_10033_2')[0].text.strip().split('(')[0]) * 1000000
        except:
            investments = 0
        cost = int(soup.select('#param_10030_2')[0].text.strip().split('(')[0]) * 1000000
        try:
            floor_numbers = int(soup.select('#param_10007_2')[0].text.strip().split('层')[0])
        except:
            floor_numbers = 0
        heating_mode = ''
        wall_materials = ''
        time_start = soup.select('#param_10018_2')[0].text.strip()
        time_end = soup.select('#param_10019_2')[0].text.strip()
        need_materials = 'http://gc.buildnet.cn'+soup.select('tr.line_02 > td > img')[0]['src']
        project_info = soup.select('#param_10017_2')[0].text.strip()
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

        print(project_name,project_stage,developer_name,project_type,province,city,project_address,design_stage,
              build_stage,decorate_stage,is_decorate,has_elevator,has_airconditioner,has_steel,floor_space,investments,
              cost,floor_numbers,heating_mode,wall_materials,time_start,time_end,need_materials,project_info,company_info,
              contact_gen,company_type,company_name,job,telphone,work_address,remark,is_main,file,buisness_file)

    #     try:
    #         insert_sql = "INSERT INTO TianChen(project_name,project_stage,developer_name,project_type,province,city,project_address,design_stage,build_stage,decorate_stage,is_decorate,has_elevator,has_airconditioner,has_steel,floor_space,investments,cost,floor_numbers,heating_mode,wall_materials,time_start,time_end,need_materials,project_info,contact_name,contact_gen,company_type,company_name,job,telphone,work_address,remark,is_main,file,buisness_file) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},{},{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(project_name,project_stage,developer_name,project_type,province,city,project_address,design_stage,build_stage,decorate_stage,is_decorate,has_elevator,has_airconditioner,has_steel,floor_space,investments,cost,floor_numbers,heating_mode,wall_materials,time_start,time_end,need_materials,project_info,json.dumps(company_info,ensure_ascii=False),contact_gen,company_type,company_name,job,telphone,work_address,remark,is_main,file,buisness_file)
    #         cursor.execute(insert_sql)
    #         db.commit()
    #     except Exception as e:
    #         print(e)
    #         db.rollback()
    #
    # cursor.close()
    # db.close()


insert_url()