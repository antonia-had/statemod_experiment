#!/bin/bash
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=80
#SBATCH -p normal
#SBATCH -t 00:10:00
#SBATCH --export=ALL
#SBATCH --exclusive
#SBATCH --mail-user=ah986@cornell.edu
#SBATCH --mail-type=ALL

module load parallel
source /home/fs02/pmr82_0001/ah986/statemod_training/bin/activate

# This specifies the options used to run srun. The "-N1 -n1" options are
# used to allocates a single core to each task.
srun="srun --export=all"
# This specifies the options used to run GNU parallel:
#
#   --delay of 0.2 prevents overloading the controlling node.
#
#   -j is the number of tasks run simultaneously.
#
#   The combination of --joblog and --resume create a task log that
#   can be used to monitor progress.
#
parallel="parallel --delay 0.2 -j 80 --joblog statemod_runs.log"
$srun $parallel "python3 ./scripts/generate_input_files.py" ::: {1..320}