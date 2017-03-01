import re
from multiprocessing import Pool, Lock
from Tools import get_html


def handle(asin):
    asin = asin.strip()
    try:
        baseurl = "https://www.amazon.ca/dp/[asin]"
        url = baseurl.replace('[asin]', asin)
        print (asin)
        html = get_html.get_html_src(url)
        robot_check = re.findall('<title dir="ltr">Robot Check</title>', html)
        if robot_check:
            lock.acquire()
            captcha_url_file.write(asin + '\n')
            captcha_url_file.flush()
            lock.release()
            print ("robot_check")
        else:
            error404 = re.findall("We're sorry. The Web address you entered is not a functioning page on our site", html)
            if error404:
                lock.acquire()
                not_list_file.write(asin + '\n')
                not_list_file.flush()
                lock.release()
                print ("not exit")
            else:
                buyboxinfo = [asin]
                price = re.findall(r'New <span class="olp-from">from</span> CDN\$ (.*?)\n', html)[0]
                buyboxinfo.append(str(price))
                lock.acquire()
                result_file.write("\t".join(buyboxinfo) + "\n")
                result_file.flush()
                success_asin_file.write(asin + '\n')
                success_asin_file.flush()
                lock.release()
                print ("success")
    except Exception as e:
        print (str(e))
        lock.acquire()
        captcha_url_file.write(asin + '\n')
        captcha_url_file.flush()
        lock.release()
        print ("error: not html")


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
    # global not_crawl_file  # 抓取3次后失败，没有抓取到结果的页面
    global success_asin_file
    global lock, tool

    lock = Lock()
    captcha_url_file = open("./result/not_get", "aw")
    not_list_file = open("./result/not_found.txt", "aw")
    success_asin_file = open("./result/success_asin.txt", "aw")

    titles = ['asin', 'price']

    create_titles(fbainfofile, titles)
    result_file = open(fbainfofile, "aw")

    file_asin = open(asinfile, 'r')
    asins = file_asin.readlines()

    pool = Pool(40)
    pool.map(handle, asins)
    pool.close()
    pool.join()

    file_asin.close()
    result_file.close()
    captcha_url_file.close()
    not_list_file.close()
    success_asin_file.close()

    print ("run over")


if __name__ == '__main__':
    asinfile = './asins.txt'
    buyboxinfofile = './exit_ca111.csv'
    get_fba_buybox(asinfile, buyboxinfofile)  # 抓取buybox数据