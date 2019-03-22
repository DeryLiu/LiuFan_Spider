import boto
import json
from multiprocessing import Lock, Pool

import time

import datetime


class S3():
    """
    用来保存文件到S3的类
    """
    access_key = '*****************'
    secret_key = 'kZG1m+/xDdYsyh/MjziJs/***************'
    bucket_name = 'ebay.media'
    image_bucket_name = 'product-image-keep'  # alibaba-product
    file_size = 100 * 1024 * 1024
    connect = None
    bucket = None

    def __init__(self, access_key=None, secret_key=None, bucket_name=None):
        if access_key and secret_key:
            self.access_key = access_key
            self.secret_key = secret_key

        if bucket_name:
            self.bucket_name = bucket_name

        self.connect = boto.connect_s3(self.access_key, self.secret_key)
        bucket_have = self.connect.lookup(self.bucket_name)
        if bucket_have is None:
            self.connect.create_bucket(self.bucket_name)

        self.bucket = self.connect.get_bucket(self.bucket_name, validate=True)

    def get_file_by_key(self,key_name,file_name):

        file_key = boto.s3.key.Key(self.bucket)
        file_key.key = key_name
        file_key.get_contents_to_filename(file_name)


def donwload_image(file_name):
    url_file = open(file_name).readlines()
    for url in url_file:
        try:
            keys = url.split('net/')[1].replace('\n','')
            # if '-' in keys:
            #     keys= '/'+keys.split('/')[1]
            print (keys)
            save_file = keys.replace('/', '_')
            # time.sleep(15)
            try:
                s3.get_file_by_key(keys, './Image/' + save_file)
                # time.sleep(18)
            except Exception as e:
                print ('[\[\[\[\[\[\[\[')
                print (e)
                with open('./fail_info.txt', 'aw') as fail_url:
                    fail_url.write(json.dumps({'result': str(e), 'url': url}) + '\n')

        except Exception as e:
            print ('-=-=--')
            print (e)
            with open('./fail_info.txt','aw') as fail_url:
                fail_url.write(json.dumps({'result':str(e),'url':url})+'\n')


def save_fail_url():
    text_file = open('./text_url.txt','aw')
    for info_url in open('./fail_info.txt','r').readlines():
        info_url = eval(info_url)
        url= info_url['url']
        text_file.write(url)

if __name__ == '__main__':
    s3 = S3()
    t1 = datetime.datetime.now()
    name = './url.txt'
    # name = './text_url.txt'
    donwload_image(name)
    t2 = datetime.datetime.now()

    # save_fail_url()
    print (t1)
    print (t2)

    # lock = Lock()
    # pool = Pool(10)
    # # 调用函数把items的url依次传入handle函数中爬虫
    # pool.map(make_url())
    # pool.close()
    # pool.join()