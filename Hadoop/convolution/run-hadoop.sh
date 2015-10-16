#!/usr/bin/env bash

# This is the command to run the MapReduce job on Guillimin

hadoop jar $HADOOP_STREAM \
 -file "/home/afogarty/Cantorinus/Hadoop/convolution/mapper.py" -mapper /home/afogarty/Cantorinus/Hadoop/convolution/mapper.py \
  -file "/home/afogarty/Cantorinus/Hadoop/convolution/reducer.py" -reducer /home/afogarty/Cantorinus/Hadoop/convolution/reducer.py \
   -input mandrill.csv -output convolution