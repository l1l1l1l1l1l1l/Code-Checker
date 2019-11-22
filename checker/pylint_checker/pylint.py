# -*- coding: utf-8 -*-
# @Time    : 2019/10/22 22:33
# @Author  : LIU YUE
# @File    : pylint.py

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


# call command to get result
def comm(filename):
    command = 'pylint ' + filename
    result = os.popen(command)
    info = result.readlines()
    grade = 0
    for line in info:
        line = line.strip('\r\n')
        # print(line)
        if line.startswith('Your code has been rated at'):
            grade = float(line[28: 32])
    return info, grade


# define the parameters
def pylint(testDir):
    fileType = 'py'
    fileNames = []
    fileNames = get_py_files(testDir, fileType, fileNames)
    grade_all = 0
    py_result = []
    for i in range(len(fileNames)):
        result, grade = comm(fileNames[i])
        py_result.append(result)
        grade_all = grade_all + grade
    # np.savetxt('PylintResult.txt',py_result)
    return grade_all/len(fileNames), py_result
