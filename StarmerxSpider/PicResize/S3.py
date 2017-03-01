#!/usr/bin/env python
# encoding:utf-8

import boto
import hashlib
import os
import hashlib
import math

from filechunkio import FileChunkIO   #需要安装filechunkio模块


class S3():
    """
    用来保存文件到S3的类
    """

    access_key = 'AKIAJQH5XY2NHA3SBQNA'
    secret_key = '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'
    bucket_name = 'product_url-hmtl-backup'
    image_bucket_name = 'product_url-image-keep' #alibaba-product_url
    file_size = 100 * 1024 *1024
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

    def upload_image_list(self, image_list, policy='public-read'):
        """
        :param file_name:文件名列表
        :param policy: 文件访问权限
        :return:返回文件名的上传状态
        """
        print "upload_image_list ..."
        return_list = []
        #image_list = image_list.readlines()
        #for file_dict in image_list:
        file_dict = eval(image_list)
        file_name = file_dict.get("filename", "")
        source_url = file_dict.get("source_url", "")
        if not file_name:
            return return_list
        file_name_tran = self.tran_file_name(source_url)
        file_size = os.stat(file_name).st_size

        file_key = boto.s3.key.Key(self.bucket)
        file_key.key = file_name_tran

        tran_size = file_key.set_contents_from_filename(file_name, policy=policy)
        if tran_size == file_size:
            return_url = 'https://s3.amazonaws.com/' + str(self.bucket_name) +"/" + file_name_tran
            return_list.append({'status' : True, 'source_url': source_url, 'cate_url' : return_url, 'file' : file_name, 'file_key' : file_name_tran})
        else:
            return_list.append({'status' : False, 'source_url': source_url, 'file' : file_name})
        return return_list


    def upload_file_no_split(self, file_name_list, policy='public-read'):
        """
        :param file_name:文件名列表
        :param policy: 文件访问权限
        :return:返回文件名的上传状态
        """

        return_list = []

        for file_name in file_name_list:
            #file_name_tran = self.tran_file_name(file_name)
            file_name_tran = file_name
            file_size = os.stat(file_name).st_size

            file_key = boto.s3.key.Key(self.bucket)
            file_key.key = file_name_tran

            tran_size = file_key.set_contents_from_filename(file_name, policy='public-read')
            if tran_size == file_size:
                return_url = 'https://s3.amazonaws.com/' + str(self.bucket_name) + file_name_tran
                return_list.append({'status' : True, 'cate_url' : return_url, 'file' : file_name, 'file_key' : file_name_tran})
            else:
                return_list.append({'status' : False, 'file' : file_name})
        return return_list

    @staticmethod
    def tran_file_name(file_name):
        """
        :param file_name: 传入的文件名
        :return:传入到s3的key的值
        """

        file_name_tran = hashlib.md5(file_name).hexdigest() + ".jpg"
        return file_name_tran

    def upload_file(self, file_name):
        """
        :param file_name:需要上传的文件
        :return:返回结果
        """
        try:
            file_name_tran = self.tran_file_name(file_name)
            file_size = os.stat(file_name).st_size
            chunk_count = int(math.ceil(file_size / float(self.file_size)))
            print 'upload file:',file_name, ',size:',file_size, ',total_count:',chunk_count

            mp = self.bucket.initiate_multipart_upload(file_name_tran)
            for i in range(chunk_count):
                offset = self.file_size * i
                bytes = min(self.file_size, file_size - offset)
                with FileChunkIO(file_name, 'r', offset=offset, bytes=bytes) as fp:
                    mp.upload_part_from_file(fp, part_num=i + 1)
            mp.complete_upload()
            return {'leaf_category_urls' : True, 'file_key' : file_name_tran, 'file' : file_name}
        except Exception as e:
            print "Error: %s" % e
            return {'leaf_category_urls' : False, 'file' : file_name}

    def upload_files(self, files):
        return_list = []
        for filename in files:
            file_upload = self.upload_file(filename)
            with open('upload_history.csv', 'a') as temp_upload_file:
                temp_upload_file.write(str(file_upload) + '\n')
            return_list.append(file_upload)
        return return_list

    def delete_keys(self, keys):
        try:
            delete_keys_obj = self.bucket.delete_keys(keys=keys)
        except Exception as e:
            print 'Error when delte keys:', str(e)


if __name__ == "__main__":
    s3 = S3()

    s3.upload_image_list()
