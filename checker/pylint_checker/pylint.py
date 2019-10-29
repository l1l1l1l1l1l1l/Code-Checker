# -*- coding: utf-8 -*-
# @Time    : 2019/10/22 22:33
# @Author  : LIU YUE
# @File    : pylint.py.py

import os


# get all python files in the test dir
def get_py_files(testDir, fileType, fileNames):
    for root, dirs, files in os.walk(testDir):
        for filename in files:
            file_type = filename.split('.')[-1]
            if file_type == fileType:
                fileNames.append(os.path.join(root, filename))
        if len(dirs) != 0:
            for j in range(len(dirs)):
                get_py_files(dirs[j], fileType, fileNames)
    return fileNames


# 调用命令行得到结果, 入参filename是带完整目录的
def comm(filename):
    command = 'pylint ' + filename
    result = os.popen(command)
    info = result.readlines()
    print("{}的pylint结果：".format(filename))
    for line in info:  # 按行遍历
        line = line.strip('\r\n')
        # print(line)
        if line.startswith('Your code has been rated at'):
            grade = line[28: 32]
    return grade
