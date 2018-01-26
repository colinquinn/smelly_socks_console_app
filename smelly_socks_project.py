import csv
import time
import datetime
import sys

welcome = '''\


===================================================================================================
   _____                _ _          _____            _          _____           _           _
  / ____|              | | |        / ____|          | |        |  __ \         (_)         | |
 | (___  _ __ ___   ___| | |_   _  | (___   ___   ___| | _____  | |__) | __ ___  _  ___  ___| |_
  \___ \| '_ ` _ \ / _ \ | | | | |  \___ \ / _ \ / __| |/ / __| |  ___/ '__/ _ \| |/ _ \/ __| __|
  ____) | | | | | |  __/ | | |_| |  ____) | (_) | (__|   <\__ \ | |   | | | (_) | |  __/ (__| |_
 |_____/|_| |_| |_|\___|_|_|\__, | |_____/ \___/ \___|_|\_\___/ |_|   |_|  \___/| |\___|\___|\__|
                             __/ |                                             _/ |
                            |___/                                             |__/
===================================================================================================

Welcome, please wait for system tests to finish...


'''
sys_options = '''\
1) Run Experiment
2) View CSV Library
3) Ping FTP
4) Conduct System Tests

Your selection:
'''

# print(welcome);
# time.sleep(5)
print(sys_options)

action = None
while not action:
    try:
        action = int(raw_input())
    except ValueError:
        print 'Invalid Number'


experiment_interface = '''\

Smelly Socks Experiment Interface - Please Fill in Following Information
===================================================================================================

Sock Owner Name:
'''
experiemnt_Details = '''\
Experiemnt Details:

Sock Owner\t\t\tCSV name\t\t\tExperiment Number
---------------\t\t\t---------------\t\t\t---------------
'''

def run_experiment():
    print(experiment_interface)

    name = None
    while not name:
        try:
            name = str(raw_input())
        except ValueError:
            print 'Invalid Name'

    date_ljust = str(datetime.datetime.utcnow().strftime("%d-%m-%Y_%I:%M%p").ljust(32, ' '))
    print(experiemnt_Details)
    print(name.ljust(32, ' ') + date_ljust + '000000007826'.ljust(32, ' ') + '\n')

    raw_input('Confirm information and prep Gates, press enter to begin. \n ')

    experiment_header = '''\
===================================================================================================
    !!! EXPERIMENT IN PROGRESS  !!!
===================================================================================================
    '''

    experiment_footer = '''\

===================================================================================================
    !!! EXPERIMENT CONCLUDED, CLOSE GATES  !!!
===================================================================================================
    '''
    print(experiment_header)
    count_down('Open gates in', 5, '', False)
    start_sensor_reader()
    print(experiment_footer)

    print('CSV saved to' + name)
    # myData = [[1, 2, 3], ['Good Morning', 'Good Evening', 'Good Afternoon']]
    # myFile = open('test1.csv', 'w')
    # with myFile:
    #     writer = csv.writer(myFile)
    #     writer.writerows(myData)
    #     print('Complete')
def start_sensor_reader():
    sys.stdout.flush()
    for x in range (0,30):
        print('generate_random_data_point()')
        time.sleep(.1)


def count_down(front_message, sleep_time, back_message, blank_sleep):
    if blank_sleep is False:
        for remaining in range(sleep_time, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write(front_message + "{:2d} ".format(remaining) + back_message)
            sys.stdout.flush()
            time.sleep(1)
    else:
            time.sleep(sleep)

def print_csv_library():
    with open('./csv_library/test_csv.csv') as myFile:
        reader = csv.reader(myFile)
        for row in reader:
            print(row)

if action == 1:
    run_experiment()
else:
     if action == 2:
         print_csv_library()
     else:
        if action ==3:
            print('3')
        else:
            if action == 4:
                print('4')
