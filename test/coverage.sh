#! /bin/bash

export PYTHONPATH=.

rm .coverage

for test_file in `find . -name "*_tests.py"`
do
    echo "Run coverage for $test_file"
    coverage run --append --source checker $test_file
done

min=0
current_coverage=`coverage report -m | grep  TOTAL | awk '{print $4}' | sed s/%//g`
echo "HTML report is generated at ./htmlcov/index.html"
coverage html

echo "Current coverage is $current_coverage. See more detail in htmlcov."
if [ $current_coverage -lt $min ]; then
    RED='\033[0;31m'
    NC='\033[0m' # No Color
    echo -e "${RED}Current coverage $current_coverage is lower than min requirement $min!!! ${NC}"
    exit -1
fi
