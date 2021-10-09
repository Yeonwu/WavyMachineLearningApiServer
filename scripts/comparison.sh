#!/bin/sh
venv_loc=/Users/oyeonwu/.python-venv/soma-ml/bin/activate
python_file=/Users/oyeonwu/Desktop/comparison.py
result_loc=/Users/oyeonwu/Desktop/Repo/soma/WavyMahineLearningApiServer

source $venv_loc
cd $result_loc
python3 $python_file --userjson $1 --usersec $2 --refvideojson $3 --refvideosec $4