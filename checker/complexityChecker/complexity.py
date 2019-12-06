import os

#example of dir = 'd:\mccabe'
#get score of cyclomatic complexity
import sys


def get_score(dir):
    command = 'flake8 --max-complexity 0 ' + dir
    result = os.popen(command)
    info = result.readlines()
    score = 100

    #count of different results
    countAlert = 0
    countNotice9 = 0
    countNotice8 = 0
    countNotice7 = 0
    countNotice6 = 0
    countPass = 0

    for line in info:
        complexity = int(line[-3:-2])

        #count different types of complexity
        if(complexity >= 10):
            countAlert = countAlert + 1
        elif(complexity < 6):
            countPass = countPass + 1
        else:
            if(complexity == 9):
                countNotice9 = countNotice9 + 1
            if (complexity == 8):
                countNotice8 = countNotice8 + 1
            if (complexity == 7):
                countNotice7 = countNotice7 + 1
            if (complexity == 6):
                countNotice6 = countNotice6 + 1
    # calculate score
    if (countAlert > 0):
        score = 0
    else:
        score = 1 - ((2 * countNotice6 + 4 * countNotice7 + 6 * countNotice8 + 8 * countNotice9) /
                     (countNotice6 + countNotice7 + countNotice8 + countNotice9 + countPass))
        if (score < 0):
            score = 0
        score = score * 100
    return round(score, 2)

# get the string for complexity of functions
def get_complexity(dir):
    command = 'flake8 --max-complexity 6 ' + dir
    result = os.popen(command)
    info = result.readlines()
    return info

# count functions with different complexity
def get_funcs_num(dir):
    command = 'flake8 --max-complexity 0 ' + dir
    result = os.popen(command)
    info = result.readlines()

    # count of different results
    countAlert = 0
    countNotice9 = 0
    countNotice8 = 0
    countNotice7 = 0
    countNotice6 = 0
    countPass = 0

    for line in info:
        complexity = int(line[-3:-2])

        # count different types of complexity
        if (complexity >= 10):
            countAlert = countAlert + 1
        elif (complexity < 6):
            countPass = countPass + 1
        else:
            if (complexity == 9):
                countNotice9 = countNotice9 + 1
            if (complexity == 8):
                countNotice8 = countNotice8 + 1
            if (complexity == 7):
                countNotice7 = countNotice7 + 1
            if (complexity == 6):
                countNotice6 = countNotice6 + 1

    return str(countPass) + "," + str(countNotice6+countNotice7+countNotice8+countNotice9) + "," + str(countAlert)

if __name__ == '__main__':
    print(get_complexity(sys.argv[1]))
