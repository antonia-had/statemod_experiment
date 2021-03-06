import os
import pickle
from utils import writenewXBM, writenewIWR, writenewDDM
from string import Template
import argparse
import logging
import numpy as np

'''Input information setup'''
# Read RSP template
T = open('./inputs/cm2015B_template.rsp', 'r')
template_RSP = Template(T.read())
# Define directory for all files - change to match your own
experiment_directory = '../cm2015_StateMod/StateMod'
# Read in parameter sample
sample = np.loadtxt('./inputs/parameter_values.txt', delimiter=',', dtype=float)
# List of irrigation users
irrigation = np.genfromtxt('./inputs/irrigation.txt', dtype='str').tolist()
# List of transbasin users
transbasin = np.genfromtxt('./inputs/TBD.txt', dtype='str').tolist()

def input_scaling(sample_number):
    '''Get data from original IWR'''
    # We need different subsets to modify and recreate the file
    firstline_iwr = 463
    original_IWR = []
    all_data_IWR = []
    all_split_data_IWR = []
    with open(experiment_directory + '/cm2015B.iwr', 'r') as f:
        for x in f.readlines():
            original_IWR.append(x.split())
            all_data_IWR.append(x)
            all_split_data_IWR.append(x.split('.'))
    original_IWR = original_IWR[firstline_iwr:]

    '''Get data from original DDM'''
    firstline_ddm = 779
    with open(experiment_directory + '/cm2015B.ddm', 'r') as f:
        all_data_DDM = [x for x in f.readlines()]

    '''Get data from original XBM'''
    firstline_xbm = 16
    all_data_XBM = []
    all_split_data_XBM = []
    with open(experiment_directory + '/cm2015x.xbm', 'r') as f:
        for x in f.readlines():
            all_data_XBM.append(x)
            all_split_data_XBM.append(x.split('.'))

    '''
    Extract scaling factors for sample number i
    '''
    irrigation_demand_factor = sample[sample_number, 0]
    transbasin_demand_factor = sample[sample_number, 1]
    flow_factor = sample[sample_number, 2]

    '''
    Apply scaling factors to necessary input files
    '''

    writenewXBM(experiment_directory, all_split_data_XBM, all_data_XBM, firstline_xbm,
                flow_factor, sample_number)

    writenewIWR(experiment_directory, all_split_data_IWR, all_data_IWR, firstline_iwr,
                sample_number, irrigation, irrigation_demand_factor)

    writenewDDM(experiment_directory, all_data_DDM, firstline_ddm, original_IWR,
                firstline_iwr, sample_number, irrigation, transbasin, transbasin_demand_factor)

    d = {'IWR': 'cm2015B_' + str(sample_number) + '.iwr',
         'DDM': 'cm2015B_' + str(sample_number) + '.ddm',
         'XBM': 'cm2015x_' + str(sample_number) + '.xbm'}
    new_rsp = template_RSP.safe_substitute(d)
    f1 = open(experiment_directory + '/cm2015B_' + str(sample_number) + '.rsp', 'w')
    f1.write(new_rsp)
    f1.close()

    print('running cm2015B ' + str(sample_number))
    # Run simulation
    processing_directory = os.getcwd() # get current
    os.chdir(experiment_directory)
    os.system('./statemod cm2015B_{} -simulate'.format(sample_number))
    os.chdir(processing_directory)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create inputs for sample')
    parser.add_argument('i', type=int,
                        help='sample number')
    args = parser.parse_args()
    input_scaling(args.i)