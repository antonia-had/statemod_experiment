# Training on generating and executing a small sensitivity analysis on StateMod

## Setup
### Clone this directory

### Setup the model and input files

Compile StateMod executable, download model files and create symbolic link to executable in input directory.

Directions for all this can be found in the first training in this series: https://cornell.box.com/s/xlwk6smzrikykmwyt2d7vxb7042puit0 
 
###Install necessary Python packages
```
python3 -m venv environment_name
source environment_name/bin/activate
pip install -r requirements.txt
```

## Experiment Steps
1. Generate Saltelli Sample of model parameters to change
```
python3 ./scripts/generate_sample.py
```
2. Create new input files reflecting changes
3. Execute model runs
4. Collect outputs for different users
5. Generate figures 