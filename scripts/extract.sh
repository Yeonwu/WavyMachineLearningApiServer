#!/bin/sh
venv_loc=/Users/oyeonwu/.python-venv/soma-ml/bin/activate
python_file=/Users/oyeonwu/Desktop/extraction.py
result_loc=/Users/oyeonwu/Desktop/Repo/soma/WavyMachineLearningApiServer

source $venv_loc
cd $result_loc
python3 $python_file --videofilename $1