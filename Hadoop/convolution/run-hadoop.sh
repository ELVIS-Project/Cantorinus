#!/usr/bin/env bash

hadoop jar $HADOOP_STREAM \
 -file "/home/afogarty/Cantorinus/Hadoop/convolution/mapper.py" -mapper /home/afogarty/Cantorinus/Hadoop/convolution/mapper.py \
  -file "/home/afogarty/Cantorinus/Hadoop/convolution/reducer.py" -reducer /home/afogarty/Cantorinus/Hadoop/convolution/reducer.py \
   -input mandrill.csv -output convolution