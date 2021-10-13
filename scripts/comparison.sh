#!/bin/bash

source $ML_VENV_PATH
cd $ML_RUN_PATH
python3 $ML_PYTHON_SCRIPT_PATH/comparison.py --ujsonfilepath $ML_PYTHON_SCRIPT_PATH/results/$1 --usec $2 --rvjsonfilepath $3 --rvsec $4
