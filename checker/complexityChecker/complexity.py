import os

#example of dir = 'd:\mccabe'
def flake8(dir):
    command = 'flake8 --max-complexity 6 ' + dir
    result = os.popen(command)
    info = result.readlines()
    score = 100
    for line in info:
        print(line)
        complexity = int(line[-3:-2])
        if(score != 0 and complexity >=10):
            score = 0
        elif(score > 90 and complexity == 6):
            if (score - 3 > 90):
                score = score - 3
            else:
                score = 90
        elif(score > 80 and complexity == 7):
            if (score - 3 > 80):
                score = score - 3
            else:
                score = 80
        elif(score > 70 and complexity == 8):
            if (score - 3 > 70):
                score = score - 3
            else:
                score = 70
        elif (score > 60 and complexity == 9):
            if (score - 3 > 60):
                score = score - 3
            else:
                score = 60
    return score
