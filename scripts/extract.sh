#!/bin/bash

source $ML_VENV_PATH
cd $ML_RUN_PATH
python3 $ML_PYTHON_SCRIPT_PATH/extraction.py --videofilename $1