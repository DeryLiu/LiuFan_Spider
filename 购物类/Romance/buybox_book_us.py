import re
from multiprocessing import Pool, Lock

from Tools import get_html

regex_sub_info = re.compile('[\t\n]*', re.S)


def handle(asin):
    asin = asin.strip()
    try:
        baseurl = "http://www.amazon.com/gp/offer-listing/[asin]/ref=olp_f_primeEligible?ie=UTF8&f_new=true&f_primeEligible=true"
        url = baseurl.replace('[asin]', asin)

        # html = tool.gethtmlproxy(url)
        html = get_html.get_html_src(url)
        print ('handling...')
        # 验证码页面
        if html == '' or -1 != html.find('Sorry, we just need to make sure you'):
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

        author = re.search('<div id="olpProductByline" class="a-section a-spacing-mini">\s+by (.*?)\s+</div>', html,
                           re.S)
        if author:
            author = author.group(1).strip()
        else:
            author = ''
        buyboxinfo.append(regex_sub_info.sub(str(author), ''))

        price_list = re.findall(
            '<span class="a-size-large a-color-price olpOfferPrice a-text-bold">\s+\$(.*?)\s+</span>', html)
        if price_list:
            for i in range(len(price_list)):
                price = price_list[i].strip().replace(',', '')
                price_list[i] = float(price)
            min_price = min(price_list)
            fbastatus = 'FBA'
        else:
            min_price = ''
            fbastatus = 'FBM'
        buyboxinfo.append(regex_sub_info.sub(str(min_price), ''))
        buyboxinfo.append(regex_sub_info.sub(str(fbastatus), ''))
        print (buyboxinfo)

        lock.acquire()
        result_file.write("\t".join(buyboxinfo) + "\n")
        result_file.flush()
        success_asin_file.write(asin.strip() + '\n')
        success_asin_file.flush()
        lock.release()
    except Exception as e:
        print (asin, e)


def create_titles(filename, titles):
    f = open(filename, "w")
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
    captcha_url_file = open("./result/captcha_url.txt", "w")
    not_list_file = open("./result/not_found.txt", "w")
    not_crawl_file = open("./result/not_crawl.txt", "w")
    success_asin_file = open("./result/success_asin.txt", "w")

    #     titles = ['asin','ISBN-10','ISBN-13','reviews','brand','price','shipping_price','fba_lowest_price','fba_status','title','sellers_new','sellers_used','department','seller','sales_rank_num','cate1','cate2','cate3','img_list']
    titles = ['asin', 'author', 'price', 'fba_status']

    create_titles(fbainfofile, titles)
    result_file = open(fbainfofile, "aw")

    #     try:
    file_asin = open(asinfile, 'r')
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
    buyboxinfofile = './result/buybox11111.csv'
    get_fba_buybox(asinfile, buyboxinfofile)  # 抓取buybox数据
