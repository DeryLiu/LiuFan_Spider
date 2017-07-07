
'强制性'
'http://www.gb688.cn/bzgk/gb/std_list_type?p.p1=1&p.p90=circulation_date&p.p91=desc'

'推荐性'
'http://www.gb688.cn/bzgk/gb/std_list_type?p.p1=2&p.p90=circulation_date&p.p91=desc'

import requests,re
from bs4 import BeautifulSoup

def download():
    # '强制性 - 91建筑材料和建筑物'
    # url_list = ['http://www.gb688.cn/bzgk/gb/std_list_type?r=0.18888231214251094&page={}&pageSize=10&p.p1=1&p.p6=91&p.p90=circulation_date&p.p91=desc'.format(i) for i in range(1,14)]
    '推荐性 - 91建筑材料和建筑物'
    url_list = ['http://www.gb688.cn/bzgk/gb/std_list_type?r=0.13757189409190085&page={}&pageSize=10&p.p1=2&p.p6=91&p.p90=circulation_date&p.p91=desc'.format(i) for i in range(1,24)]
    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        standnum_list = soup.select('div.table-responsive > table > tbody > tr > td:nth-of-type(2) > a')
        caiBiao_list = soup.select('div.table-responsive > table > tbody > tr > td:nth-of-type(3)')
        stand_name_list = soup.select('div.table-responsive > table > tbody > tr > td:nth-of-type(4)')
        zhuangTai_list = soup.select('div.table-responsive > table > tbody > tr > td:nth-of-type(5) > span')
        start_data_list = soup.select('div.table-responsive > table > tbody > tr > td:nth-of-type(6)')
        end_data_list = soup.select('div.table-responsive > table > tbody > tr > td:nth-of-type(7)')

        for num in range(len(standnum_list)):
            standNum = standnum_list[num].text.strip()
            standId = re.findall("'(.*?)'",str(standnum_list[num]['onclick']),re.S)[0]
            if '\n' == re.findall("<td>(.*?)</td>",str(caiBiao_list[num]),re.S)[0]:
                caiOrNot = '空'
            else:
                caiOrNot = '采'
            standName = stand_name_list[num].text.strip()
            zhuangTai = zhuangTai_list[num].text.strip()
            start_data = start_data_list[num].text.strip()
            end_data = end_data_list[num].text.strip()

            file_name = standNum+'_'+standId+'_'+caiOrNot+'_'+standName+'_'+zhuangTai+'_'+start_data+'_'+end_data
            download_url = 'http://c.gb688.cn/bzgk/gb/viewGb?hcno={}'.format(standId)
            download_response = requests.get(download_url)
            try:
                with open(file_name+'.pdf','wb') as ssss:
                    ssss.write(download_response.content)
                    print(standNum,standId,caiOrNot,standName,zhuangTai,start_data,end_data)
            except Exception as e:
                print(e)

'强制性 - 91建筑材料和建筑物'
'http://www.gb688.cn/bzgk/gb/std_list_type?r=0.18888231214251094&page=2&pageSize=10&p.p1=1&p.p6=91&p.p90=circulation_date&p.p91=desc'

'推荐性 - 91建筑材料和建筑物'

'下载标准'
'http://c.gb688.cn/bzgk/gb/showGb?type=download&hcno=46BF4615143C8F26BD804F767E43C280'
'下载地址'
'http://c.gb688.cn/bzgk/gb/viewGb?hcno=46BF4615143C8F26BD804F767E43C280'

download()


with open('text.html','r') as text_file:
    soup = BeautifulSoup(text_file,'html.parser')
    standnum_list = soup.select('div.table-responsive > table > tbody > tr > td:nth-of-type(2) > a')
    caiBiao_list = soup.select('div.table-responsive > table > tbody > tr > td:nth-of-type(3)')
    stand_name_list = soup.select('div.table-responsive > table > tbody > tr > td:nth-of-type(4)')
    zhuangTai_list = soup.select('div.table-responsive > table > tbody > tr > td:nth-of-type(5) > span')
    start_data_list = soup.select('div.table-responsive > table > tbody > tr > td:nth-of-type(6)')
    end_data_list = soup.select('div.table-responsive > table > tbody > tr > td:nth-of-type(7)')

    for num in range(len(standnum_list)):
        standNum = standnum_list[num].text.strip()
        standId = re.findall("'(.*?)'",str(standnum_list[num]['onclick']),re.S)[0]
        if '\n' == re.findall("<td>(.*?)</td>",str(caiBiao_list[num]),re.S)[0]:
            caiOrNot = '空'
        else:
            caiOrNot = '采'
        standName = stand_name_list[num].text.strip()
        zhuangTai = zhuangTai_list[num].text.strip()
        start_data = start_data_list[num].text.strip()
        end_data = end_data_list[num].text.strip()
        download_url = 'http://c.gb688.cn/bzgk/gb/viewGb?hcno={}'.format(standId)
        # print(download_url)
        # print(standNum,standId,caiOrNot,standName,zhuangTai,start_data,end_data)
        print('done')

