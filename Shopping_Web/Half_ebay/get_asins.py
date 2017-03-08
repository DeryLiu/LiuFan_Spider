from Tools.util import httptools
import sys
import re, os
from multiprocessing import Pool, Lock
import datetime
import logging.config
from fileinput import filename

def handle(url):
    try:
        html = tool.gethtmlproxy(url)
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
        print (e)


# logger2.error(url + '\t' + str(e))

def get_all_page(filename):
    urls = []
    with open(filename) as f:
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


def get_asins(dir_name='./result'):
    global lock, f_success, f_asins, f_fail, tool
    lock = Lock()
    tool = httptools.httptools('com')

    filename = dir_name + '/price_url.txt'
    urls = get_all_page(filename)

    f_asins = open(dir_name + '/asins_more.txt', 'w')
    f_success = open(dir_name + '/success_url.txt', 'w')
    f_fail = open(dir_name + '/fail_url.txt', 'w')

    pool = Pool(5)
    pool.map(handle, urls)
    pool.close()
    pool.join()
    #     for url in urls:
    #         handle(url)

    f_asins.close()
    f_success.close()
    f_fail.close()


if __name__ == '__main__':
    try:
        dir_name = './result'
        if sys.argv[1]:
            dir_name = sys.argv[1]
        print (dir_name)
        t1 = datetime.datetime.now()
        #         logger1.info('start get_asins...')
        get_asins(dir_name)
        #         logger1.info('over get_asins')
        #         os.system('sort -u '+'./result/asins_more.txt'+' > '+'./result/asins.txt')
        #         os.system('nohup python get_isbn_china &')
        t2 = datetime.datetime.now()
        print ('开始时间：', t1)
        print ('结束时间：', t2)
    except Exception as e:
        print (e)
# logger2.error(str(e))


