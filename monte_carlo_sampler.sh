#!/bin/bash

echo
echo start: $(date "+%y-%m-%d %H:%M:%S.%3N")
echo

# run script
cd $PBS_O_WORKDIR
python run_monte_carlo_sampler.py $1 $2 $3
# ---------

echo
echo stop:  $(date "+%y-%m-%d %H:%M:%S.%3N")
echo
