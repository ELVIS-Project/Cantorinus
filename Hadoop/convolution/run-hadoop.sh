#!/usr/bin/env bash

hadoop jar $HADOOP_STREAM \
 -file "mapper.py" -mapper mapper.py \
  -file "reducer.py" -reducer reducer.py \
   -input mandrill.csv -output convolution