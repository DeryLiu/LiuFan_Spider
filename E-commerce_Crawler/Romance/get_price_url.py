from multiprocessing import Pool, Lock
import re
from Tools import get_html


def get_count(price_range, url):  # 没有解析出count的url记录下来。
    try:
        html = get_html.get_html_src(url)
        if html == '' or -1 != html.find('Sorry, we just need to make sure you'):
            lock.acquire()
            captcha_url_file.write(url + '\n')
            captcha_url_file.flush()
            lock.release()
            return
        if html == '404 error':
            lock.acquire()
            not_list_file.write(url + '\n')
            not_list_file.flush()
            lock.release()
            # print 'product not found'
            return
        # 没有抓下来的页面
        if html == 'time out or other errors':
            lock.acquire()
            not_crawl_file.write(price_range + '\n')
            not_crawl_file.flush()
            lock.release()
            return
        num = re.search('<h2 id="s-result-count".*?>1-60 of (.*?) result', html)
        if num == None:
            num = re.search('<h2 id="s-result-count".*?>(.*?) result', html)

        if num != None:
            num = int(num.group(1).replace(',', ''))
            return num
        else:
            if 'did not match any products.' in html:
                lock.acquire()
                f_no_product.write(url + '\n')
                f_no_product.flush()
                lock.release()
            else:
                with open('get_count_fail.txt', 'aw') as f:
                    f.write(price_range + '\n')
            return
    except Exception as e:
        print (str(e))


def dichotomy(price_range):
    # print price_range
    try:
        # base_url = "https://www.amazon.com/s/ref=sr_nr_n_24?fst=as%3Aoff&rh=n%3A283155%2Cp_n_feature_nine_browse-bin%3A3291437011%2Cp_85%3A2470955011%2Cp_n_condition-type%3A1294423011%2Cp_n_availability%3A2245265011%2Cn%3A!1000%2Cn%3A23%2Cp_36%3A[price_range]&bbn=1000&ie=UTF8&qid=1467165535&rnid=1000&lo=stripbooks"
        base_url = 'https://www.amazon.com/s/ref=sr_nr_n_2?fst=as%3Aoff&rh=n%3A283155%2Cp_n_feature_nine_browse-bin%3A3291437011%2Cp_85%3A2470955011%2Cp_n_condition-type%3A1294423011%2Cp_n_availability%3A2245265011%2Cn%3A!1000%2Cn%3A3%2Cp_36%3A[price_range]&bbn=1000&ie=UTF8&qid=1477277123&rnid=1000&lo=stripbooks'
        url = base_url.replace('[price_range]', price_range)
        count = get_count(price_range, url)
        if count == None:
            return
        if count <= 1200:
            lock.acquire()
            f_price_url.write(url + '\t' + str(count) + '\n')
            f_price_url.flush()
            lock.release()
            print (price_range, ':', count)
        else:
            low = int(price_range.split('-')[0])
            high = int(price_range.split('-')[1])
            mid = (low + high) / 2

            price_range_low = str(low) + '-' + str(mid)
            url_low = base_url.replace('[price_range]', price_range_low)
            count_low = get_count(price_range_low, url_low)
            if count_low == None:
                return
            if count_low <= 1200:
                lock.acquire()
                f_price_url.write(url_low + '\t' + str(count_low) + '\n')
                f_price_url.flush()
                lock.release()
                print (price_range_low, ':', count_low)
            else:
                if mid - low == 1:
                    lock.acquire()
                    f_price_url.write(url_low + '\t' + str(count_low) + '\n')
                    f_price_url.flush()
                    lock.release()
                    print (price_range_low, ':', count_low)
                else:
                    dichotomy(price_range_low)

            price_range_high = str(mid) + '-' + str(high)
            url_high = base_url.replace('[price_range]', price_range_high)
            count_high = get_count(price_range_high, url_high)
            if count_high == None:
                return
            if count_high <= 1200:
                lock.acquire()
                f_price_url.write(url_high + '\t' + str(count_high) + '\n')
                f_price_url.flush()
                lock.release()
                print (price_range_high, ':', count_high)
            else:
                if high - mid == 1:
                    lock.acquire()
                    f_price_url.write(url_high + '\t' + str(count_high) + '\n')
                    f_price_url.flush()
                    lock.release()
                    print (price_range_high, ':', count_high)
                else:
                    dichotomy(price_range_high)
    except Exception as e:
        print (str(e))


def handle_url(price_range):
    try:
        dichotomy(price_range)
    except Exception as e:
        print (str(e))


def get_price_url(high_price):
    global f_price_url, f_no_product, captcha_url_file, not_list_file, not_crawl_file, lock
    lock = Lock()

    number = high_price / 50 + 1
    # print number
    price_ranges = []
    for i in range(number):
        low = i * 50
        high = (i + 1) * 50
        price_range = str(low) + '-' + str(high)
        price_ranges.append(price_range)
        # print price_range
    # print price_ranges

    f_price_url = open('./result/price_url.txt', 'w')
    f_no_product = open('./result/no_product.txt', 'w')
    captcha_url_file = open('./result/captcha_url.txt', 'w')
    not_list_file = open('./result/not_found.txt', 'w')
    not_crawl_file = open('./result/not_crawl.txt', 'w')

    pool = Pool(30)
    pool.map(handle_url, price_ranges)
    pool.close()
    pool.join()

    f_price_url.close()
    f_no_product.close()
    captcha_url_file.close()
    not_list_file.close()
    not_crawl_file.close()


if __name__ == '__main__':
    get_price_url(20000)
    # "20000-1083309" 803