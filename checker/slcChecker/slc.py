# -*- coding: utf-8 -*-
# @Time    : 2019/10/22 22:28
# @Author  : LIU YUE
# @File    : slc.py

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


# calculate source lines of code
def calculate_slo(filename):
    source_lines = 0
    annotation_lines = 0
    for line in open(filename).readlines():
        if line != '' and line != '\n':
            source_lines += 1
        if line.startswith('#'):
            annotation_lines += 1
    # print('{}-----slc={},alc={}'.format(filename, source_lines, annotation_lines))
    return source_lines, annotation_lines


# define the parameters
def slc(testDir):
    fileType = 'py'
    fileNames = []
    fileNames = get_py_files(testDir, fileType, fileNames)
    slc = 0
    for i in range(len(fileNames)):
        source_lines, annotation_lines = calculate_slo(fileNames[i])
        # result[i] = '{}-----slc={},alc={}'.format(fileNames[i], source_lines, annotation_lines)
        slc = slc + source_lines
    return slc
