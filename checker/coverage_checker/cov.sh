#! /bin/bash

export PYTHONPATH=$0

rm .coverage

for test_file in `find $0 -name "*_tests.py"`
do
    coverage run --append --source checker $test_file
done

current_coverage=`coverage report -m | grep  TOTAL | awk '{print $4}' | sed s/%//g`
coverage html

echo $current_coverage
