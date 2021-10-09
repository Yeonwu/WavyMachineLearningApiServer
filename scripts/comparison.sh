#!/bin/bash

source $ML_VENV_PATH
cd $ML_RUN_PATH
python3 $ML_PYTHON_SCRIPT_PATH/comparison.py --userjson $1 --usersec $2 --refvideojson $3 --refvideosec $4