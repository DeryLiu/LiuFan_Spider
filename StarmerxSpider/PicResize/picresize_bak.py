#!/usr/bin/env python
# coding=utf-8

import gl
from PIL import Image
import urllib2
import os
import random
from S3 import S3
import multiprocessing
from multiprocessing import Pool, Lock

global pool, lock
lock = Lock()



"""
    :param file_name_list:需要合并的图片的路径列表
    :param output_file_name:合并后的图片名称
    :param backgroud_color:
    :return:合并后的图片的路径
"""


class HttpTools:
    def __init__(self):
        self.head = {}
        self.head['User-Agent'] = random.choice(gl.USER_AGENT)
        self.error = open(gl.ERROR_DIR+gl.ERROR_FILE,"a")


    def get_request(self,url):
        try:
            req=urllib2.Request(url,None,self.head)
        except Exception ,e:
            print e
            self.error.write(url+"\n")
            return False
        return req

    def get_request_proxy(self,url):
        try:
            print random.choice(gl.PROXY_IP)
            proxy_support = urllib2.ProxyHandler({'http':'http://'+random.choice(gl.PROXY_IP)})
            opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)            
            urllib2.install_opener(opener)
            req=urllib2.Request(url,None,self.head)
        except Exception ,e:
            print e
            return self.get_request(url)
        return req

    def __del__(self):
        self.error.close()



class PicHandle:
    def __init__(self,imgurl):
        self.error_file = open(gl.ERROR_DIR+gl.ERROR_FILE,"a")
        self.s3_list_file = open('./s3_list.txt', 'a')
        self.image_list_file = open('./image_list.txt', 'a')

        self.imgurl = imgurl.strip()
        self.image_dic = {}
        self.request = HttpTools()
        self.pic_filename=gl.INPUT_DIR + self.imgurl.replace("/","_")+".jpg"
        self.merge_output=gl.OUTPUT_DIR+ self.imgurl.replace("/","_")+".jpg"
        # self.run(self.imgurl)

    def get_pic(self):

        req = self.request.get_request(self.imgurl)

        if req:
            try:
                res = urllib2.urlopen(req,timeout=10)
                content = res.read()
                with open(self.pic_filename, 'wb') as f:
                    f.write(content)
                print "write success!",self.pic_filename
                return True
            except Exception , e:
                print e
                self.error_file.write(self.imgurl+"\n")
                return False
        return False




    def get_pic_proxy(self):
        req = self.request.get_request_proxy(self.imgurl)
        if req:
            try:
                res = urllib2.urlopen(req,timeout=10)
                content = res.read()
                with open(self.pic_filename, 'wb') as f:
                    f.write(content)
                print "Write Success!\n",self.pic_filename
                return True
            except Exception , e:
                print e
                self.error_file.write(self.imgurl+"\n")
                return False
        return False



    def upload_pic(self):
        s3 = S3()
        try:
            # lock.acquire()
            print "Start Upload",self.merge_output
            S3list = s3.upload_image_list(str(self.image_dic))
            print "Done Upload",self.merge_output
            print S3list
            # lock.release()
            lock.acquire()
            self.s3_list_file.write(str(S3list) + '\n')
            self.s3_list_file.flush()
            lock.release()
        except Exception ,e:
            lock.acquire()
            print "Upload Error. %s " % e
            self.error_file.write(str(url) + '\n')
            self.error_file.flush()
            lock.release()
            return False



    def resize(self,w, h, w_box, h_box, pil_image):
        try:
            backresize = pil_image.resize((w_box, h_box), Image.ANTIALIAS)
        except Exception, e:
            print "resize Error, %s" % e
            return pil_image
        return backresize

    def merge_thumb(self,file_name, url, output_file_name=None, backgroud_color='white'):

        file_name = file_name
        try:
            img = Image.open(file_name)
            temp_width, temp_height = img.size
        except Exception, e:
            lock.acquire()
            print "Img Open :Image File Error. %s " % e
            self.error_file.write(str(url) + '\n')
            self.error_file.flush()
            lock.release()
            return False
        temp_width, temp_height = img.size
        if temp_width > temp_height:
            if temp_height >= 900:
                every_height = temp_height
                every_width = temp_width
            elif temp_height <= 300:
                every_height = int(2.0 * temp_height)
                every_width = int(2.0 * temp_width)
            else:
                every_height = 900
                every_width = int((every_height * temp_width) / temp_height)
        else:
            if temp_width >= 900:
                every_width, every_height = temp_width, temp_height
            elif temp_width <= 300:
                every_height = int(2.0 * temp_height)
                every_width = int(2.0 * temp_width)
            else:
                every_width = 900
                every_height = int((every_width * temp_height) / temp_width)
        # 如果要将图片也放大成比例
        merge_width, merge_height = 25, 25
        width, height = every_width + 50, every_height + 50
        if width < 1001 or height < 1001:
            width = 1001
            height = 1001
            merge_width = (width - every_width) / 2
            merge_height = (height - every_height) / 2
        # 新建一个白色底的图片
        # width=1000
        # height=1000
        merge_img = Image.new('RGB', (width, height), backgroud_color)
        img_resize = self.resize(temp_width, temp_height, every_width, every_height, img)
        merge_img.paste(img_resize, (merge_width, merge_height))


        # 图片不放大，只是加个白底，图片放中间
        # img_resize = resize(temp_width, temp_height, temp_width, temp_height, img)
        # merge_width =  (every_with/2) - (temp_width/2)
        # merge_height =  (every_height/2) - (temp_height/2)
        # merge_img.paste(img_resize, (merge_width, merge_height))

        # if not output_file_name:
        #     import os
        #     if not os.path.exists("merge"): os.mkdir("merge")
        #     output_file_name = os.path.join("merge", file_name_list[0])

        try:
            lock.acquire()
            merge_img.save(output_file_name)
            lock.release()
        except Exception, e:
            lock.acquire()
            print "not img save , %s " % e
            self.error_file.write(str(url) + '\n')
            self.error_file.flush()
            lock.release()
            return False
        self.image_dic = {'filename': output_file_name, "source_url": url}
        lock.acquire()
        self.image_list_file.write(str(self.image_dic) + '\n')
        self.image_list_file.flush()
        lock.release()
        print 'Resize Pic Success!'
        return True

    def run(self):
        get_flag = self.get_pic()
        if get_flag:
            merge_flag = self.merge_thumb(self.pic_filename, self.imgurl, self.merge_output, 'white')
            if merge_flag:
                self.upload_pic()


    def __del__(self):
        self.error_file.close()
        self.s3_list_file.close()
        self.image_list_file.close()
        try:
            os.remove(self.pic_filename)
            os.remove(self.merge_output)
        except Exception,e:
            print e

def check_path():
    if not os.path.exists("output"):
        os.mkdir("output")
    if not os.path.exists("input"):
        os.mkdir("input")
    if not os.path.exists("error"):
        os.mkdir("error")


def get_urls():
    try:
        picture_file = open(gl.URLS_FILE, 'r')
        pic_urls = picture_file.readlines()
        picture_file.close()
    except Exception, e:
        print e
        import sys
        sys.exit(1)
    return pic_urls


def task(imgurl):
    try:
        pichandle = PicHandle(imgurl)
        pichandle.run()
        return
    except Exception , e:
        print e
        return


def run():
    cpu_count = multiprocessing.cpu_count()

    with open(gl.URLS_FILE) as f:
        img_urls = set()
        for l in f:
            img_urls.add(l)
            if len(img_urls) > gl.URLS_LIMIT:
                print 'Dealing with %s image urls' % gl.URLS_LIMIT
                task_pool = Pool(cpu_count + 2)
                task_pool.map(task, list(img_urls))
                task_pool.close()
                task_pool.join()
                img_urls.clear()
        else:
            print 'Dealing with rest %s image urls' % len(img_urls)
            task_pool = Pool(cpu_count + 2)
            task_pool.map(task, list(img_urls))
            task_pool.close()
            task_pool.join()
    print "\nDone!\n"


if __name__ == "__main__":
    check_path()
    run()
