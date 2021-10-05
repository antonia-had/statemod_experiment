import numpy as np

# lengths of intervals to split rows in
lengths = [5, 12, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10]  # lengths of intervals to split rows in
lengths_XBM = [5, 13, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]

def writenewXBM(experiment_directory, all_split_data_XBM, all_data_XBM, firstline_xbm,
                flow_factor, i):
    # replace former flows with new flows
    new_data = []
    for i in range(len(all_split_data_XBM) - firstline_xbm):
        row_data = []
        # split first 3 columns of row on space and find 1st month's flow
        row_data.extend(all_split_data_XBM[i + firstline_xbm][0].split())
        row_data[2] = int(row_data[2])
        # find remaining months' flows
        for j in range(1, 12):
            row_data.append(int(all_split_data_XBM[i + firstline_xbm][j]))
        # scale all flows
        for j in range(2, 14):
            row_data[j] = int(row_data[j] * flow_factor)
        # calculate totals
        row_data.append(sum(row_data[2:]))
        row_data = [str(x) for x in row_data]
        # append row of adjusted data
        new_data.append(row_data)

    f = open(experiment_directory + '/cm2015x_' + str(i) + '.xbm', 'w')
    # write firstLine # of rows as in initial file
    for i in range(firstline_xbm):
        f.write(all_data_XBM[i])

    for i in range(len(new_data)):
        # write year, ID and first month of adjusted data
        f.write(new_data[i][0] + ' ' + new_data[i][1] + (19 - len(new_data[i][1]) - len(new_data[i][2])) * ' ' +
                new_data[i][2] + '.')
        # write all but last month of adjusted data
        for j in range(len(new_data[i]) - 4):
            f.write((7 - len(new_data[i][j + 3])) * ' ' + new_data[i][j + 3] + '.')

        # write last month of adjusted data
        if len(new_data[i][-1]) <= 7:
            f.write((7 - len(new_data[i][-1])) * ' ' + new_data[i][-1] + '.' + '\n')
        else:
            f.write('********\n')

    f.close()


def writenewIWR(experiment_directory, all_split_data, all_data, firstline_iwr,
                i, users, irrigation_demand_factor):
    # replace former iwr demands with new
    new_data = []
    for j in range(len(all_split_data) - firstline_iwr):
        row_data = []
        # split first 3 columns of row on space and find 1st month's flow
        row_data.extend(all_split_data[j + firstline_iwr][0].split())
        # check if year is a curtailment year and if user is to be curtailed
        if row_data[1] in users:
            # scale first month
            value = float(row_data[2]) * irrigation_demand_factor
            row_data[2] = str(int(value))+'.'
            # scale other months
            for k in range(len(all_split_data[j + firstline_iwr]) - 2):
                value = float(all_split_data[j + firstline_iwr][k + 1]) * irrigation_demand_factor
                row_data.append(str(int(value))+'.')
        else:
            row_data[2] = str(int(row_data[2])) + '.'
            for k in range(len(all_split_data[j + firstline_iwr]) - 2):
                value = float(all_split_data[j + firstline_iwr][k + 1])
                row_data.append(str(int(value))+'.')
        # append row of adjusted data
        new_data.append(row_data)

    f = open(experiment_directory + '/cm2015B_' + str(i) + '.iwr', 'w')
    # write firstLine # of rows as in initial file
    for j in range(firstline_iwr):
        f.write(all_data[j])
    for k in range(len(new_data)):
        # write year and ID (spaces after the entry)
        for j in range(2):
            f.write(new_data[k][j] + (lengths[j] - len(new_data[k][j])) * ' ')
        # write all the rest (spaces before the entry)
        for j in range(2, len(new_data[k])):
            f.write((lengths[j] - len(new_data[k][j])) * ' ' + new_data[k][j])
        # write line break
        f.write('\n')
    f.close()
    return None

def writenewDDM(experiment_directory, all_data_DDM, firstline_ddm, original_IWR,
                firstline_iwr, i, irrigation, transbasin, transbasin_demand_factor):
    users = irrigation+transbasin
    with open(experiment_directory + '/cm2015B_' + str(i) + '.iwr') as f:
        sample_IWR = [row for row in f.readlines()[firstline_iwr:]]
    for m in range(len(sample_IWR)):
        sample_IWR[m] = [sample_IWR[m][sum(lengths[:k]):sum(lengths[:k+1])] for k in range(len(lengths))]

    new_data = []
    irrigation_encounters = np.zeros(len(users))

    for j in range(len(all_data_DDM) - firstline_ddm):
        # To store the change between historical and sample irrigation demand (12 months + Total)
        change = np.zeros(13)
        # Split first 3 columns of row on space
        # This is because the first month is lumped together with the year and the ID when spliting on periods
        row = all_data_DDM[j + firstline_ddm]
        row_data = [row[sum(lengths[:k]):sum(lengths[:k+1])] for k in range(len(lengths))]
        # If the structure is not in the ones we care about then do nothing
        if row_data[1].strip() in users:
            if row_data[1].strip() in irrigation:
                index = np.where(users == row_data[1].strip())[0][0]
                line_in_iwr = int(irrigation_encounters[index] * len(users) + index)
                irrigation_encounters[index] = +1
                for m in range(len(change)):
                    change[m] = float(sample_IWR[line_in_iwr][2 + m]) - float(original_IWR[line_in_iwr][2 + m])
                    value = float(row_data[m + 2]) + change[m]
                    row_data[m + 2] = str(int(value))+'.'
            if row_data[1].strip() in transbasin:
                for m in range(len(change)):
                    value = float(row_data[m + 2]) * transbasin_demand_factor
                    row_data[m + 2] = str(int(value))+'.'
                    # append row of adjusted data
        new_data.append(row_data)
        # write new data to file

    f = open(experiment_directory + '/cm2015B_' + str(i) + '.ddm', 'w')
    # write firstLine # of rows as in initial file
    for j in range(firstline_ddm):
        f.write(all_data_DDM[j])
    for k in range(len(new_data)):
        # write year and ID (spaces after the entry)
        for j in range(2):
            f.write(new_data[k][j] + (lengths[j] - len(new_data[k][j])) * ' ')
        # write all the rest (spaces before the entry)
        for j in range(2, len(new_data[k])):
            f.write((lengths[j] - len(new_data[k][j])) * ' ' + new_data[k][j])
        # write line break
        f.write('\n')
    f.close()
    return None