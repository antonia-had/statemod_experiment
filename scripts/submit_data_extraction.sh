#!/bin/bash
#SBATCH --cpus-per-task=1
#SBATCH -p normal
#SBATCH -t 00:10:00
#SBATCH --export=ALL
#SBATCH --mail-user=ah986@cornell.edu
#SBATCH --mail-type=ALL
#SBATCH --array=1-10         # array of tasks to execute

source /home/fs02/pmr82_0001/ah986/statemod_training/bin/activate
DIR="./outputs/"
if ! [ -d "$DIR" ]; then
  mkdir $DIR
fi
srun python3 ./scripts/extract_xdd.py $SLURM_ARRAY_TASK_ID
