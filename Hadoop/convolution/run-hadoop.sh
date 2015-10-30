#!/usr/bin/env bash
#HADOOP_STREAM

hadoop jar \
-files mapper.py, reducer.py \
-mapper mapper.py \
-reducer reducer.py \
-input mandrill.csv \
-output outputLog.txt
