from pathlib import Path
import logging
import re
import io
import numpy as np
import pandas as pd
import argparse

experiment_directory = '../cm2015_StateMod/StateMod'

expected_column_sizes = np.asarray([11, 12, 4, 4, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                                    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                                    7, 7, 7, 7, 7, 7, 7, 12, 11])

ids_of_interest = np.genfromtxt('./inputs/output_ids.txt', dtype='str').tolist()
expected_line_size = expected_column_sizes.sum() + len(expected_column_sizes)
expected_column_count = 35
month_column = 3
id_column = 0
year_column = 2
demand_column = 4
shortage_column = 17
id_column_name = 'structure_id'
year_column_name = 'year'
month_column_name = 'month'
demand_column_name = 'demand'
shortage_column_name = 'shortage'
id_column_type = object
year_column_type = np.uint16
month_column_type = object
demand_column_type = np.uint32
shortage_column_type = np.uint32
sample_column_name = 'sample'
sample_column_type = np.uint16

def xxd_to_parquet(sample_number):
    path = Path(experiment_directory + '/cm2015B_' + str(sample_number) + '.xdd')
    # stream will hold CSV of interesting data
    stream = io.StringIO()
    # read the file line by line
    with open(path, 'r') as file:
        for line in file:
            # note here that we make two simplifying assumptions:
            #   - all structure ids of interest start with a digit
            #   - only lines of data start with a digit
            if line[0].isdigit() and line[0:expected_column_sizes[0] + 1].strip() in ids_of_interest:
                if len(line) != expected_line_size:
                    # unexpected line length; you need to double check the expected column sizes
                    logging.error(
                        f"Unexpected line length: {len(line)} instead of {expected_line_size}:\n{line}"
                    )
                    return False
                # split data by character counts
                data = []
                position = 0
                for count in expected_column_sizes:
                    data.append(line[position:position + count].strip())
                    # account for single space between columns
                    position += count + 1
                if len(data) != expected_column_count:
                    # unexpected number of columns; you need to double check your data and settings
                    logging.error(
                        f"Unexpected column count: {len(data)} instead of {expected_column_count}:\n{line}"
                    )
                    return False
                # only keep non-total rows
                if not data[month_column].casefold().startswith('tot'):
                    stream.write(
                        ','.join(
                            [data[i] for i in [
                                id_column,
                                year_column,
                                month_column,
                                demand_column,
                                shortage_column
                            ]]
                        )
                    )
                    stream.write('\n')
    stream.seek(0)

    df = pd.read_csv(
        stream,
        header=None,
        names=[
            id_column_name,
            year_column_name,
            month_column_name,
            demand_column_name,
            shortage_column_name
        ],
        dtype={
            id_column_name: id_column_type,
            year_column_name: year_column_type,
            month_column_name: month_column_type,
            demand_column_name: demand_column_type,
            shortage_column_name: shortage_column_type
        }
    )

    stream.close()

    df[sample_column_name] = sample_column_type(sample_number)
    df.to_parquet(
        Path(f'./outputs/S{sample_number}.parquet'),
        engine='pyarrow',
        compression='gzip'
    )
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert .xdd to .parquet')
    parser.add_argument('sample_number', type=int)
    args = parser.parse_args()
    xxd_to_parquet(args.sample_number)