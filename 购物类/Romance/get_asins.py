import os
from multiprocessing import Pool, Lock
import re
from Tools import get_html


def handle(url):
    try:
        # html = tool.gethtmlproxy(url)
        html = get_html.get_html_src(url)
        if html == '' or -1 != html.find('Sorry, we just need to make sure you'):
            lock.acquire()
            f_fail.write(url + '\t空或验证码\n')
            f_fail.flush()
            lock.release()
            return
        if html == '404 error':
            lock.acquire()
            f_fail.write(url + '\t404 error\n')
            f_fail.flush()
            lock.release()
            return
        if html == 'time out or other errors':
            lock.acquire()
            f_fail.write(url + '\ttime out or other errors\n')
            f_fail.flush()
            lock.release()
            return
        tmp_asins = re.findall(r'data-asin="(.*?)"', html)
        print (tmp_asins)
        if len(tmp_asins) != 0:
            for asin in tmp_asins:
                lock.acquire()
                f_asins.write(asin + '\n')
                f_asins.flush()
                lock.release()
            lock.acquire()
            f_success.write(url + '\n')
            f_success.flush()
            lock.release()
        else:
            lock.acquire()
            f_fail.write(url + '\ttmp_asins为空\n')
            f_fail.flush()
            lock.release()
    except Exception as e:
        print (str(e))


def get_all_page():
    urls = []
    with open('./result/price_url.txt') as f:
        lines = f.readlines()
    for line in lines:
        base_url = line.split('\t')[0]
        count = int(line.split('\t')[1].strip())
        page_count = count / 60
        if count % 60:
            page_count += 1
        total_page = min([page_count, 20])
        for i in range(1, total_page + 1):
            url = base_url + '&page=' + str(i)
            print (url)
            urls.append(url)
    return urls


def get_asins():
    global lock, f_success, f_asins, f_fail, tool
    lock = Lock()
    # tool = httptools.httptools('com')

    urls = get_all_page()

    f_asins = open('./result/asins_more.txt', 'aw')
    f_success = open('./result/success_url.txt', 'aw')
    f_fail = open('./result/fail_url.txt', 'aw')

    pool = Pool(30)
    pool.map(handle, urls)
    pool.close()
    pool.join()

    f_asins.close()
    f_success.close()
    f_fail.close()


if __name__ == '__main__':
    try:
        get_asins()
        os.system('sort -u '+'./result/asins_more.txt'+' > '+'./result/asins.txt')
    #         os.system('nohup python get_isbn_china &')
    except Exception as e:
        print (e)
