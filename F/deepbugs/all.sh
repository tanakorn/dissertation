#!/bin/bash

echo "generating raw"
cd script
./genhtml.py ../../../../jira-study-db-svn/

echo "generating dat"
cd ../raw
for f in $(ls *)
do
    ../script/process.sh $f
done

echo "generating eps"
cd ../plot
/usr/bin/env gnuplot deepbugs.plt

