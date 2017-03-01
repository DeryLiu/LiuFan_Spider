import re
from multiprocessing import Pool, Lock
import time
from Tools import get_html


regex_sub_info = re.compile('[\t\n]*', re.S)


def handle(asin):
    asin = asin.strip()
    # time.sleep(3)
    try:
        baseurl = "https://www.amazon.com/dp/[asin]"
        url = baseurl.replace('[asin]', asin)
        # time.sleep(30)
        html = get_html.get_html_src(url)
        print ('handling...')
        # 验证码页面
        if html == '' or -1 != html.find('Sorry, we just need to make sure you'):
            # time.sleep(180)
            lock.acquire()
            captcha_url_file.write(asin + '\n')
            captcha_url_file.flush()
            lock.release()
            return
        # 下架产品
        if html == '404 error':
            lock.acquire()
            not_list_file.write(asin + '\n')
            not_list_file.flush()
            lock.release()
            # print 'product not found'
            return
        # 没有抓下来的页面
        if html == 'time out or other errors':
            lock.acquire()
            not_crawl_file.write(asin + '\n')
            not_crawl_file.flush()
            lock.release()
            return

        buyboxinfo = []
        buyboxinfo.append(asin)

        stock = re.search('<span class="a-size-medium a-color-success">\s+(.*?)\.', html, re.S)
        if stock:
            stock = stock.group(1)
        else:
            stock = re.search('<span class="a-size-base a-color-state">\s+(.*?)\.', html, re.S)
            if stock:
                stock = stock.group(1)
            else:
                stock = re.search('<span class="a-color-success a-text-bold">\s+(.*?)\.', html, re.S)
                if stock:
                    stock = stock.group(1)
                else:
                    stock = re.search('<span class="a-size-medium a-color-price">\s+(.*?)\.', html, re.S)
                    if stock:
                        stock = stock.group(1)
                    else:
                        stock = ''
        buyboxinfo.append(regex_sub_info.sub(str(stock), ''))

        print (buyboxinfo)

        lock.acquire()
        result_file.write("\t".join(buyboxinfo) + "\n")
        result_file.flush()
        success_asin_file.write(asin + '\n')
        success_asin_file.flush()
        lock.release()
    except Exception as e:
        print (asin, e)


def create_titles(filename, titles):
    f = open(filename, "aw")
    f.write("\t".join(titles) + "\n")
    f.flush()
    f.close()


def get_fba_buybox(asinfile, fbainfofile):
    print ("run start...")
    global result_file  # 结果文件
    global captcha_url_file  # yan zheng ma ye mian
    global not_list_file  # yi xia jia ye mian
    global not_crawl_file  # 抓取3次后失败，没有抓取到结果的页面
    global success_asin_file
    global lock, tool

    lock = Lock()
    # tool = httptools.httptools('com')
    captcha_url_file = open("./result/captcha_url.txt", "aw")
    not_list_file = open("./result/not_found.txt", "aw")
    not_crawl_file = open("./result/not_crawl.txt", "aw")
    success_asin_file = open("./result/success_asin.txt", "aw")

    # titles = ['asin', 'state']

    # create_titles(fbainfofile, titles)
    result_file = open(fbainfofile, "aw")
    file_asin = open(asinfile, 'r')

    #     try:
    #     except Exception, e:
    #         print e
    asins = file_asin.readlines()

    pool = Pool(30)
    pool.map(handle, asins)
    pool.close()
    pool.join()

    file_asin.close()
    result_file.close()
    captcha_url_file.close()
    not_list_file.close()
    not_crawl_file.close()
    success_asin_file.close()

    print ("run over")


if __name__ == '__main__':
    asinfile = './asins.txt'
    buyboxinfofile = './buybox3.csv'
    get_fba_buybox(asinfile, buyboxinfofile)  # 抓取buybox数据
