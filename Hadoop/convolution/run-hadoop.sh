#!/usr/bin/env bash

hadoop jar $HADOOP_STREAM \
-files mapper.py, reducer.py \
-mapper mapper.py \
-reducer reducer.py \
-input mandrill.csv \
-output outputLog.txt