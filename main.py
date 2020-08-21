# coding=utf-8

import os
import re
import zipfile

from multiprocessing import Pool


# jar文件所在目录
TARGET = "D:/WEB-INF/lib"
# 反编译输出文件
DESTINATION = "D:/src/"

ret = set()


def get_all_file_from_dir(path_dir):

    if os.path.exists(path_dir):
        path_dir = os.path.abspath(path_dir)
        for i in os.listdir(path_dir):
            path_i = os.path.join(path_dir, i)
            if os.path.isfile(path_i) and not os.path.isdir(path_i):
                if re.search('.jar$', path_i):
                    ret.add(path_i)
            else:
                get_all_file_from_dir(path_i)


def unzip(filename, target_path):
    print("Unzip %s to %s" % (filename, target_path))
    file_zip = zipfile.ZipFile(filename, 'r')
    for file in file_zip.namelist():
        file_zip.extract(file, target_path)
    file_zip.close()
    os.remove(filename)


def task(target_jar):
    jar_name = os.path.basename(target_jar)
    target_path = DESTINATION + "/%s" % jar_name.replace('.jar', '')
    print('Run child process %s (%s)...' % (target_jar, os.getpid()))
    exec_file = "jd-cli.jar"
    cmd = "java -jar %s -od %s %s" % (exec_file, target_path, target_jar)
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    get_all_file_from_dir(TARGET)
    jar_list = list(ret)
    print jar_list
    p = Pool(3)
    for jar in jar_list:
        p.apply_async(task, args=(jar,))
    print("Waiting for all subprocess done...")
    p.close()
    p.join()
    print("All work done!")



