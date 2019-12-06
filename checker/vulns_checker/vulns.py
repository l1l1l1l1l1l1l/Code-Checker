import subprocess
import sys
import csv
from io import StringIO


# Check aims at tarRepo and check any vulnerability it may have
# @params tarRepo: string absolute path of target Python repo
# @params loc: int lines of code of py file of whole repo
# @return score: int ranged from 0 to 100, 100 is best, 0 is worst in terms of code quality
# @return output: string detailed output from bandit, in csv format
def Check(tarRepo, loc):
    loc = int(loc)
    output = subprocess.run(['python3', '-m', 'bandit', '-r', tarRepo,
                             '-q', '-f', 'csv'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    reader = csv.reader(StringIO(output), delimiter=',')
    penalty = 0
    for row in reader:
        if row[3] == 'UNDEFINED':
            penalty += 1
        if row[3] == 'LOW':
            penalty += 5
        if row[3] == 'MEDIUM':
            penalty += 25
        if row[3] == 'HIGH':
            penalty += 50

    # we assume in every 100 lines of code, maximumly 5 points of vulnerability is allowed
    if penalty > loc * 0.05:
        score = 0
    else:
        # if no more than 5 points found, then score if 100 minus penalty
        score = int((1 - penalty / (loc * 0.05)) * 100)
    return score, output


if __name__ == '__main__':
    score, output = Check(sys.argv[1], sys.argv[2])
    print(score)
    print(output)
