'''
Input file: /naive_result/raw
Output file: /naive_result/processed
#
The script will read all raw data from the input directory,
and will return a single file for each participants which
will be ready for psychometric curve fitting in fitting.py
'''

import numpy as np
import os
import pandas as pd

input_folder_path =\
    "C:/Users/Herrick Fung/Desktop/Course Materials/Sem 4.1/\
PSY402 Research Thesis II/experiment/naive_result/raw/"
output_folder_path =\
    "C:/Users/Herrick Fung/Desktop/Course Materials/Sem 4.1/\
PSY402 Research Thesis II/experiment/naive_result/processed/"


def read_and_sort(filename):
    input_filename = "raw/" + filename
    output_filename = "processed/processed_" + filename

    # Read the input file & return response, j = 1, f = 0
    input_data = pd.read_csv(input_filename, 'r', delimiter = ',')
    input_data['return_resp'] = \
        input_data['Response'].replace(to_replace=["j","f"], value=[1,0])

    # Create array for output data frame
    date_array = []
    time_array = []
    name_array = []
    age_array = []
    gender_array = []
    hand_array = []
    condition_array = []
    neg30_array = []
    neg20_array = []
    neg10_array = []
    zero_array = []
    pos10_array = []
    pos20_array = []
    pos30_array = []
    deg = []
    np.array(deg)
    names = [
        neg30_array, neg20_array, neg10_array,
        zero_array, pos10_array, pos20_array,
        pos30_array
    ]
    for name in names:
        deg.append(name)
    accuracy_10 = []
    accuracy_20 = []
    accuracy_30 = []
    latency_mean_array = []
    latency_sd_array = []

    # read from input and write from output (Participant Basic info. and Con.)
    date_array = input_data.Exp_Date[0:4]
    time_array = input_data.Exp_Time[0:4]
    name_array = input_data.Sub_Name[0:4]
    age_array = input_data.Age[0:4]
    gender_array = input_data.Gender[0:4]
    hand_array = input_data.Dominant_Hand[0:4]
    condition_array = [1,2,3,4]

    '''
    Obtain mean and n-1 sd for latency for each condition &
    Count no. of "J" response for each orientation and each condition
    '''
    orientation = [-30,-20,-10,0,10,20,30]
    con1_count = []
    con2_count = []
    con3_count = []
    con4_count = []
    condition = []
    np.array(condition)
    for names in [con1_count, con2_count, con3_count, con4_count]:
        condition.append(names)
        np.array(names)

    for con in condition_array:
        # for latency
        con_frame = input_data[input_data.Condition == con]
        latency_mean_array.append(con_frame['Latency'].mean(axis = 0))
        latency_sd_array.append(con_frame['Latency'].std(axis = 0))

        # for response
        for ori in orientation:
            if con == 1 or con == 4:
                ori_frame = con_frame[con_frame.Cued_Orientation == ori]
                if con == 1:
                    con1_count.append(ori_frame['return_resp'].sum(axis = 0))
                else:
                    con4_count.append(ori_frame['return_resp'].sum(axis = 0))
            else:
                ori_frame = con_frame[con_frame.Set_Orientation == ori]
                if con == 2:
                    con2_count.append(ori_frame['return_resp'].sum(axis = 0))
                else:
                    con3_count.append(ori_frame['return_resp'].sum(axis = 0))

    for i in range(4):
        for j in range(7):
            deg[j].append(condition[i][j])
        accuracy_10.append(14 - condition[i][2] + condition[i][4])
        accuracy_20.append(14 - condition[i][1] + condition[i][5])
        accuracy_30.append(14 - condition[i][0] + condition[i][6])

    # Create the output dataframe and saved to output file path
    output_data = pd.DataFrame({'Exp_Date': date_array,
                                'Exp_Time': time_array,
                                'Parti_Name': name_array,
                                'Age': age_array,
                                'Gender': gender_array,
                                'Dominant_Hand': hand_array,
                                'Condition': condition_array,
                                'Count_-30': neg30_array,
                                'Count_-20': neg20_array,
                                'Count_-10': neg10_array,
                                'Count_0': zero_array,
                                'Count_+10': pos10_array,
                                'Count_+20': pos20_array,
                                'Count_+30': pos30_array,
                                'Accuracy_10': accuracy_10,
                                'Accuracy_20': accuracy_20,
                                'Accuracy_30': accuracy_30,
                                'Latency_Mean': latency_mean_array,
                                'Latency_SD': latency_sd_array
                                })
    output_data.to_csv(output_filename, sep=',', index=False)


def main():
    # Create the output directory
    try:
        os.mkdir(output_folder_path)
        print("Processed Directory Created!")
    except FileExistsError:
        print("Processed Directory Existed!")

    # sort out the main result files from input directory and work on it
    print("Processed the following files:")
    for filename in os.listdir(input_folder_path):
        if filename.endswith("_ep_experiment.csv"):
            print(filename)
            read_and_sort(filename)


if __name__ == "__main__":
    main()
