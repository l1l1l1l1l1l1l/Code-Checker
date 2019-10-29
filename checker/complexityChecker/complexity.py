import os

#def of colors
PASS = '\033[0;32m'
#NOTICE = '\033[0;33;40m'
NOTICE = '\033[0;33m'
ALERT = '\033[0;31m'
ENDSIG = '\033[0m'

#example of dir = 'd:\mccabe'
def flake8(dir):
    command = 'flake8 --max-complexity 1 ' + dir
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
            print(ALERT + 'ALERT(' + str(countAlert) + ')')
            print('\t' + line + ENDSIG)
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
            printNotice(line, countNotice6, countNotice7, countNotice8, countNotice9)

    # print result
    print(ALERT + 'ALERT(' + str(countAlert) + ')' + ENDSIG + '\t' +
          NOTICE + 'NOTICE(' + countNotice(countNotice6, countNotice7, countNotice8,countNotice9) + ')' + ENDSIG + '\t' +
          PASS + 'PASS(' + str(countPass) + ')' + ENDSIG + '\t')

    # calculate score
    if (countAlert > 0):
        score = 0
    else:
        score = 1 - ((0.50 * countNotice6 + 0.70 * countNotice7 + 0.85 * countNotice8 + 1 * countNotice9) /
                     (countNotice6 + countNotice7 + countNotice8 + countNotice9 + countPass))
        score = score * 100
    return int(score)

def countNotice(count6, count7, count8, count9):
    count = count6 + count7 + count8 + count9
    return str(count)

def printNotice(line, count6, count7, count8, count9):
    print(NOTICE + 'NOTICE(' + countNotice(count6, count7, count8, count9) + ')')
    print('\t' + line + ENDSIG)
