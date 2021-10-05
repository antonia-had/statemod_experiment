from SALib.sample import saltelli
import numpy as np

# Define the uncertainties
problem = {
    'num_vars': 3,
    'names': ['Irrigation_Demand',
              'Transbasin_Demand',
              'Flows_scaling'],
    'bounds': [[0.5, 1.5],
               [0.5, 1.5],
               [0.5, 1.5]]
}

'''
Generate samples
'''
# Note that an appropriate SA sample should be in the order of n*(m+2)
# where m is the number of parameters and n is ~ 1000.
# This is smaller for the purposes of demonstration.
param_values = saltelli.sample(problem, 64, calc_second_order=False)

np.savetxt('./inputs/parameter_values.txt', param_values, delimiter=',')