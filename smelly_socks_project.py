# Author: Colin O. Quinn
# Date Modified: 1/30/2018
# Email:
import os
import csv
import time
import datetime
import sys
from random import randint

#default vairables
global SOCK_OWNER_NAME = 'no_name_entered'
SOCK_OWNER_COUNTRY = 'no_country_entered'
CURRENT_DATE_TIME = 'system_date_error'
CSV_FILE_NAME = 'no_time_stamp_assigned'
EXPERIMENT_PREP_TIME = 5
EXPERIMENT_RUN_TIME = 30
DATA_COLLECTED = []

welcome = '''
===================================================================================================
   _____                _ _          _____            _          _____           _           _
  / ____|              | | |        / ____|          | |        |  __ \         (_)         | |
 | (___  _ __ ___   ___| | |_   _  | (___   ___   ___| | _____  | |__) | __ ___  _  ___  ___| |_
  \___ \| '_ ` _ \ / _ \ | | | | |  \___ \ / _ \ / __| |/ / __| |  ___/ '__/ _ \| |/ _ \/ __| __|
  ____) | | | | | |  __/ | | |_| |  ____) | (_) | (__|   <\__ \ | |   | | | (_) | |  __/ (__| |_
 |_____/|_| |_| |_|\___|_|_|\__, | |_____/ \___/ \___|_|\_\___/ |_|   |_|  \___/| |\___|\___|\__|
                             __/ |                                             _/ |
                            |___/                                             |__/
===================================================================================================\n
Welcome, please wait for system tests to finish...\n
'''
sys_options = '''\
Please select one of the following:\n
1) Run Experiment
2) View CSV Library
3) Ping FTP
4) Conduct System Tests
5) Quit (or ctrl+c at anytime)\n
Your selection:
'''
#2) Push CSV library to server
experiment_interface = '''
Selection (1):\n
Smelly Socks Experiment Interface - Fill in Following Information
===================================================================================================
'''
experiment_details = '''
Sock Owner\t\t\tSock Owner Country\t\tCSV name\t\t\tExperiment Number
--------------------\t\t--------------------\t\t--------------------\t\t-------------------
''' + SOCK_OWNER_NAME.ljust(32, ' ') + SOCK_OWNER_COUNTRY.ljust(32, ' ') + CSV_FILE_NAME.ljust(32, ' ') + '000000007826'.ljust(32, ' ') + '''\n
'''
experiment_header = '''\
===================================================================================================
!!! EXPERIMENT IN PROGRESS  !!!
===================================================================================================
'''
experiment_footer = '''\n
===================================================================================================
    !!! EXPERIMENT CONCLUDED, CLOSE GATES  !!!
===================================================================================================
    '''
experiment_summary_and_re_prompt = '''\

Experiment summary:
===================================================================================================\n
'''+ experiment_details + '''\n
- Experiment CSV has been written to ".\csv_library\ ''' + CSV_FILE_NAME + '''"
- To push the CVS(s) in csv_library, select option #2\n
===================================================================================================\n
'''

def run_experiment():
    clear()
    print(experiment_interface)
    print('Sock Owner Name:\n')
    SOCK_OWNER_NAME = retrieve_name_from_user()
    print('\nSock Owner Country:')
    SOCK_OWNER_COUNTRY = retrieve_country_from_user()

    CURRENT_DATE_TIME = str(datetime.datetime.utcnow().strftime("%d-%m-%Y_%H:%M"))
    CSV_FILE_NAME = CURRENT_DATE_TIME + '.csv'
    clear()
    print('Experiemnt Details:')
    print(experiment_details)
    # print(SOCK_OWNER_NAME.ljust(32, ' ') + SOCK_OWNER_COUNTRY.ljust(32, ' ') + CSV_FILE_NAME.ljust(32, ' ') + '000000007826'.ljust(32, ' ') + '\n')

    raw_input('Confirm information and prep Gates, press enter to begin. (You will have 5 seconds to get into place)\n ')

    print(experiment_header)
    count_down('Open gates in', EXPERIMENT_PREP_TIME, '', False)
    start_sensor_reader()
    print(experiment_footer)

    print('CSV saved to ' + CSV_FILE_NAME + '\n\n')
    myData = []
    if yes_or_no('Rerun experiment? <y/n + enter>') == False:
        write_to_csv()
    else:
        run_experiment()

def write_to_csv():
    DATA_COLLECTED = [[SOCK_OWNER_NAME, SOCK_OWNER_COUNTRY, CURRENT_DATE_TIME] , [randint(0,1) for p in range(0,30)]] #Delete when real data is here
    csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE)
    new_csv_file = open('.\csv_library\\' + CSV_FILE_NAME, 'w')
    with new_csv_file:
        writer = csv.writer(new_csv_file, dialect = 'myDialect')
        writer.writerows(DATA_COLLECTED)
    clear()
    print(experiment_summary_and_re_prompt)
    print(sys_options)
    choose_path()

def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Please enter either y or n")

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
            time.sleep(sleep_time)

def print_csv_library():
    with open('./csv_library/test_csv.csv') as myFile:
        reader = csv.reader(myFile)
        for row in reader:
            print(row)

def retrieve_name_from_user():
    name = None
    while not name:
        try:
            name = str(raw_input())
        except ValueError:
            print 'Invalid Name'
    return name

def retrieve_country_from_user():
    country = None
    while not country:
        try:
            country = str(raw_input()) #Use pyCountry in the future
        except ValueError:
            print 'Invalid Country'
    return country

def choose_path():
    action = None
    while not action:
        try:
            action = int(raw_input())
        except ValueError:
            print('Invalid Number')

    if action == 1:
        run_experiment()
        #write_to_csv() use for testing only
    else:
         if action == 2:
             print_csv_library()
         else:
            if action ==3:
                print('3')
            else:
                if action == 4:
                    print('4')
def clear():
     os.system('cls' if os.name=='nt' else 'clear')
clear()
print(welcome.center(30));
# time.sleep(4)
print(sys_options)
choose_path()
#
# mosquito = '''
#            _         _
#           /x\       /x\
#          /v\x\     /v\/\
#          \><\x\   /></x/
#           \><\x\ /></x/
#   __ __  __\><\x/></x/___
#  /##_##\/       \</x/    \__________
# |###|###|  \         \    __________\
#  \##|##/ \__\____\____\__/          \\
#    |_|   |  |  | |  | |              \|
#    \*/   \  |  | |  | /              /
#            /    /
#
# '''
