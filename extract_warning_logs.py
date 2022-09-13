import os
import csv 

'''Constant paths to the target files'''
ABS_PATH = os.path.abspath(os.curdir)
FILE_PATH = "conan_workarea"

WARNING_TO_FIND = "warning:"#string to find in each line 

warnings = [] #warnings list

#for each directory in conan_workarea find the files
#that starts with build* and then in those files in the 
#conan_run_logs directory find the files that ends with *.log and parse them
try:
    for dir in os.listdir(f'{ABS_PATH}/{FILE_PATH}'):
        # acces only the files that starts with 'build' in name
        if dir.startswith('build'):
            for files in os.listdir(f'{ABS_PATH}/{FILE_PATH}/{dir}/conan_run_logs'):
                # if a '*.log' file is found then execute
                if files.endswith('.log'):
                    with open(f"{ABS_PATH}/{FILE_PATH}/{dir}/conan_run_logs/{files}", "r") as file:
                        for line in file:
                            #this line is true when we find a line that contains 'warning:'
                            if WARNING_TO_FIND in line: 
                                #substract from the line the string that start with 'warning' until end
                                warning = line[line.find("warning") : len(line) - 1] 
                                 #substract from the line the string that start from the beginning until find 'warning'
                                warning_path = line[0 : line.find("warning")]
                                # push to warnings a tuple that contains the warning and the path 
                                warnings.append((warning_path, warning))
                        # sort all warnings by their path to organise the warnings in 'categories'
                        sorted_warnings = sorted(warnings, key = lambda x:x[0]) 
                        file.close()

                    #if file that we want to create is found, delete it
                    if os.path.exists(f"{ABS_PATH}/{FILE_PATH}/{dir}/conan_run_logs/{files}.csv"):
                        os.remove(f"{ABS_PATH}/{FILE_PATH}/{dir}/conan_run_logs/{files}.csv") 

                    #create a new '*.csv' file with all the warnings'
                    #if warnings:
                    if 'dpu' in dir:
                        with open(f"{ABS_PATH}/{FILE_PATH}/{dir}/conan_run_logs/{files}.dpu.csv", "w", newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerows(sorted_warnings)
                            csvfile.close()
                    else:
                        with open(f"{ABS_PATH}/{FILE_PATH}/{dir}/conan_run_logs/{files}.infra.csv", "w", newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerows(sorted_warnings)
                            csvfile.close()
                    #after creating the '*.csv file' clear warnings list     
                    warnings = [] 
                '''
                    #Chart generator
                    if sorted_warnings: 
                        warnings_number = 1
                        chart_frame = []
                        for warning in range(len(sorted_warnings) - 1):
                            if(sorted_warnings[warning][0] == sorted_warnings[warning + 1][0]):
                                warnings_number += 1
                            else:
                                chart_frame.append((sorted_warnings[warning][0], warnings_number))
                                warnings_number = 1
                        x, y = zip(*chart_frame)
                        plot.plot(x, y)
                        plot.axis('off')
                        #plot.show()
                        plot.savefig(f'{ABS_PATH}/{FILE_PATH}/{dir}/conan_run_logs/{files}.jpg')
            '''
except Exception as e:
    print(e)



