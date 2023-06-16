#!/bin/bash

module add python36-modules-gcc

module avail python/ # list available modules
module load python   # load (default) module

module add python36-modules-gcc

DATADIR=/storage/plzen1/home/astrox/eda/yolov8_testing

cp -r $DATADIR/* $SCRATCHDIR

cd $SCRATCHDIR

python3 $SCRATCHDIR/yolov8_testing.py

OUTPUTDIR=/storage/plzen1/home/astrox/eda/yolov8_testing_output

mv * $OUTPUTDIR
