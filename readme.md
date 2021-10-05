# Training on generating and executing a small sensitivity analysis on StateMod

## Setup
### 1. Clone this directory
```
git clone https://github.com/antonia-had/statemod_experiment.git
```

### 2. Setup the model and input files

Clone git repository with StateMod executable and Upper Colorado dataset:
```
git clone https://github.com/antonia-had/cm2015_StateMod 
``` 

Give execution permissions to statemod executable:
```
cd cm2015_StateMod/StateMod/
chmod +x statemod
```
Test if it runs with:
```
./statemod cm2015B –simulate
```

**Note: This only runs on linux machines.** 

---
Optional:
You can compile the StateMod executable and download model files yourself. Directions for this can be found in the first training in this series (at the end of the slidedeck): https://cornell.box.com/s/xlwk6smzrikykmwyt2d7vxb7042puit0  

Before you proceed, `cm2015_StateMod/StateMod` should contain all StateMod input files in the convention `cm2015B.*` and the StateMod executable.

Test if it runs **fully** before proceeding. At the end you should have several output and binary files created in the same repository (e.g., you should have a `cm2015B.xdd`). 

 You can reduce number of reoperations to speed up model runs. To do this you need to edit the control file (`cm2015.ctl`) and change the value of the `ireopx` variable from 0 to 10. This is already done for you if you clone the `antonia-had/cm2015_StateMod` repository.
    
---

### 3. Install necessary Python packages
You need to create a virtual environment to host all the packages you need for this experiment. To do so, navigate back to the experiment repository directory `statemod_experiment` and run the following commands:
```
python3 -m venv environment_name
source environment_name/bin/activate
pip install -r requirements.txt
```

## Experiment Steps
### 1. Generate Saltelli Sample of model parameters to change
This takes less than a second and can be run on the login node. 

```
python3 ./scripts/generate_sample.py
```
### 2. Create new input files reflecting changes
This is a parallel process depending on the 
3. Execute model runs
4. Collect outputs for different users
5. Generate figures 